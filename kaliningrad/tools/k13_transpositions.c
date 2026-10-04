/* K13 — transposition nihiliste (N), Myszkowski (M), AMSCO (A) ; recuit simulé ; score quadrigrammes allemands (Q) ou MI(1) (I).
   Voir experiments/K13_transpositions_restantes/PREREGISTRATION.md.
   Compilation : gcc -O2 -o k13 tools/k13_transpositions.c -lm
   Usage :
     k13 ctrl  <fam N|M|A> <score Q|I> <qg.bin> <texte_reserve> <n> <nessais> <R> <I> <graine>
     k13 solve <fam> <score> <qg.bin> <lettres> <R> <I> <graine>
     k13 null  <fam> <score> <qg.bin> <lettres> <nnull> <R> <I> <graine>
   Portées : N : n = q² (q = 12 ou 13), lecture en lignes (v=0) ou en colonnes (v=1) ; M : w = 5..15 ; A : w = 3..12, départ 1/2. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static float *QG; static double LOG2[4096];
static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }
static double rnd01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static char FAM, SC;

static double score(const int *p, int n) {
    if (SC == 'Q') { double s = 0; for (int i = 0; i + 3 < n; i++) s += QG[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]; return s / (n - 3); }
    static int cnt[676], cx[26], cy[26];
    memset(cnt, 0, sizeof cnt); memset(cx, 0, sizeof cx); memset(cy, 0, sizeof cy);
    for (int i = 0; i + 1 < n; i++) { cnt[p[i] * 26 + p[i + 1]]++; cx[p[i]]++; cy[p[i + 1]]++; }
    double m = n - 1, s = 0, lm = log2(m);
    for (int a = 0; a < 26; a++) { if (!cx[a]) continue; for (int b = 0; b < 26; b++) { int c = cnt[a * 26 + b]; if (c) s += c * (LOG2[c] + lm - LOG2[cx[a]] - LOG2[cy[b]]); } }
    return s / m;
}

/* paramètres : w (largeur ou côté), v (variante : N lecture, A départ), key[w] (permutation, ou rangs pour M) */
typedef struct { int w, v, key[32]; } Param;

/* order[k] = indice dans le clair de la k-ième lettre du chiffré */
static int order_of(const Param *P, int n, int *ord) {
    int w = P->w, k = 0;
    if (FAM == 'N') {                       /* clair en lignes q×q ; H[i][j] = G[key[i]][key[j]] ; chiffré = H lu en lignes/colonnes */
        for (int a = 0; a < w; a++) for (int b = 0; b < w; b++) {
            int i = P->v ? b : a, j = P->v ? a : b;
            ord[k++] = P->key[i] * w + P->key[j];
        }
    } else if (FAM == 'M') {                /* rangs avec ex æquo : pour chaque rang croissant, lignes, colonnes de ce rang */
        int h = (n + w - 1) / w;
        for (int r = 0; r < w; r++) {
            int any = 0; for (int c = 0; c < w; c++) if (P->key[c] == r) any = 1;
            if (!any) continue;
            for (int row = 0; row < h; row++) for (int c = 0; c < w; c++) if (P->key[c] == r && row * w + c < n) ord[k++] = row * w + c;
        }
    } else {                                /* AMSCO : cases 1/2 lettres alternées (globalement), colonnes lues selon la clé */
        static int cs[2048], cl[2048], cc[2048]; int ncell = 0, pos = 0, sz = P->v;
        while (pos < n) { int L = sz < n - pos ? sz : n - pos; cs[ncell] = pos; cl[ncell] = L; cc[ncell] = ncell % w; ncell++; pos += L; sz = 3 - sz; }
        for (int j = 0; j < w; j++) { int col = P->key[j]; for (int c = 0; c < ncell; c++) if (cc[c] == col) for (int t = 0; t < cl[c]; t++) ord[k++] = cs[c] + t; }
    }
    return k;
}
static void decrypt(const int *c, int n, const Param *P, int *out) { int ord[2048]; order_of(P, n, ord); for (int k = 0; k < n; k++) out[ord[k]] = c[k]; }
static void encrypt(const int *p, int n, const Param *P, int *c) { int ord[2048]; order_of(P, n, ord); for (int k = 0; k < n; k++) c[k] = p[ord[k]]; }

static void randkey(Param *P) {
    int w = P->w;
    if (FAM == 'M') { for (int i = 0; i < w; i++) P->key[i] = rint_(w); return; }
    for (int i = 0; i < w; i++) P->key[i] = i;
    for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), t = P->key[i]; P->key[i] = P->key[j]; P->key[j] = t; }
}
static void mutate(Param *P) {
    int w = P->w, a = rint_(w), b = rint_(w);
    if (FAM == 'M' && rint_(2)) { P->key[a] = rint_(w); return; }
    if (a == b) return;
    if (rint_(2)) { int t = P->key[a]; P->key[a] = P->key[b]; P->key[b] = t; }
    else { int v = P->key[a]; if (a < b) memmove(P->key + a, P->key + a + 1, sizeof(int) * (b - a)); else memmove(P->key + b + 1, P->key + b, sizeof(int) * (a - b)); P->key[b] = v; }
}

