/* K16 — double transposition à grandes clés : attaque « diviser pour régner » de Lasry.
   Étape K2 : recuit sur la seconde clé, noté par l'IDP (potentiel de juxtaposition des colonnes, bigrammes allemands) ;
   étape K1 : recuit sur la première clé (quadrigrammes). Criblage des paires de largeurs par IDP normalisé (score z contre
   des clés aléatoires), option K16_SCREEN=Rs,Is,top.
   L'évaluation IDP (plages exactes de fin de colonne, fenêtre glissante, score de matrice par chaîne gloutonne) et le
   répertoire de mouvements sont réimplémentés en C d'après CrypPlugins/IDPAttack/IDPAnalyser.cs (CrypTool 2,
   https://github.com/CrypToolProject/CrypTool-2, licence Apache 2.0) ; méthode : Lasry, Kopal & Wacker, Cryptologia 38(3), 2014.
   Voir experiments/K16_double_lasry/PREREGISTRATION.md.
   Compilation multithreadée : gcc -O3 -march=native -flto -fopenmp -o k16 tools/k16_double_ct2.c -lm
   Régler le nombre de fils avec OMP_NUM_THREADS (par exemple 8 sur un appareil à huit cœurs).
   Usage : identique à k14_double_idp.c (ctrl / solve / null), avec ctrlpair pour
   tester une paire fixe de largeurs. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>

static float *QG; static double BG[26][26];
/* Chaque worker OpenMP garde son propre état pseudo-aléatoire. */
static _Thread_local unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static unsigned long long seed_for(unsigned long long x) {
    x += 0x9e3779b97f4a7c15ULL; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL; x ^= x >> 31; return x ? x : 1;
}
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }
static double T2A = 0.05, T2B = 0.002;
static double rnd01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
#define D 3

static void mapping(int n, int w, const int *perm, int *pos) {
    int h = n / w, r = n % w, start[64], k = 0;
    for (int j = 0; j < w; j++) { int col = perm[j]; start[col] = k; k += h + (col < r); }
    for (int i = 0; i < n; i++) pos[i] = start[i % w] + i / w;
}
static void encrypt2(const int *p, int n, int w1, const int *k1, int w2, const int *k2, int *c) {
    int p1[2048], p2[2048], t[2048]; mapping(n, w1, k1, p1); mapping(n, w2, k2, p2);
    for (int i = 0; i < n; i++) t[p1[i]] = p[i];
    for (int j = 0; j < n; j++) c[p2[j]] = t[j];
}
static void undo(const int *c, int n, int w, const int *k, int *t) { int p[2048]; mapping(n, w, k, p); for (int j = 0; j < n; j++) t[j] = c[p[j]]; }

static double quad(const int *p, int n) { double s = 0; for (int i = 0; i + 3 < n; i++) s += QG[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]; return s / (n - 3); }

/* IDP, portage fidèle de CrypTool 2 (IDPAnalyser.cs, Lasry) : plages exactes de fin de colonne, fenêtre glissante,
   puis score de matrice par chaîne gloutonne (chaque colonne a au plus un voisin gauche et un droit, sans cycle). */
static _Thread_local int MINE[64], MAXE[64], CURW = -1, CURN = -1;
static void colends(int n, int w) {
    int full = n / w, nl = n % w;
    for (int i = 0; i < w; i++) { MINE[i] = full * (i + 1) - 1; MAXE[i] = (i < nl) ? full * (i + 1) + i : MINE[i] + nl; }
    for (int i = 0; i < w; i++) {
        int idx = w - 1 - i;
        if (MAXE[idx] > n - 1 - full * i) MAXE[idx] = n - 1 - full * i;
        if (i < nl) { int v = n - 1 - full * i - i; if (MINE[idx] < v) MINE[idx] = v; }
        else { int v = MAXE[idx] - nl; if (MINE[idx] < v) MINE[idx] = v; }
    }
    CURW = w; CURN = n;
}
static double chain_score(double m[64][64], int d) {
    int left[64], right[64]; for (int i = 0; i < d; i++) left[i] = right[i] = -1;
    double sum = 0;
    for (int it = 1; it <= d; it++) {
        double best = -1e18; int b1 = -1, b2 = -1;
        for (int p1 = 0; p1 < d; p1++) {
            if (right[p1] != -1) continue;
            int head = p1;
            if (it != d) while (left[head] != -1) head = left[head];
            for (int p2 = 0; p2 < d; p2++) {
                if (left[p2] != -1 || (it != d && head == p2) || p1 == p2) continue;
                if (m[p1][p2] > best) { best = m[p1][p2]; b1 = p1; b2 = p2; }
            }
        }
        if (b1 != -1) { sum += best; left[b2] = b1; right[b1] = b2; }
    }
    return sum / d;
}
static double idp(const int *t, int n, int w1) {
    if (CURW != w1 || CURN != n) colends(n, w1);
    static _Thread_local double m[64][64]; int full = n / w1;
    for (int c1 = 0; c1 < w1; c1++) for (int c2 = 0; c2 < w1; c2++) {
        if (c1 == c2) { m[c1][c2] = -1e18; continue; }
        double best = -1e18;
        if (n % w1 == 0) {
            int p1 = MINE[c1], p2 = MINE[c2]; double s = 0;
            for (int l = 0; l < full; l++) s += BG[t[p1 - l]][t[p2 - l]];
            best = s;
        } else {
            int s1 = MINE[c1] - full + 1, s2 = MINE[c2] - full + 1, o1 = MAXE[c1] - MINE[c1], o2 = MAXE[c2] - MINE[c2];
            for (int pass = 0; pass < 2; pass++) {
                int omax = pass == 0 ? o2 : o1;
                for (int off = pass; off <= omax; off++) {
                    int p1 = s1 + (pass ? off : 0), p2 = s2 + (pass ? 0 : off); double s = 0; int a = p1, b = p2;
                    if (a < 0 || b < 0 || a + full > n || b + full > n) continue;
                    for (int i = 0; i < full; i++) s += BG[t[a + i]][t[b + i]];
                    if (s > best) best = s;
                    int q1 = a + full, q2 = b + full, k = 0;
                    while (q1 <= MAXE[c1] && q2 <= MAXE[c2]) { s += BG[t[q1]][t[q2]] - BG[t[a + k]][t[b + k]]; k++; q1++; q2++; if (s > best) best = s; }
                }
            }
        }
        m[c1][c2] = best / full;
    }
    return chain_score(m, w1);
}

