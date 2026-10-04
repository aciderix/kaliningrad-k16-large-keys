// bdt_gpu.cu — attaque par dictionnaire de la double transposition sur GPU (BLUME SALAMANCA).
// Même méthode que tools/bdt.c, mode dict : chaque clé-phrase (11–30 lettres) est essayée comme K2 pour chaque w1
// (IDP de T1, bigrammes PMI espagnols, plages exactes de fin de colonne, chaîne gloutonne de CrypTool 2), et comme
// clé unique (K1 = K2, quadrigrammes de T1 + T2). Les deux numérotations sont essayées : ex aequo de gauche à droite
// (variante 0) et de droite à gauche (variante 1). Scores en z contre des clés aléatoires de même largeur.
// Compilation : nvcc -O3 -arch=sm_60 -o bdt_gpu bdt_gpu.cu   (T4 : sm_75 ; P100 : sm_60)
// Usage : bdt_gpu qg.bin T1.txt T2.txt cles.txt w1a w1b lo hi variantes(1|2) zrec top
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <cuda_runtime.h>

#define MAXN 640
#define MAXW 32
#define MAXW1 31
#define CK(x) do { cudaError_t e_ = (x); if (e_ != cudaSuccess) { fprintf(stderr, "CUDA %s @%d: %s\n", #x, __LINE__, cudaGetErrorString(e_)); exit(1); } } while (0)

__constant__ float cBG[676];
__constant__ int cMine[MAXW1 + 1][MAXW1 + 1], cMaxe[MAXW1 + 1][MAXW1 + 1];
__constant__ float cMu[MAXW1 + 1][MAXW + 1], cSd[MAXW1 + 1][MAXW + 1], cSMu[MAXW + 1], cSSd[MAXW + 1];
__constant__ unsigned char cC1[MAXN], cC2[MAXN];

struct Hit { int key; short w1, w2; char kind, var; float z; };

