/* K14 — double transposition à grandes clés : recuit sur K2 noté par le potentiel de juxtaposition des colonnes (IDP, bigrammes
   allemands), puis recuit sur K1 (quadrigrammes). Voir experiments/K14_double_grandes_cles/PREREGISTRATION.md.
   Compilation : gcc -O2 -o k14 tools/k14_double_idp.c -lm
   Usage :
     k14 ctrl  <qg.bin> <texte_reserve> <nessais> <wmin> <wmax> <connues 0/1> <R2> <I2> <R1> <I1> <graine>
     k14 solve <qg.bin> <lettres> <wmin> <wmax> <R2> <I2> <R1> <I1> <graine>
     k14 null  <qg.bin> <lettres> <nnull> <wmin> <wmax> <R2> <I2> <R1> <I1> <graine> */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static float *QG; static double BG[26][26];
static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
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

/* potentiel de juxtaposition de T découpé (estimation) en w1 colonnes */
static double idp(const int *t, int n, int w1) {
    int h = n / w1, r = n % w1, st[64];
    for (int j = 0; j < w1; j++) st[j] = j * h + (int)lround((double)j * r / w1);
    double tot = 0;
    for (int a = 0; a < w1; a++) {
        double best = -1e18;
        for (int b = 0; b < w1; b++) {
            if (a == b) continue;
            for (int d = -D; d <= D; d++) {
                int sb = st[b] + d; if (sb < 0 || sb + h > n) continue;
                double s = 0; const int *x = t + st[a], *y = t + sb;
                for (int row = 0; row < h; row++) s += BG[x[row]][y[row]];
                if (s > best) best = s;
            }
        }
        tot += best / h;
    }
    return tot / w1;
}

static void randperm(int *p, int w) { for (int i = 0; i < w; i++) p[i] = i; for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), x = p[i]; p[i] = p[j]; p[j] = x; } }
static void mutate(int *k, int w) {
    int a = rint_(w), b = rint_(w); if (a == b) return;
    int mv = rint_(3);
    if (mv == 0) { int x = k[a]; k[a] = k[b]; k[b] = x; }
    else if (mv == 1) { if (a > b) { int x = a; a = b; b = x; } while (a < b) { int x = k[a]; k[a] = k[b]; k[b] = x; a++; b--; } }
    else { int v = k[a]; if (a < b) memmove(k + a, k + a + 1, sizeof(int) * (b - a)); else memmove(k + b + 1, k + b, sizeof(int) * (a - b)); k[b] = v; }
}

static double stage2(const int *c, int n, int w1, int w2, int R, int I, int *bk2) {
    int k[64], q[64], t[2048]; double best = -1e18;
    for (int r = 0; r < R; r++) {
        randperm(k, w2); undo(c, n, w2, k, t); double cur = idp(t, n, w1);
        for (int it = 0; it < I; it++) {
            memcpy(q, k, sizeof(int) * w2); mutate(q, w2); undo(c, n, w2, q, t); double s = idp(t, n, w1);
            double T = T2A * pow(T2B / T2A, (double)it / I);
            if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; memcpy(k, q, sizeof(int) * w2); if (cur > best) { best = cur; memcpy(bk2, k, sizeof(int) * w2); } }
        }
    }
    return best;
}
static double stage1(const int *t, int n, int w1, int R, int I, int *bk1, int *out) {
    int k[64], q[64], p[2048], pos[2048]; double best = -1e18;
    for (int r = 0; r < R; r++) {
        randperm(k, w1); mapping(n, w1, k, pos); for (int i = 0; i < n; i++) p[i] = t[pos[i]]; double cur = quad(p, n);
        for (int it = 0; it < I; it++) {
            memcpy(q, k, sizeof(int) * w1); mutate(q, w1); mapping(n, w1, q, pos); for (int i = 0; i < n; i++) p[i] = t[pos[i]];
            double s = quad(p, n), T = 0.3 * pow(0.005 / 0.3, (double)it / I);
            if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; memcpy(k, q, sizeof(int) * w1); if (cur > best) { best = cur; memcpy(bk1, k, sizeof(int) * w1); memcpy(out, p, sizeof(int) * n); } }
        }
    }
    return best;
}