static void randperm(int *p, int w) { for (int i = 0; i < w; i++) p[i] = i; for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), x = p[i]; p[i] = p[j]; p[j] = x; } }
static void mutate(int *k, int w) {
    int a = rint_(w), b = rint_(w); if (a == b) return;
    int mv = rint_(3);
    if (mv == 0) { int x = k[a]; k[a] = k[b]; k[b] = x; }
    else if (mv == 1) { if (a > b) { int x = a; a = b; b = x; } while (a < b) { int x = k[a]; k[a] = k[b]; k[b] = x; a++; b--; } }
    else { int v = k[a]; if (a < b) memmove(k + a, k + a + 1, sizeof(int) * (b - a)); else memmove(k + b + 1, k + b, sizeof(int) * (a - b)); k[b] = v; }
}
static void mutate_ct2(int *k, int w) {       /* répertoire de mouvements de CrypTool 2 */
    int r = rint_(100), tmp[64];
    if (r < 50) { int n = 1 + rint_(9); for (int i = 0; i < n; i++) { int a = rint_(w), b = rint_(w), x = k[a]; k[a] = k[b]; k[b] = x; } }
    else if (r < 70) { int n = 1 + rint_(2); for (int j = 0; j < n; j++) { int l = 1 + rint_(w - 1), f = rint_(w), t = (f + l + rint_(w - l > 0 ? w - l : 1)) % w;
                        for (int i = 0; i < l; i++) { int x = k[(f + i) % w]; k[(f + i) % w] = k[(t + i) % w]; k[(t + i) % w] = x; } } }
    else if (r < 90) { int l = 1 + rint_(w - 1), f = rint_(w), t = (f + 1 + rint_(w - 1)) % w; memcpy(tmp, k, sizeof(int) * w);
                        int t0 = (t - f + w) % w, nn = (t0 + l) % w; for (int i = 0; i < nn; i++) { int ff = (f + i) % w, tt = (((t0 + i) % nn) + f) % w; k[tt] = tmp[ff]; } }
    else { int p = 1 + rint_(w - 1); memcpy(tmp, k, sizeof(int) * w); memcpy(k, tmp + p, sizeof(int) * (w - p)); memcpy(k + w - p, tmp, sizeof(int) * p); }
}
static double stage2(const int *c, int n, int w1, int w2, int R, int I, int *bk2) {
    double best = -1e18; int best_r = INT_MAX; unsigned long long base_seed = rs;
    double *temps = malloc(sizeof(double) * (size_t)I);
    for (int it = 0; it < I; it++) temps[it] = T2A * pow(T2B / T2A, (double)it / I);
    #pragma omp parallel for schedule(static) if(R > 1)
    for (int r = 0; r < R; r++) {
        rs = seed_for(base_seed + (unsigned long long)r * 0x9e3779b97f4a7c15ULL);
        int k[64], q[64], t[2048], local_key[64]; double local_best = -1e18;
        randperm(k, w2); undo(c, n, w2, k, t); double cur = idp(t, n, w1);
        if (cur > local_best) { local_best = cur; memcpy(local_key, k, sizeof(int) * w2); }
        for (int it = 0; it < I; it++) {
            memcpy(q, k, sizeof(int) * w2); mutate_ct2(q, w2); undo(c, n, w2, q, t); double s = idp(t, n, w1);
            double T = temps[it];
            if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; memcpy(k, q, sizeof(int) * w2); if (cur > local_best) { local_best = cur; memcpy(local_key, k, sizeof(int) * w2); } }
        }
        #pragma omp critical(k16_stage2_best)
        if (local_best > best || (local_best == best && r < best_r)) { best = local_best; best_r = r; memcpy(bk2, local_key, sizeof(int) * w2); }
    }
    rs = seed_for(base_seed ^ 0x243f6a8885a308d3ULL);
    free(temps);
    return best;
}

/* Greedy K2 search: spend evaluations on full neighborhoods instead of long
   random annealing walks. This is a fast diagnostic/optimization variant. */
