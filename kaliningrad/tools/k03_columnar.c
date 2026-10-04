/* K03 — grille carrée à clé (V1 colonnes / V2 lignes), montée avec redémarrages, score quadrigrammes allemands.
   Voir experiments/K03_grille_a_cle/PREREGISTRATION.md.
   Compilation : gcc -O2 -o k03 tools/k03_columnar.c -lm
   Usage :
     k03 ctrl  <qg.bin> <heldout.txt> <q> <nblocs> <taux_bruit> <R> <I> <graine>
     k03 solve <qg.bin> <lettres a-z> <R> <I> <graine>            (q déduit : 169 -> 13, 144 -> 12)
     k03 null  <qg.bin> <lettres a-z> <nnull> <R> <I> <graine>
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static float *QG;
static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }

static double score(const int *p, int n) {
    double s = 0;
    for (int i = 0; i + 3 < n; i++) s += QG[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]];
    return s / (n - 3);
}

/* lecture : var 0 = V1 (colonnes à clé : le morceau j du chiffré est la colonne perm[j], clair lu en lignes)
             var 1 = V2 (opération inverse : clair écrit en lignes, colonnes permutées, lu en lignes après lecture des colonnes)
   dir 0 = endroit, 1 = envers */
static void decrypt(const int *c, int q, const int *perm, int var, int dir, int *out) {
    int n = q * q, tmp[256];
    for (int j = 0; j < q; j++)
        for (int k = 0; k < q; k++) {
            if (var == 0) tmp[k * q + perm[j]] = c[j * q + k];
            else          tmp[j * q + k] = c[k * q + perm[j]];
        }
    for (int i = 0; i < n; i++) out[i] = dir ? tmp[n - 1 - i] : tmp[i];
}