// ---------- IDP : un bloc par (clé, w1) ----------
__global__ void idpKernel(const unsigned char *perms, const unsigned char *w2s, int nk, int w1a, int n,
                          Hit *hits, int *nhits, int maxhits, unsigned int *hist, float zrec, float *raw) {
    int kid = blockIdx.x, w1 = w1a + blockIdx.y, tid = threadIdx.x, bd = blockDim.x;
    if (kid >= nk) return;
    __shared__ unsigned char I[MAXN];
    __shared__ int start[MAXW];
    __shared__ float m[MAXW1 * MAXW1];
    __shared__ int left[MAXW1], right_[MAXW1], head[MAXW1];
    __shared__ float rv[256]; __shared__ int ri[256];
    int w2 = w2s[kid]; const unsigned char *perm = perms + (size_t)kid * MAXW;
    if (tid == 0) { int h = n / w2, r = n % w2, k = 0; for (int j = 0; j < w2; j++) { int col = perm[j]; start[col] = k; k += h + (col < r); } }
    __syncthreads();
    for (int i = tid; i < n; i += bd) I[i] = cC1[start[i % w2] + i / w2];
    __syncthreads();
    int full = n / w1, d = w1;
    for (int p = tid; p < d * d; p += bd) {
        int c1 = p / d, c2 = p % d; float best = -1e30f;
        if (c1 == c2) { m[p] = -1e30f; continue; }
        if (n % w1 == 0) {
            int p1 = cMine[w1][c1], p2 = cMine[w1][c2]; float s = 0;
            for (int l = 0; l < full; l++) s += cBG[I[p1 - l] * 26 + I[p2 - l]];
            best = s;
        } else {
            int s1 = cMine[w1][c1] - full + 1, s2 = cMine[w1][c2] - full + 1, o1 = cMaxe[w1][c1] - cMine[w1][c1], o2 = cMaxe[w1][c2] - cMine[w1][c2];
            for (int pass = 0; pass < 2; pass++) {
                int omax = pass == 0 ? o2 : o1;
                for (int off = pass; off <= omax; off++) {
                    int a = s1 + (pass ? off : 0), b = s2 + (pass ? 0 : off); float s = 0;
                    if (a < 0 || b < 0 || a + full > n || b + full > n) continue;
                    for (int i = 0; i < full; i++) s += cBG[I[a + i] * 26 + I[b + i]];
                    if (s > best) best = s;
                    int q1 = a + full, q2 = b + full, k = 0;
                    while (q1 <= cMaxe[w1][c1] && q2 <= cMaxe[w1][c2]) { s += cBG[I[q1] * 26 + I[q2]] - cBG[I[a + k] * 26 + I[b + k]]; k++; q1++; q2++; if (s > best) best = s; }
                }
            }
        }
        m[p] = best / full;
    }
    if (tid < d) { left[tid] = right_[tid] = -1; head[tid] = tid; }
    __syncthreads();
    // chaîne gloutonne (CrypTool 2) : à chaque tour, meilleure paire autorisée (p1 sans voisin droit, p2 sans voisin
    // gauche, pas de cycle sauf au dernier tour) ; ex aequo : plus petit indice p1*d+p2 (comme la boucle séquentielle).
    float sum = 0;
    for (int it = 1; it <= d; it++) {
        float bv = -1e30f; int bi = 0x7fffffff;
        for (int p = tid; p < d * d; p += bd) {
            int p1 = p / d, p2 = p % d;
            if (p1 == p2 || right_[p1] != -1 || left[p2] != -1) continue;
            if (it != d && head[p1] == p2) continue;
            float v = m[p]; if (v > bv || (v == bv && p < bi)) { bv = v; bi = p; }
        }
        rv[tid] = bv; ri[tid] = bi;
        __syncthreads();
        for (int s = bd / 2; s > 0; s >>= 1) {
            if (tid < s) { float v2 = rv[tid + s]; int i2 = ri[tid + s]; if (v2 > rv[tid] || (v2 == rv[tid] && i2 < ri[tid])) { rv[tid] = v2; ri[tid] = i2; } }
            __syncthreads();
        }
        if (tid == 0 && ri[0] != 0x7fffffff && rv[0] > -1e29f) {
            int b1 = ri[0] / d, b2 = ri[0] % d; sum += rv[0]; right_[b1] = b2; left[b2] = b1;
            if (it != d) { int h = head[b1]; int x = b2; while (x != -1) { head[x] = h; x = right_[x]; } }   /* au dernier tour la chaîne se referme : pas de mise à jour */
        }
        __syncthreads();
    }
    if (tid == 0) {
        float v = sum / d;
        if (raw) { raw[(size_t)kid * gridDim.y + blockIdx.y] = v; return; }
        float z = (v - cMu[w1][w2]) / cSd[w1][w2];
        if (z >= 4.0f) { int b = (int)z - 4; if (b > 11) b = 11; atomicAdd(&hist[b], 1u); }
        if (z >= zrec) { int k = atomicAdd(nhits, 1); if (k < maxhits) { hits[k].key = kid; hits[k].w1 = w1; hits[k].w2 = w2; hits[k].kind = 0; hits[k].z = z; } }
    }
}