static void slide_one(int *k, int w, int from, int to) {
    int v = k[from];
    if (from < to) { memmove(k + from, k + from + 1, sizeof(int) * (to - from)); k[to] = v; }
    else if (from > to) { memmove(k + to + 1, k + to, sizeof(int) * (from - to)); k[to] = v; }
}
static double stage2_greedy(const int *c, int n, int w1, int w2, int R, int I, int *bk2) {
    (void)I;
    double global_best = -1e18;
    unsigned long long base_seed = rs;
    #pragma omp parallel for schedule(static) if(R > 1)
    for (int r = 0; r < R; r++) {
        rs = seed_for(base_seed + (unsigned long long)r * 0x9e3779b97f4a7c15ULL);
        int k[64], candidate[64], t[2048];
        randperm(k, w2);
        undo(c, n, w2, k, t);
        double current = idp(t, n, w1);
        for (int pass = 0; pass < 200; pass++) {
            double next = current;
            int next_key[64]; memcpy(next_key, k, sizeof(int) * w2);
            for (int a = 0; a < w2; a++) for (int b = a + 1; b < w2; b++) {
                memcpy(candidate, k, sizeof(int) * w2);
                int x = candidate[a]; candidate[a] = candidate[b]; candidate[b] = x;
                undo(c, n, w2, candidate, t);
                double s = idp(t, n, w1);
                if (s > next) { next = s; memcpy(next_key, candidate, sizeof(int) * w2); }
            }
            for (int a = 0; a < w2; a++) for (int b = 0; b < w2; b++) if (a != b) {
                memcpy(candidate, k, sizeof(int) * w2); slide_one(candidate, w2, a, b);
                undo(c, n, w2, candidate, t);
                double s = idp(t, n, w1);
                if (s > next) { next = s; memcpy(next_key, candidate, sizeof(int) * w2); }
            }
            if (next <= current + 1e-12) break;
            current = next; memcpy(k, next_key, sizeof(int) * w2);
        }
        #pragma omp critical(k16_stage2_greedy_best)
        if (current > global_best) { global_best = current; memcpy(bk2, k, sizeof(int) * w2); }
    }
    rs = seed_for(base_seed ^ 0x243f6a8885a308d3ULL);
    return global_best;
}
static double stage1(const int *t, int n, int w1, int R, int I, int *bk1, int *out) {
    double best = -1e18; int best_r = INT_MAX; unsigned long long base_seed = rs;
    double *temps = malloc(sizeof(double) * (size_t)I);
    for (int it = 0; it < I; it++) temps[it] = 0.3 * pow(0.005 / 0.3, (double)it / I);
    #pragma omp parallel for schedule(static) if(R > 1)
    for (int r = 0; r < R; r++) {
        rs = seed_for(base_seed + (unsigned long long)r * 0xbf58476d1ce4e5b9ULL);
        int k[64], q[64], p[2048], pos[2048], local_key[64], local_out[2048]; double local_best = -1e18;
        randperm(k, w1); mapping(n, w1, k, pos); for (int i = 0; i < n; i++) p[i] = t[pos[i]]; double cur = quad(p, n);
        if (cur > local_best) { local_best = cur; memcpy(local_key, k, sizeof(int) * w1); memcpy(local_out, p, sizeof(int) * n); }
        for (int it = 0; it < I; it++) {
            memcpy(q, k, sizeof(int) * w1); mutate(q, w1); mapping(n, w1, q, pos); for (int i = 0; i < n; i++) p[i] = t[pos[i]];
            double s = quad(p, n), T = temps[it];
            if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; memcpy(k, q, sizeof(int) * w1); if (cur > local_best) { local_best = cur; memcpy(local_key, k, sizeof(int) * w1); memcpy(local_out, p, sizeof(int) * n); } }
        }
        #pragma omp critical(k16_stage1_best)
        if (local_best > best || (local_best == best && r < best_r)) { best = local_best; best_r = r; memcpy(bk1, local_key, sizeof(int) * w1); memcpy(out, local_out, sizeof(int) * n); }
    }
    rs = seed_for(base_seed ^ 0x13198a2e03707344ULL);
    free(temps);
    return best;
}

/* Finalize K2 against the recovered K1, as in the published divide-and-conquer
   attack. Test whole-key swaps and single-column slides using the plaintext score. */
static double plaintext_score_k12(const int *c, int n, int w1, const int *k1,
                                  int w2, const int *k2, int *plain) {
    int t[2048], pos[2048];
    undo(c, n, w2, k2, t);
    mapping(n, w1, k1, pos);
    for (int i = 0; i < n; i++) plain[i] = t[pos[i]];
    return quad(plain, n);
}
static double polish_k2(const int *c, int n, int w1, int w2,
                        const int *k1, int *k2, int *plain) {
    int candidate[64], candidate_plain[2048];
    double current = plaintext_score_k12(c, n, w1, k1, w2, k2, plain);
    for (int pass = 0; pass < 100; pass++) {
        double next = current;
        int next_key[64], next_plain[2048];
        memcpy(next_key, k2, sizeof(int) * w2);
        memcpy(next_plain, plain, sizeof(int) * n);
        for (int a = 0; a < w2; a++) for (int b = a + 1; b < w2; b++) {
            memcpy(candidate, k2, sizeof(int) * w2);
            int x = candidate[a]; candidate[a] = candidate[b]; candidate[b] = x;
            double s = plaintext_score_k12(c, n, w1, k1, w2, candidate, candidate_plain);
            if (s > next) { next = s; memcpy(next_key, candidate, sizeof(int) * w2); memcpy(next_plain, candidate_plain, sizeof(int) * n); }
        }
        for (int a = 0; a < w2; a++) for (int b = 0; b < w2; b++) if (a != b) {
            memcpy(candidate, k2, sizeof(int) * w2); slide_one(candidate, w2, a, b);
            double s = plaintext_score_k12(c, n, w1, k1, w2, candidate, candidate_plain);
            if (s > next) { next = s; memcpy(next_key, candidate, sizeof(int) * w2); memcpy(next_plain, candidate_plain, sizeof(int) * n); }
        }
        if (next <= current + 1e-12) break;
        current = next; memcpy(k2, next_key, sizeof(int) * w2); memcpy(plain, next_plain, sizeof(int) * n);
    }
    return current;
}