static double anneal(const int *c, int n, int w, int v, int R, int I, Param *best) {
    double bs = -1e18, T0 = SC == 'Q' ? 0.3 : 0.02, T1 = SC == 'Q' ? 0.005 : 0.0005; int out[2048];
    for (int r = 0; r < R; r++) {
        Param P = { .w = w, .v = v }; randkey(&P); decrypt(c, n, &P, out); double cur = score(out, n);
        for (int it = 0; it < I; it++) {
            Param Q = P; mutate(&Q); decrypt(c, n, &Q, out); double s = score(out, n);
            double T = T0 * pow(T1 / T0, (double)it / I);
            if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; P = Q; if (cur > bs) { bs = cur; *best = P; } }
        }
    }
    return bs;
}

static double search(const int *c, int n, int R, int I, Param *best) {
    double bs = -1e18; Param P;
    int wmin, wmax, vmin, vmax;
    if (FAM == 'N') { wmin = wmax = (int)lround(sqrt(n)); vmin = 0; vmax = 1; }
    else if (FAM == 'M') { wmin = 5; wmax = 15; vmin = vmax = 0; }
    else { wmin = 3; wmax = 12; vmin = 1; vmax = 2; }
    for (int w = wmin; w <= wmax; w++) for (int v = vmin; v <= vmax; v++) {
        double s = anneal(c, n, w, v, R, I, &P); if (s > bs) { bs = s; *best = P; }
    }
    return bs;
}

static int load_letters(const char *s, int *out, int max) {
    int n = 0; for (; *s && n < max; s++) if (*s >= 'a' && *s <= 'z') out[n++] = *s - 'a'; else if (*s >= 'A' && *s <= 'Z') out[n++] = *s - 'A';
    return n;
}

int main(int argc, char **argv) {
    for (int i = 1; i < 4096; i++) LOG2[i] = log2(i);
    if (argc < 5) return 1;
    FAM = argv[2][0]; SC = argv[3][0];
    QG = malloc(sizeof(float) * 456976); FILE *fp = fopen(argv[4], "rb");
    if (!fp || fread(QG, sizeof(float), 456976, fp) != 456976) { fprintf(stderr, "qg ?\n"); return 1; } fclose(fp);
    if (!strcmp(argv[1], "ctrl")) {
        fp = fopen(argv[5], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *t = malloc(L + 1); if (fread(t, 1, L, fp) != (size_t)L) return 2; t[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(t, txt, L);
        int n = atoi(argv[6]), ne = atoi(argv[7]), R = atoi(argv[8]), I = atoi(argv[9]); rs = strtoull(argv[10], 0, 10) * 2654435761ULL + 29;
        int ok = 0;
        for (int e = 0; e < ne; e++) {
            int p[2048], c[2048], sub[26], idx[2048], cidx[2048], oidx[2048]; Param P, B;
            for (int i = 0; i < 26; i++) sub[i] = i;
            if (SC == 'I') for (int i = 25; i > 0; i--) { int j = rint_(i + 1), x = sub[i]; sub[i] = sub[j]; sub[j] = x; }
            int o = rint_(M - n); for (int i = 0; i < n; i++) p[i] = sub[txt[o + i]];
            if (FAM == 'N') { P.w = (int)lround(sqrt(n)); P.v = rint_(2); }
            else if (FAM == 'M') { P.w = 5 + rint_(11); P.v = 0; }
            else { P.w = 3 + rint_(10); P.v = 1 + rint_(2); }
            randkey(&P); encrypt(p, n, &P, c);
            double s = search(c, n, R, I, &B);
            for (int i = 0; i < n; i++) idx[i] = i;
            encrypt(idx, n, &P, cidx); decrypt(cidx, n, &B, oidx);
            int good = 0; for (int i = 0; i + 1 < n; i++) good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1;
            ok += good >= 0.9 * (n - 1);
            printf("essai %d : vrai w=%d v=%d | trouvé w=%d v=%d score=%.4f (vrai %.4f) contacts=%d/%d\n", e, P.w, P.v, B.w, B.v, s, score(p, n), good, n - 1);
            fflush(stdout);
        }
        printf("SUCCES %d/%d (fam=%c score=%c n=%d R=%d I=%d)\n", ok, ne, FAM, SC, n, R, I);
    } else {
        int c[2048], n = load_letters(argv[5], c, 2048);
        int isnull = !strcmp(argv[1], "null"), nn = isnull ? atoi(argv[6]) : 1, a = isnull ? 7 : 6;
        int R = atoi(argv[a]), I = atoi(argv[a + 1]); rs = strtoull(argv[a + 2], 0, 10) * 2654435761ULL + 31;
        for (int k = 0; k < nn; k++) {
            int cc[2048], out[2048]; Param B; memcpy(cc, c, sizeof(int) * n);
            if (isnull) for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), t = cc[i]; cc[i] = cc[j]; cc[j] = t; }
            double s = search(cc, n, R, I, &B); decrypt(cc, n, &B, out);
            printf("%s %d score=%.4f w=%d v=%d ", isnull ? "NUL" : "REEL", k, s, B.w, B.v);
            for (int i = 0; i < n && i < 160; i++) putchar('a' + out[i]);
            putchar('\n'); fflush(stdout);
        }
    }
    return 0;
}