// ---------- clé unique : un bloc par clé, quadrigrammes de T1 + T2 ----------
__device__ void undoDev(const unsigned char *src, unsigned char *dst, int n, int w, const unsigned char *perm, int *start, int tid, int bd) {
    if (tid == 0) { int h = n / w, r = n % w, k = 0; for (int j = 0; j < w; j++) { int col = perm[j]; start[col] = k; k += h + (col < r); } }
    __syncthreads();
    for (int i = tid; i < n; i += bd) dst[i] = src[start[i % w] + i / w];
    __syncthreads();
}
__global__ void sameKernel(const unsigned char *perms, const unsigned char *w2s, int nk, int n1, int n2, const float *QG,
                           Hit *hits, int *nhits, int maxhits, unsigned int *hist, float zrec, float *raw) {
    int kid = blockIdx.x, tid = threadIdx.x, bd = blockDim.x; if (kid >= nk) return;
    __shared__ unsigned char A[MAXN], B[MAXN], X[MAXN]; __shared__ int start[MAXW]; __shared__ float red[256];
    int w = w2s[kid]; const unsigned char *perm = perms + (size_t)kid * MAXW;
    for (int i = tid; i < n1; i += bd) X[i] = cC1[i];
    __syncthreads();
    undoDev(X, A, n1, w, perm, start, tid, bd); undoDev(A, B, n1, w, perm, start, tid, bd);
    float s = 0;
    for (int i = tid; i + 3 < n1; i += bd) s += QG[((B[i] * 26 + B[i + 1]) * 26 + B[i + 2]) * 26 + B[i + 3]];
    __syncthreads();
    if (n2) { for (int i = tid; i < n2; i += bd) X[i] = cC2[i]; __syncthreads();
        undoDev(X, A, n2, w, perm, start, tid, bd); undoDev(A, B, n2, w, perm, start, tid, bd);
        for (int i = tid; i + 3 < n2; i += bd) s += QG[((B[i] * 26 + B[i + 1]) * 26 + B[i + 2]) * 26 + B[i + 3]]; }
    red[tid] = s; __syncthreads();
    for (int st = bd / 2; st > 0; st >>= 1) { if (tid < st) red[tid] += red[tid + st]; __syncthreads(); }
    if (tid == 0) {
        float v = red[0] / (float)(n1 - 3 + (n2 ? n2 - 3 : 0));
        if (raw) { raw[kid] = v; return; }
        float z = (v - cSMu[w]) / cSSd[w];
        if (z >= 4.0f) { int b = (int)z - 4; if (b > 11) b = 11; atomicAdd(&hist[b], 1u); }
        if (z >= zrec) { int k = atomicAdd(nhits, 1); if (k < maxhits) { hits[k].key = kid; hits[k].w1 = w; hits[k].w2 = w; hits[k].kind = 1; hits[k].z = z; } }
    }
}

// ---------- hôte ----------
static int loadLetters(const char *path, unsigned char *out, int max) {
    FILE *f = fopen(path, "r"); if (!f) { fprintf(stderr, "lecture %s ?\n", path); exit(1); } int n = 0, ch;
    while ((ch = fgetc(f)) != EOF && n < max) { if (ch >= 'a' && ch <= 'z') out[n++] = ch - 'a'; else if (ch >= 'A' && ch <= 'Z') out[n++] = ch - 'A'; }
    fclose(f); return n;
}
static void keyPerm(const std::string &k, int var, unsigned char *perm) {
    int w = (int)k.size(), j = 0;
    for (int r = 0; r < 26; r++) for (int cc = 0; cc < w; cc++) { int c = var ? w - 1 - cc : cc; if (k[c] - 'a' == r) perm[j++] = (unsigned char)c; }
}
static void geo(int n, int w, int *mine, int *maxe) {
    int full = n / w, nl = n % w;
    for (int i = 0; i < w; i++) { mine[i] = full * (i + 1) - 1; maxe[i] = (i < nl) ? full * (i + 1) + i : mine[i] + nl; }
    for (int i = 0; i < w; i++) { int idx = w - 1 - i; if (maxe[idx] > n - 1 - full * i) maxe[idx] = n - 1 - full * i;
        if (i < nl) { int v = n - 1 - full * i - i; if (mine[idx] < v) mine[idx] = v; } else { int v = maxe[idx] - nl; if (mine[idx] < v) mine[idx] = v; } }
}