/* recherche sur les paires de largeurs. Mode criblage (K16_SCREEN=Rs,Is,top) : passage rapide sur toutes les paires, puis
   recherche profonde (R2, I2) seulement sur les « top » paires au meilleur IDP. */
static double full(const int *c, int n, int wmin, int wmax, int kw1, int kw2, int R2, int I2, int R1, int I1,
                   int *bw1, int *bw2, int *bk1, int *bk2, int *bout) {
    double best = -1e18; int best_i = INT_MAX, k1[64], k2[64], t[2048], out[2048];
    unsigned long long base_seed = rs;
    int pw1[512], pw2[512], np = 0; double pid[512];
    for (int w1 = (kw1 ? kw1 : wmin); w1 <= (kw1 ? kw1 : wmax); w1++)
        for (int w2 = (kw2 ? kw2 : wmin); w2 <= (kw2 ? kw2 : wmax); w2++) { pw1[np] = w1; pw2[np] = w2; pid[np] = 0; np++; }
    int Rs = 0, Is = 0, top = np;
    if (getenv("K16_SCREEN")) sscanf(getenv("K16_SCREEN"), "%d,%d,%d", &Rs, &Is, &top);
    if (Rs > 0 && top < np) {
        unsigned long long call_seed = base_seed;
        #pragma omp parallel for schedule(dynamic,1) if(np > 1)
        for (int i = 0; i < np; i++) {
            rs = seed_for(call_seed + (unsigned long long)i * 0x9e3779b97f4a7c15ULL);
            /* normalisation : niveau de hasard de l'IDP pour cette paire de largeurs (40 clés K2 aléatoires) */
            double m = 0, m2 = 0; int rk[64], tt[2048];
            for (int r = 0; r < 40; r++) { randperm(rk, pw2[i]); undo(c, n, pw2[i], rk, tt); double v = idp(tt, n, pw1[i]); m += v; m2 += v * v; }
            m /= 40; double sd = sqrt(m2 / 40 - m * m) + 1e-9;
            pid[i] = (stage2(c, n, pw1[i], pw2[i], Rs, Is, k2) - m) / sd;
        }
        rs = base_seed;
        for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) if (pid[j] > pid[i]) {
            double x = pid[i]; pid[i] = pid[j]; pid[j] = x; int a = pw1[i]; pw1[i] = pw1[j]; pw1[j] = a; a = pw2[i]; pw2[i] = pw2[j]; pw2[j] = a; }
        if (getenv("K16_VERBOSE")) { fprintf(stderr, "criblage :"); for (int i = 0; i < 8 && i < np; i++) fprintf(stderr, " (%d,%d)%.3f", pw1[i], pw2[i], pid[i]); fprintf(stderr, "\n"); }
        np = top;
    }
    unsigned long long call_seed = seed_for(base_seed ^ 0xd1b54a32d192ed03ULL);
    #pragma omp parallel for schedule(dynamic,1) if(np > 1)
    for (int i = 0; i < np; i++) {
        unsigned long long candidate_seed = seed_for(call_seed + (unsigned long long)(i + 512) * 0x9e3779b97f4a7c15ULL);
        rs = candidate_seed;
        int w1 = pw1[i], w2 = pw2[i];
        int k1[64], k2[64], t[2048], out[2048];
        if (getenv("K16_IDP_GREEDY")) stage2_greedy(c, n, w1, w2, R2, I2, k2);
        else stage2(c, n, w1, w2, R2, I2, k2);
        undo(c, n, w2, k2, t);
        rs = seed_for(candidate_seed ^ 0xa4093822299f31d0ULL);
        double s = stage1(t, n, w1, R1, I1, k1, out);
        if (getenv("K16_K2_POLISH")) {
            double polished = polish_k2(c, n, w1, w2, k1, k2, out);
            if (polished > s) s = polished;
        }
        #pragma omp critical(k16_best)
        if (s > best || (s == best && i < best_i)) { best = s; best_i = i; *bw1 = w1; *bw2 = w2; memcpy(bk1, k1, sizeof k1); memcpy(bk2, k2, sizeof k2); memcpy(bout, out, sizeof(int) * n); }
    }
    rs = seed_for(base_seed ^ 0x94d049bb133111ebULL);
    return best;
}