static double climb(const int *c, int q, int var, int dir, int R, int I, int *bestperm) {
    int n = q * q, perm[16], cand[16], pt[256];
    double best = -1e9;
    for (int r = 0; r < R; r++) {
        for (int i = 0; i < q; i++) perm[i] = i;
        for (int i = q - 1; i > 0; i--) { int j = rint_(i + 1), t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
        decrypt(c, q, perm, var, dir, pt); double cur = score(pt, n);
        for (int it = 0; it < I; it++) {
            memcpy(cand, perm, sizeof(int) * q);
            int mv = rint_(3), a = rint_(q), b = rint_(q);
            if (a == b) continue;
            if (mv == 0) { int t = cand[a]; cand[a] = cand[b]; cand[b] = t; }
            else if (mv == 1) { if (a > b) { int t = a; a = b; b = t; } while (a < b) { int t = cand[a]; cand[a] = cand[b]; cand[b] = t; a++; b--; } }
            else { int v = cand[a]; if (a < b) { memmove(cand + a, cand + a + 1, sizeof(int) * (b - a)); } else { memmove(cand + b + 1, cand + b, sizeof(int) * (a - b)); } cand[b] = v; }
            decrypt(c, q, cand, var, dir, pt); double s = score(pt, n);
            if (s >= cur) { cur = s; memcpy(perm, cand, sizeof(int) * q); }
        }
        if (cur > best) { best = cur; if (bestperm) memcpy(bestperm, perm, sizeof(int) * q); }
    }
    return best;
}

/* meilleure des 4 lectures */
static double search(const int *c, int q, int R, int I, int *bv, int *bd, int *bp) {
    double best = -1e9; int perm[16];
    for (int var = 0; var < 2; var++)
        for (int dir = 0; dir < 2; dir++) {
            double s = climb(c, q, var, dir, R, I, perm);
            if (s > best) { best = s; *bv = var; *bd = dir; memcpy(bp, perm, sizeof(int) * q); }
        }
    return best;
}

/* chiffrement inverse de decrypt (pour les contrôles) */
static void encrypt(const int *p, int q, const int *perm, int var, int *c) {
    for (int j = 0; j < q; j++)
        for (int k = 0; k < q; k++) {
            if (var == 0) c[j * q + k] = p[k * q + perm[j]];
            else          c[k * q + perm[j]] = p[j * q + k];
        }
}

static int load_letters(const char *s, int *out) {
    int n = 0;
    for (; *s; s++) if (*s >= 'a' && *s <= 'z') out[n++] = *s - 'a'; else if (*s >= 'A' && *s <= 'Z') out[n++] = *s - 'A';
    return n;
}

static void loadqg(const char *f) {
    QG = malloc(sizeof(float) * 456976); FILE *fp = fopen(f, "rb");
    if (!fp || fread(QG, sizeof(float), 456976, fp) != 456976) { fprintf(stderr, "qg ?\n"); exit(1); }
    fclose(fp);
}

static void print_pt(const int *p, int n) { for (int i = 0; i < n; i++) putchar('a' + p[i]); putchar('\n'); }

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage : voir en-tête\n"); return 1; }
    loadqg(argv[2]);
    if (!strcmp(argv[1], "ctrl")) {
        FILE *fp = fopen(argv[3], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *t = malloc(L + 1); if (fread(t, 1, L, fp) != (size_t)L) return 2; t[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int N = load_letters(t, txt);
        int q = atoi(argv[4]), nb = atoi(argv[5]); double noise = atof(argv[6]); int R = atoi(argv[7]), I = atoi(argv[8]);
        rs = strtoull(argv[9], 0, 10) * 2654435761ULL + 1;
        int n = q * q, ok = 0;
        for (int b = 0; b < nb; b++) {
            int p[256], c[256], perm[16], bp[16], out[256], bv, bd;
            int o = rint_(N - n); memcpy(p, txt + o, sizeof(int) * n);
            int pn[256]; memcpy(pn, p, sizeof(int) * n);
            for (int i = 0; i < n; i++) if ((rnd() % 100000) < noise * 100000) pn[i] = rint_(26);
            for (int i = 0; i < q; i++) perm[i] = i;
            for (int i = q - 1; i > 0; i--) { int j = rint_(i + 1), tt = perm[i]; perm[i] = perm[j]; perm[j] = tt; }
            int var = b & 1; encrypt(pn, q, perm, var, c);
            double s = search(c, q, R, I, &bv, &bd, bp);
            decrypt(c, q, bp, bv, bd, out);
            /* critère (amendement 1) : part des lettres voisines du résultat qui sont voisines dans le clair */
            int idx[256], cidx[256], oidx[256], good = 0;
            for (int i = 0; i < n; i++) idx[i] = i;
            encrypt(idx, q, perm, var, cidx); decrypt(cidx, q, bp, bv, bd, oidx);
            for (int i = 0; i + 1 < n; i++) good += oidx[i + 1] == oidx[i] + 1;
            ok += good >= 0.9 * (n - 1);
            printf("bloc %2d q=%d var=%d score=%.3f vrai=%.3f contacts=%d/%d\n", b, q, var, s, score(pn, n), good, n - 1);
        }
        printf("SUCCES %d/%d (q=%d, bruit=%.2f, R=%d, I=%d)\n", ok, nb, q, noise, R, I);
    } else if (!strcmp(argv[1], "solve") || !strcmp(argv[1], "null")) {
        int c[256], n = load_letters(argv[3], c), q = n == 169 ? 13 : n == 144 ? 12 : 0;
        if (!q) { fprintf(stderr, "taille %d non carrée\n", n); return 1; }
        int isnull = !strcmp(argv[1], "null"), nn = isnull ? atoi(argv[4]) : 1, a = isnull ? 5 : 4;
        int R = atoi(argv[a]), I = atoi(argv[a + 1]); rs = strtoull(argv[a + 2], 0, 10) * 2654435761ULL + 7;
        for (int k = 0; k < nn; k++) {
            int cc[256], bp[16], out[256], bv, bd; memcpy(cc, c, sizeof(int) * n);
            if (isnull) for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), t = cc[i]; cc[i] = cc[j]; cc[j] = t; }
            double s = search(cc, q, R, I, &bv, &bd, bp);
            decrypt(cc, q, bp, bv, bd, out);
            printf("%s %d score=%.4f var=V%d dir=%d ", isnull ? "NUL" : "REEL", k, s, bv + 1, bd);
            if (!isnull) { printf("cle="); for (int i = 0; i < q; i++) printf("%d%c", bp[i], i < q - 1 ? ',' : ' '); }
            print_pt(out, n);
            fflush(stdout);
        }
    }
    return 0;
}