/* recherche complète sur les paires de largeurs ; renvoie le meilleur score final (quadrigrammes) */
static double full(const int *c, int n, int wmin, int wmax, int kw1, int kw2, int R2, int I2, int R1, int I1,
                   int *bw1, int *bw2, int *bk1, int *bk2, int *bout) {
    double best = -1e18; int k1[64], k2[64], t[2048], out[2048];
    for (int w1 = (kw1 ? kw1 : wmin); w1 <= (kw1 ? kw1 : wmax); w1++)
        for (int w2 = (kw2 ? kw2 : wmin); w2 <= (kw2 ? kw2 : wmax); w2++) {
            stage2(c, n, w1, w2, R2, I2, k2); undo(c, n, w2, k2, t);
            double s = stage1(t, n, w1, R1, I1, k1, out);
            if (s > best) { best = s; *bw1 = w1; *bw2 = w2; memcpy(bk1, k1, sizeof k1); memcpy(bk2, k2, sizeof k2); memcpy(bout, out, sizeof(int) * n); }
        }
    return best;
}

static int load_letters(const char *s, int *out, int max) {
    int n = 0; for (; *s && n < max; s++) if (*s >= 'a' && *s <= 'z') out[n++] = *s - 'a'; else if (*s >= 'A' && *s <= 'Z') out[n++] = *s - 'A';
    return n;
}

int main(int argc, char **argv) {
    if (argc < 4) return 1;
    if (getenv("K14_T2A")) T2A = atof(getenv("K14_T2A")); if (getenv("K14_T2B")) T2B = atof(getenv("K14_T2B"));
    QG = malloc(sizeof(float) * 456976); FILE *fp = fopen(argv[2], "rb");
    if (!fp || fread(QG, sizeof(float), 456976, fp) != 456976) { fprintf(stderr, "qg ?\n"); return 1; } fclose(fp);
    for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double s = 0; for (int c = 0; c < 676; c++) s += exp(QG[(a * 26 + b) * 676 + c]); BG[a][b] = log(s); }
    if (!strcmp(argv[1], "ctrl")) {
        fp = fopen(argv[3], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *tx = malloc(L + 1); if (fread(tx, 1, L, fp) != (size_t)L) return 2; tx[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(tx, txt, L);
        int ne = atoi(argv[4]), wmin = atoi(argv[5]), wmax = atoi(argv[6]), known = atoi(argv[7]);
        int R2 = atoi(argv[8]), I2 = atoi(argv[9]), R1 = atoi(argv[10]), I1 = atoi(argv[11]); rs = strtoull(argv[12], 0, 10) * 2654435761ULL + 41;
        int n = 979, ok = 0;
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
        int c[2048], n = load_letters(argv[3], c, 2048), isnull = !strcmp(argv[1], "null"), a = isnull ? 5 : 4;
        int nn = isnull ? atoi(argv[4]) : 1, wmin = atoi(argv[a]), wmax = atoi(argv[a + 1]);
        int R2 = atoi(argv[a + 2]), I2 = atoi(argv[a + 3]), R1 = atoi(argv[a + 4]), I1 = atoi(argv[a + 5]); rs = strtoull(argv[a + 6], 0, 10) * 2654435761ULL + 43;
        for (int k = 0; k < nn; k++) {
            int cc[2048], b1[64], b2[64], out[2048], bw1, bw2; memcpy(cc, c, sizeof(int) * n);
            if (isnull) for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), x = cc[i]; cc[i] = cc[j]; cc[j] = x; }
            double s = full(cc, n, wmin, wmax, 0, 0, R2, I2, R1, I1, &bw1, &bw2, b1, b2, out);
            printf("%s %d score=%.4f w=%d,%d ", isnull ? "NUL" : "REEL", k, s, bw1, bw2);
            for (int i = 0; i < n && i < 160; i++) putchar('a' + out[i]);
            putchar('\n'); fflush(stdout);
        }
    }
    return 0;
}