static int load_letters(const char *s, int *out, int max) {
    int n = 0; for (; *s && n < max; s++) if (*s >= 'a' && *s <= 'z') out[n++] = *s - 'a'; else if (*s >= 'A' && *s <= 'Z') out[n++] = *s - 'A';
    return n;
}
static int load_letters_file(const char *path, int *out, int max) {
    FILE *f = fopen(path, "rb");
    if (!f) { perror(path); return -1; }
    int n = 0, ch;
    while ((ch = fgetc(f)) != EOF && n < max) {
        if (ch >= 'a' && ch <= 'z') out[n++] = ch - 'a';
        else if (ch >= 'A' && ch <= 'Z') out[n++] = ch - 'A';
    }
    fclose(f);
    return n;
}

int main(int argc, char **argv) {
    if (argc < 4) return 1;
    if (getenv("K14_T2A")) T2A = atof(getenv("K14_T2A")); if (getenv("K14_T2B")) T2B = atof(getenv("K14_T2B"));
    QG = malloc(sizeof(float) * 456976); FILE *fp = fopen(argv[2], "rb");
    if (!fp || fread(QG, sizeof(float), 456976, fp) != 456976) { fprintf(stderr, "qg ?\n"); return 1; } fclose(fp);
    for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double s = 0; for (int c = 0; c < 676; c++) s += exp(QG[(a * 26 + b) * 676 + c]); BG[a][b] = log(s); }
    if (getenv("DCT_PMI")) {   /* information mutuelle ponctuelle : log P(ab) − log P(a)·P(b) */
        double U[26] = {0}, V[26] = {0}, tot = 0;
        for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double e = exp(BG[a][b]); U[a] += e; V[b] += e; tot += e; }
        for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) BG[a][b] = BG[a][b] - log(U[a] / tot) - log(V[b] / tot) - log(tot);
    }
    if (!strcmp(argv[1], "solvepair")) {
        if (argc < 11) { fprintf(stderr, "solvepair: model cipher w1 w2 R2 I2 R1 I1 seed\n"); return 1; }
        int c[2048], n = load_letters_file(argv[3], c, 2048);
        if (n < 4) { fprintf(stderr, "cipher file unreadable or too short\n"); return 1; }
        int w1 = atoi(argv[4]), w2 = atoi(argv[5]);
        int R2 = atoi(argv[6]), I2 = atoi(argv[7]), R1 = atoi(argv[8]), I1 = atoi(argv[9]);
        rs = strtoull(argv[10], 0, 10) * 2654435761ULL + 43;
        int bw1, bw2, k1[64], k2[64], out[2048];
        double score = full(c, n, w1, w1, w1, w2, R2, I2, R1, I1, &bw1, &bw2, k1, k2, out);
        printf("PAIR w1=%d w2=%d score=%.6f\nTEXT ", w1, w2, score);
        for (int i = 0; i < n; i++) putchar('a' + out[i]);
        putchar('\n');
        printf("K1"); for (int i = 0; i < w1; i++) printf(" %d", k1[i]);
        printf("\nK2"); for (int i = 0; i < w2; i++) printf(" %d", k2[i]);
        putchar('\n');
        return 0;
    }
    if (!strcmp(argv[1], "stream")) {
        /* stream : model cipher keys.txt wmin wmax top — attaque par dictionnaire en flux (des millions de clés).
           Une clé par ligne (lettres a–z) ; K2 = clé (rang alphabétique, ex aequo de gauche à droite, convention 0) ;
           w2 = longueur de la clé dans [wmin,wmax] ; w1 parcourt [wmin,wmax], w1 ≠ w2 et pgcd(w1,w2) = 1.
           Sortie : histogramme des IDP et les « top » meilleurs (clé, w1, IDP). */
        int c[2048], n = load_letters_file(argv[3], c, 2048); FILE *fd = fopen(argv[4], "r");
        if (n < 4 || !fd) { fprintf(stderr, "stream: model cipher keys wmin wmax top\n"); return 1; }
        int wmin = atoi(argv[5]), wmax = atoi(argv[6]), top = atoi(argv[7]);
        typedef struct { double s; int w1; char k[64]; } H; H *best = calloc(top, sizeof(H)); int nb = 0; double bmin = -1e9;
        long hist[200] = {0}, cnt = 0, nkeys = 0; enum { CH = 65536 }; static char buf[CH][64]; int m;
        do {
            m = 0; char line[512];
            while (m < CH && fgets(line, sizeof line, fd)) { int L = 0; for (char *x = line; *x && L < 63; x++) { char ch = *x | 32; if (ch >= 'a' && ch <= 'z') buf[m][L++] = ch; } buf[m][L] = 0; if (L >= wmin && L <= wmax) m++; }
            nkeys += m;
            #pragma omp parallel for schedule(dynamic, 256)
            for (int q = 0; q < m; q++) {
                int L = strlen(buf[q]), rank[64], ord[64], t[2048];
                for (int i = 0; i < L; i++) { rank[i] = 0; for (int j = 0; j < L; j++) if (buf[q][j] < buf[q][i] || (buf[q][j] == buf[q][i] && j < i)) rank[i]++; }
                for (int i = 0; i < L; i++) ord[rank[i]] = i;
                undo(c, n, L, ord, t);
                for (int w1 = wmin; w1 <= wmax; w1++) {
                    int a = w1, b = L; while (b) { int r = a % b; a = b; b = r; } if (w1 == L || a != 1) continue;
                    double sc = idp(t, n, w1); int hb = (int)(sc * 400) + 40; if (hb < 0) hb = 0; if (hb > 199) hb = 199;
                    #pragma omp atomic
                    hist[hb]++;
                    #pragma omp atomic
                    cnt++;
                    if (sc > bmin || nb < top) {
                        #pragma omp critical(stream_best)
                        { if (nb < top) { best[nb].s = sc; best[nb].w1 = w1; strcpy(best[nb].k, buf[q]); nb++; if (nb == top) { bmin = 1e9; for (int i = 0; i < nb; i++) if (best[i].s < bmin) bmin = best[i].s; } }
                          else if (sc > bmin) { int mi = 0; for (int i = 1; i < nb; i++) if (best[i].s < best[mi].s) mi = i;
                                 best[mi].s = sc; best[mi].w1 = w1; strcpy(best[mi].k, buf[q]); bmin = 1e9; for (int i = 0; i < nb; i++) if (best[i].s < bmin) bmin = best[i].s; } }
                    }
                }
            }
        } while (m == CH);
        fclose(fd);
        for (int i = 0; i < nb; i++) for (int j = i + 1; j < nb; j++) if (best[j].s > best[i].s) { H x = best[i]; best[i] = best[j]; best[j] = x; }
        printf("clés=%ld essais=%ld\nhistogramme IDP (pas 0,0025) :", nkeys, cnt);
        for (int i = 0; i < 200; i++) if (hist[i]) printf(" %.4f:%ld", (i - 40) / 400.0, hist[i]); printf("\n");
        for (int i = 0; i < nb; i++) printf("%.5f w1=%d w2=%d %s\n", best[i].s, best[i].w1, (int)strlen(best[i].k), best[i].k);
        return 0;
    }
    if (!strcmp(argv[1], "withk2")) {
        /* withk2 : model cipher "phrase K2" w1 R1 I1 seed — K2 donnée par une phrase, K1 par recuit (quadrigrammes). */
        int c[2048], n = load_letters_file(argv[3], c, 2048); int L = 0, key[64]; char *x = argv[4];
        for (; *x && L < 63; x++) { char ch = *x | 32; if (ch >= 'a' && ch <= 'z') key[L++] = ch; }
        int rank[64], ord[64]; for (int i = 0; i < L; i++) { rank[i] = 0; for (int j = 0; j < L; j++) if (key[j] < key[i] || (key[j] == key[i] && j < i)) rank[i]++; }
        for (int i = 0; i < L; i++) ord[rank[i]] = i;
        int w1 = atoi(argv[5]), R1 = atoi(argv[6]), I1 = atoi(argv[7]); rs = strtoull(argv[8], 0, 10) * 2654435761ULL + 7;
        int t[2048], k1[64], out[2048]; undo(c, n, L, ord, t);
        double s = stage1(t, n, w1, R1, I1, k1, out);
        printf("w2=%d w1=%d score=%.4f\nTEXT ", L, w1, s); for (int i = 0; i < n; i++) putchar('a' + out[i]);
        printf("\nK1 (ordre de lecture des colonnes)"); for (int i = 0; i < w1; i++) printf(" %d", k1[i]); putchar('\n');
        return 0;
    }
    if (!strcmp(argv[1], "dict")) {
        /* dict : model cipher phrases.txt w1min w1max top — attaque par dictionnaire de phrases sur K2 (IDP).
           Clé tirée d'une phrase : lettres a–z seules, rang alphabétique, ex aequo de gauche à droite ;
           les deux conventions de lecture (ordre des rangs ou rangs eux-mêmes) sont essayées. */
        int c[2048], n = load_letters_file(argv[3], c, 2048); FILE *fd = fopen(argv[4], "r");
        if (n < 4 || !fd) { fprintf(stderr, "dict: model cipher phrases w1min w1max top\n"); return 1; }
        int w1min = atoi(argv[5]), w1max = atoi(argv[6]), top = atoi(argv[7]);
        char line[4096]; typedef struct { double s; int w1, conv; char ph[200]; } H; H best[64]; int nb = 0; long cnt = 0;
        char *phr[200000]; int np = 0;
        while (fgets(line, sizeof line, fd) && np < 200000) { line[strcspn(line, "\r\n")] = 0; phr[np++] = strdup(line); }
        fclose(fd);
        #pragma omp parallel for schedule(dynamic, 64)
        for (int q = 0; q < np; q++) {
            int L = 0; char key[256]; for (char *x = phr[q]; *x && L < 255; x++) { char ch = *x | 32; if (ch >= 'a' && ch <= 'z') key[L++] = ch; }
            if (L < 2 || L > 63) continue;
            int rank[64], ord[64]; for (int i = 0; i < L; i++) { rank[i] = 0; for (int j = 0; j < L; j++) if (key[j] < key[i] || (key[j] == key[i] && j < i)) rank[i]++; }
            for (int i = 0; i < L; i++) ord[rank[i]] = i;
            int t[2048];
            for (int conv = 0; conv < 2; conv++) {
                undo(c, n, L, conv ? rank : ord, t);
                for (int w1 = w1min; w1 <= w1max; w1++) {
                    double s = idp(t, n, w1);
                    #pragma omp critical(dict_best)
                    { cnt++;
                      if (nb < top) { best[nb].s = s; best[nb].w1 = w1; best[nb].conv = conv; snprintf(best[nb].ph, 200, "%s", phr[q]); nb++; }
                      else { int mi = 0; for (int i = 1; i < nb; i++) if (best[i].s < best[mi].s) mi = i;
                             if (s > best[mi].s) { best[mi].s = s; best[mi].w1 = w1; best[mi].conv = conv; snprintf(best[mi].ph, 200, "%s", phr[q]); } } }
                }
            }
        }
        for (int i = 0; i < nb; i++) for (int j = i + 1; j < nb; j++) if (best[j].s > best[i].s) { H x = best[i]; best[i] = best[j]; best[j] = x; }
        printf("phrases=%d essais=%ld\n", np, cnt);
        for (int i = 0; i < nb; i++) printf("%.5f w1=%d conv=%d  %s\n", best[i].s, best[i].w1, best[i].conv, best[i].ph);
        return 0;
    }
    if (!strcmp(argv[1], "ctrlpair")) {
        if (argc < 12) { fprintf(stderr, "ctrlpair: model plain n w1 w2 R2 I2 R1 I1 seed\n"); return 1; }
        fp = fopen(argv[3], "rb"); if (!fp) { fprintf(stderr, "plain ?\n"); return 1; }
        fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *tx = malloc(L + 1); if (fread(tx, 1, L, fp) != (size_t)L) return 2; tx[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(tx, txt, L);
        int ne = atoi(argv[4]), w1 = atoi(argv[5]), w2 = atoi(argv[6]);
        int R2 = atoi(argv[7]), I2 = atoi(argv[8]), R1 = atoi(argv[9]), I1 = atoi(argv[10]);
        rs = strtoull(argv[11], 0, 10) * 2654435761ULL + 47; int n = getenv("DCT_N") ? atoi(getenv("DCT_N")) : 979, ok = 0;
        for (int e = 0; e < ne; e++) {
            int p[2048], c[2048], k1[64], k2[64], b1[64], b2[64], out[2048], bw1, bw2;
            int idx[2048], cidx[2048], t[2048], pos[2048], oidx[2048];
            int o = rint_(M - n); memcpy(p, txt + o, sizeof(int) * n);
            randperm(k1, w1); randperm(k2, w2); encrypt2(p, n, w1, k1, w2, k2, c);
            double s = full(c, n, w1, w1, w1, w2, R2, I2, R1, I1, &bw1, &bw2, b1, b2, out);
            int match1 = 0, match2 = 0; for (int j = 0; j < w1; j++) match1 += b1[j] == k1[j];
            for (int j = 0; j < w2; j++) match2 += b2[j] == k2[j];
            undo(c, n, w2, k2, t); double true_idp = idp(t, n, w1);
            undo(c, n, bw2, b2, t); double found_idp = idp(t, n, bw1);
            for (int i = 0; i < n; i++) idx[i] = i;
            encrypt2(idx, n, w1, k1, w2, k2, cidx); undo(cidx, n, bw2, b2, t); mapping(n, bw1, b1, pos);
            for (int i = 0; i < n; i++) oidx[i] = t[pos[i]];
            int good = 0; for (int i = 0; i + 1 < n; i++) good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1;
            int k2ok = bw2 == w2; for (int j = 0; j < w2 && k2ok; j++) if (b2[j] != k2[j]) k2ok = 0;
            ok += good >= 0.9 * (n - 1);
            printf("essai %d : w=%d,%d K2 %s score=%.4f (vrai %.4f) contacts=%d/%d\n", e, w1, w2, k2ok ? "exacte" : "fausse", s, quad(p, n), good, n - 1);
            printf("  K2 exact-position matches=%d/%d; K1=%d/%d; IDP true=%.6f found=%.6f\n", match2, w2, match1, w1, true_idp, found_idp);
            fflush(stdout);
        }
        printf("SUCCES %d/%d (w=%d,%d, R2=%d I2=%d R1=%d I1=%d)\n", ok, ne, w1, w2, R2, I2, R1, I1);
        return 0;
    }
    if (!strcmp(argv[1], "ctrlrep")) {
        if (argc < 12) { fprintf(stderr, "ctrlrep: model plain wmin wmax R2 I2 R1 I1 control_seed search_seed\n"); return 1; }
        fp = fopen(argv[3], "rb"); if (!fp) { fprintf(stderr, "plain ?\n"); return 1; }
        fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *tx = malloc(L + 1); if (fread(tx, 1, L, fp) != (size_t)L) return 2; tx[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(tx, txt, L);
        int wmin = atoi(argv[4]), wmax = atoi(argv[5]);
        int R2 = atoi(argv[6]), I2 = atoi(argv[7]), R1 = atoi(argv[8]), I1 = atoi(argv[9]);
        unsigned long long control_seed = strtoull(argv[10], 0, 10), search_seed = strtoull(argv[11], 0, 10);
        int n = getenv("DCT_N") ? atoi(getenv("DCT_N")) : 979, p[2048], c[2048], k1[64], k2[64], b1[64], b2[64], out[2048], bw1, bw2;
        rs = control_seed * 2654435761ULL + 41;
        int o = rint_(M - n); memcpy(p, txt + o, sizeof(int) * n);
        int w1 = wmin + rint_(wmax - wmin + 1), w2 = wmin + rint_(wmax - wmin + 1);
        randperm(k1, w1); randperm(k2, w2); encrypt2(p, n, w1, k1, w2, k2, c);
        rs = search_seed * 2654435761ULL + 53;
        double s = full(c, n, wmin, wmax, 0, 0, R2, I2, R1, I1, &bw1, &bw2, b1, b2, out);
        int idx[2048], cidx[2048], t[2048], pos[2048], oidx[2048];
        for (int i = 0; i < n; i++) idx[i] = i;
        encrypt2(idx, n, w1, k1, w2, k2, cidx); undo(cidx, n, bw2, b2, t); mapping(n, bw1, b1, pos);
        int good = 0; for (int i = 0; i < n; i++) oidx[i] = t[pos[i]];
        for (int i = 0; i + 1 < n; i++) good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1;
        int ok = good >= 0.9 * (n - 1);
        printf("CTRL control_seed=%llu search_seed=%llu planted=%d,%d found=%d,%d score=%.4f contacts=%d/%d\n",
               control_seed, search_seed, w1, w2, bw1, bw2, s, good, n - 1);
        printf("SUCCES %d/1 (w=%d..%d, R2=%d I2=%d R1=%d I1=%d)\n", ok, wmin, wmax, R2, I2, R1, I1);
        return 0;
    }
    if (!strcmp(argv[1], "ctrl")) {
        fp = fopen(argv[3], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *tx = malloc(L + 1); if (fread(tx, 1, L, fp) != (size_t)L) return 2; tx[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(tx, txt, L);
        int ne = atoi(argv[4]), wmin = atoi(argv[5]), wmax = atoi(argv[6]), known = atoi(argv[7]);
        int R2 = atoi(argv[8]), I2 = atoi(argv[9]), R1 = atoi(argv[10]), I1 = atoi(argv[11]); rs = strtoull(argv[12], 0, 10) * 2654435761ULL + 41;
        int n = getenv("DCT_N") ? atoi(getenv("DCT_N")) : 979, ok = 0;
        for (int e = 0; e < ne; e++) {
            int p[2048], c[2048], k1[64], k2[64], b1[64], b2[64], out[2048], bw1, bw2, idx[2048], cidx[2048], t[2048], oidx[2048], pos[2048];
            int o = rint_(M - n); memcpy(p, txt + o, sizeof(int) * n);
            int w1 = wmin + rint_(wmax - wmin + 1), w2 = wmin + rint_(wmax - wmin + 1); randperm(k1, w1); randperm(k2, w2);
            encrypt2(p, n, w1, k1, w2, k2, c);
            double s = full(c, n, wmin, wmax, known ? w1 : 0, known ? w2 : 0, R2, I2, R1, I1, &bw1, &bw2, b1, b2, out);
            for (int i = 0; i < n; i++) idx[i] = i;
            encrypt2(idx, n, w1, k1, w2, k2, cidx); undo(cidx, n, bw2, b2, t); mapping(n, bw1, b1, pos);
            for (int i = 0; i < n; i++) oidx[i] = t[pos[i]];
            int good = 0; for (int i = 0; i + 1 < n; i++) good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1;
            int k2ok = 1; for (int j = 0; j < w2 && bw2 == w2; j++) if (b2[j] != k2[j]) k2ok = 0;
            ok += good >= 0.9 * (n - 1);
            printf("essai %d : vrai w=%d,%d | trouvé w=%d,%d K2 %s score=%.4f (vrai %.4f) contacts=%d/%d\n", e, w1, w2, bw1, bw2,
                   (bw2 == w2 && k2ok) ? "exacte" : "fausse", s, quad(p, n), good, n - 1);
            fflush(stdout);
        }
        printf("SUCCES %d/%d (w=%d..%d, largeurs %s, R2=%d I2=%d R1=%d I1=%d)\n", ok, ne, wmin, wmax, known ? "connues" : "cherchées", R2, I2, R1, I1);
    } else {
        int c[2048], n = load_letters_file(argv[3], c, 2048), isnull = !strcmp(argv[1], "null"), a = isnull ? 5 : 4;
        if (n < 4) { fprintf(stderr, "cipher file unreadable or too short\n"); return 1; }
        int nn = isnull ? atoi(argv[4]) : 1, wmin = atoi(argv[a]), wmax = atoi(argv[a + 1]);
        int R2 = atoi(argv[a + 2]), I2 = atoi(argv[a + 3]), R1 = atoi(argv[a + 4]), I1 = atoi(argv[a + 5]); rs = strtoull(argv[a + 6], 0, 10) * 2654435761ULL + 43;
        for (int k = 0; k < nn; k++) {
            int cc[2048], b1[64], b2[64], out[2048], bw1, bw2; memcpy(cc, c, sizeof(int) * n);
            if (isnull) for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), x = cc[i]; cc[i] = cc[j]; cc[j] = x; }
            double s = full(cc, n, wmin, wmax, 0, 0, R2, I2, R1, I1, &bw1, &bw2, b1, b2, out);
            printf("%s %d score=%.4f w=%d,%d ", isnull ? "NUL" : "REEL", k, s, bw1, bw2);
            for (int i = 0; i < n; i++) putchar('a' + out[i]);
            putchar('\n'); fflush(stdout);
        }
    }
    return 0;
}