int main(int argc, char **argv) {
    if (argc < 12) { fprintf(stderr, "usage : bdt_gpu qg.bin T1 T2|- cles w1a w1b lo hi variantes zrec top\n"); return 1; }
    int w1a = atoi(argv[5]), w1b = atoi(argv[6]), lo = atoi(argv[7]), hi = atoi(argv[8]), nvar = atoi(argv[9]), top = atoi(argv[11]);
    float zrec = atof(argv[10]); int nW1 = w1b - w1a + 1;
    std::vector<float> QG(456976); FILE *fp = fopen(argv[1], "rb"); if (!fp || fread(QG.data(), 4, 456976, fp) != 456976) { fprintf(stderr, "modèle ?\n"); return 1; } fclose(fp);
    // bigrammes PMI (identique à bdt.c avec BDT_PMI)
    double L[676], U[26] = {0}, V[26] = {0}, tot = 0; float BG[676];
    for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double s = 0; for (int c = 0; c < 676; c++) s += exp(QG[(a * 26 + b) * 676 + c]); L[a * 26 + b] = log(s); }
    for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double e = exp(L[a * 26 + b]); U[a] += e; V[b] += e; tot += e; }
    for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) BG[a * 26 + b] = (float)(L[a * 26 + b] - log(U[a] / tot) - log(V[b] / tot) - log(tot));
    CK(cudaMemcpyToSymbol(cBG, BG, sizeof BG));
    unsigned char C1[MAXN] = {0}, C2[MAXN] = {0}; int n1 = loadLetters(argv[2], C1, MAXN), n2 = strcmp(argv[3], "-") ? loadLetters(argv[3], C2, MAXN) : 0;
    CK(cudaMemcpyToSymbol(cC1, C1, MAXN)); CK(cudaMemcpyToSymbol(cC2, C2, MAXN));
    static int mine[MAXW1 + 1][MAXW1 + 1], maxe[MAXW1 + 1][MAXW1 + 1];
    for (int w = 2; w <= MAXW1; w++) geo(n1, w, mine[w], maxe[w]);
    CK(cudaMemcpyToSymbol(cMine, mine, sizeof mine)); CK(cudaMemcpyToSymbol(cMaxe, maxe, sizeof maxe));
    float *dQG; CK(cudaMalloc(&dQG, 456976 * 4)); CK(cudaMemcpy(dQG, QG.data(), 456976 * 4, cudaMemcpyHostToDevice));
    const int B = 1 << 16; unsigned char *dP, *dW; float *dRaw; Hit *dH; int *dN; unsigned int *dHist;
    CK(cudaMalloc(&dP, (size_t)B * MAXW)); CK(cudaMalloc(&dW, B)); CK(cudaMalloc(&dRaw, (size_t)B * nW1 * 4));
    const int MAXH = 1 << 20; CK(cudaMalloc(&dH, MAXH * sizeof(Hit))); CK(cudaMalloc(&dN, 4)); CK(cudaMalloc(&dHist, 12 * 4));
    CK(cudaMemset(dN, 0, 4)); CK(cudaMemset(dHist, 0, 48));
    std::vector<unsigned char> hP((size_t)B * MAXW), hW(B);
    // lignes de base : 200 clés aléatoires par largeur w2 (IDP pour chaque w1) et 300 par largeur (clé unique)
    std::mt19937 rng(12345); float mu[MAXW1 + 1][MAXW + 1] = {{0}}, sd[MAXW1 + 1][MAXW + 1] = {{0}}, smu[MAXW + 1] = {0}, ssd[MAXW + 1] = {0};
    for (int w2 = lo; w2 <= hi; w2++) {
        int R = 300;
        for (int r = 0; r < R; r++) { unsigned char *p = &hP[(size_t)r * MAXW]; for (int i = 0; i < w2; i++) p[i] = i; std::shuffle(p, p + w2, rng); hW[r] = w2; }
        CK(cudaMemcpy(dP, hP.data(), (size_t)R * MAXW, cudaMemcpyHostToDevice)); CK(cudaMemcpy(dW, hW.data(), R, cudaMemcpyHostToDevice));
        idpKernel<<<dim3(R, nW1), 128>>>(dP, dW, R, w1a, n1, dH, dN, MAXH, dHist, zrec, dRaw); CK(cudaGetLastError());
        std::vector<float> raw((size_t)R * nW1); CK(cudaMemcpy(raw.data(), dRaw, raw.size() * 4, cudaMemcpyDeviceToHost));
        for (int j = 0; j < nW1; j++) { double s = 0, ss = 0; for (int r = 0; r < R; r++) { double v = raw[(size_t)r * nW1 + j]; s += v; ss += v * v; }
            mu[w1a + j][w2] = (float)(s / R); sd[w1a + j][w2] = (float)sqrt(ss / R - (s / R) * (s / R)); }
        sameKernel<<<R, 128>>>(dP, dW, R, n1, n2, dQG, dH, dN, MAXH, dHist, zrec, dRaw); CK(cudaGetLastError());
        std::vector<float> rs(R); CK(cudaMemcpy(rs.data(), dRaw, R * 4, cudaMemcpyDeviceToHost));
        double s = 0, ss = 0; for (int r = 0; r < R; r++) { s += rs[r]; ss += rs[r] * rs[r]; } smu[w2] = (float)(s / R); ssd[w2] = (float)sqrt(ss / R - (s / R) * (s / R));
    }
    CK(cudaMemcpyToSymbol(cMu, mu, sizeof mu)); CK(cudaMemcpyToSymbol(cSd, sd, sizeof sd)); CK(cudaMemcpyToSymbol(cSMu, smu, sizeof smu)); CK(cudaMemcpyToSymbol(cSSd, ssd, sizeof ssd));
    fprintf(stderr, "lignes de base faites\n");
    // balayage
    FILE *fk = fopen(argv[4], "r"); if (!fk) { fprintf(stderr, "clés ?\n"); return 1; }
    std::vector<std::string> batch, allkeys; char line[512]; long nkeys = 0, ntrials = 0; cudaEvent_t e0, e1; cudaEventCreate(&e0); cudaEventCreate(&e1); cudaEventRecord(e0);
    std::vector<Hit> keep; std::vector<std::string> keepKeys;
    auto flush = [&]() {
        int nb = (int)batch.size(); if (!nb) return; int nk = nb * nvar;
        for (int i = 0; i < nb; i++) for (int v = 0; v < nvar; v++) { int idx = i * nvar + v; keyPerm(batch[i], v, &hP[(size_t)idx * MAXW]); hW[idx] = (unsigned char)batch[i].size(); }
        CK(cudaMemcpy(dP, hP.data(), (size_t)nk * MAXW, cudaMemcpyHostToDevice)); CK(cudaMemcpy(dW, hW.data(), nk, cudaMemcpyHostToDevice));
        CK(cudaMemset(dN, 0, 4));
        idpKernel<<<dim3(nk, nW1), 128>>>(dP, dW, nk, w1a, n1, dH, dN, MAXH, dHist, zrec, nullptr); CK(cudaGetLastError());
        sameKernel<<<nk, 128>>>(dP, dW, nk, n1, n2, dQG, dH, dN, MAXH, dHist, zrec, nullptr); CK(cudaGetLastError());
        int nh; CK(cudaMemcpy(&nh, dN, 4, cudaMemcpyDeviceToHost)); if (nh > MAXH) nh = MAXH;
        std::vector<Hit> h(nh); if (nh) CK(cudaMemcpy(h.data(), dH, nh * sizeof(Hit), cudaMemcpyDeviceToHost));
        for (auto &x : h) { x.var = (char)(x.key % nvar); keepKeys.push_back(batch[x.key / nvar]); x.key = (int)keepKeys.size() - 1; keep.push_back(x); }
        nkeys += nb; ntrials += (long)nk * (nW1 + 1); batch.clear();
        if ((nkeys / nb) % 16 == 0) fprintf(stderr, "%ld clés\n", nkeys);
        if (keep.size() > 200000) { std::sort(keep.begin(), keep.end(), [](const Hit &a, const Hit &b) { return a.z > b.z; }); keep.resize(50000); }
    };
    while (fgets(line, sizeof line, fk)) {
        std::string k; for (char *c = line; *c; c++) if (*c >= 'a' && *c <= 'z') k += *c;
        if ((int)k.size() < lo || (int)k.size() > hi) continue;
        batch.push_back(k); if ((int)batch.size() * nvar >= B) flush();
    }
    flush(); fclose(fk); CK(cudaDeviceSynchronize()); cudaEventRecord(e1); cudaEventSynchronize(e1); float ms; cudaEventElapsedTime(&ms, e0, e1);
    unsigned int hist[12]; CK(cudaMemcpy(hist, dHist, 48, cudaMemcpyDeviceToHost));
    std::sort(keep.begin(), keep.end(), [](const Hit &a, const Hit &b) { return a.z > b.z; });
    printf("clés=%ld essais=%ld durée %.1f s (%.0f clés/s)  z>4 :", nkeys, ntrials, ms / 1000, nkeys / (ms / 1000));
    for (int b = 0; b < 12; b++) printf(" [%d,%d):%u", b + 4, b + 5, hist[b]); printf("\n");
    for (int i = 0; i < (int)keep.size() && i < top; i++)
        printf("%.2f %s w1=%d w2=%d var=%d %s\n", keep[i].z, keep[i].kind ? "CLE_UNIQUE" : "IDP", keep[i].w1, keep[i].w2, keep[i].var, keepKeys[keep[i].key].c_str());
    return 0;
}
