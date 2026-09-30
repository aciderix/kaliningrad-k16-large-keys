/* K15 — chiffrement par blocs avec clé commune ; score additionné sur les blocs (MI invariant par substitution, ou quadrigrammes).
   Voir experiments/K15_blocs_cle_commune/PREREGISTRATION.md.
   Compilation : gcc -O2 -o k15 tools/k15_blocs.c -lm
   Usage :
     k15 ctrl  <fam C|U|D|F> <score Q|I> <qg.bin> <texte_reserve> <nessais> <R> <I> <graine>
     k15 solve <fam> <score> <qg.bin> <blocs séparés par des virgules> <R> <I> <graine>
     k15 null  <fam> <score> <qg.bin> <blocs> <nnull> <R> <I> <graine>                         */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static float *QG; static double LOG2[8192];
static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }
static double rnd01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static char FAM, SC;
#define MAXB 6
static int NB, BL[MAXB], BLK[MAXB][256];

/* ---------- colonnes à clé (dernière ligne incomplète) ---------- */
static void mapping(int n, int w, const int *perm, int *pos) {
    int h = n / w, r = n % w, start[64], k = 0;
    for (int j = 0; j < w; j++) { int col = perm[j]; start[col] = k; k += h + (col < r); }
    for (int i = 0; i < n; i++) pos[i] = start[i % w] + i / w;
}
/* ---------- grille tournante 13×13 (cf. k05) ---------- */
static int Q13 = 13, N169 = 169, NORB, orb[169], rotm[169], center = -1;
static void build13(void) {
    int q = Q13, seen[169] = {0}; NORB = 0;
    for (int c = 0; c < N169; c++) {
        if (seen[c]) continue; int r0 = c / q, c0 = c % q;
        if (r0 == q / 2 && c0 == q / 2) { center = c; seen[c] = 1; orb[c] = -1; continue; }
        int r = r0, cc = c0;
        for (int m = 0; m < 4; m++) { int id = r * q + cc; seen[id] = 1; orb[id] = NORB; rotm[id] = m; int nr = cc, nc = q - 1 - r; r = nr; cc = nc; }
        NORB++;
    }
}
static void fl_order(const int *key, int v, int *ord) {
    int k = 0, dir = v & 1;
    for (int p = 0; p < 4; p++) for (int c = 0; c < N169; c++) {
        int pass = (c == center) ? key[NORB] : (dir ? (key[orb[c]] - rotm[c]) & 3 : (rotm[c] - key[orb[c]]) & 3);
        if (pass == p) ord[k++] = c;
    }
}

typedef struct { int w1, w2, v, k1[64], k2[64]; } Key;

/* clair d'un bloc à partir du chiffré du bloc */
static void decrypt_block(const int *c, int n, const Key *K, int *out) {
    int p1[256], p2[256], t[256];
    if (FAM == 'C') { mapping(n, K->w1, K->k1, p1); for (int i = 0; i < n; i++) out[i] = c[p1[i]]; }
    else if (FAM == 'U' || FAM == 'D') {
        const int *kk2 = FAM == 'U' ? K->k1 : K->k2; int w2 = FAM == 'U' ? K->w1 : K->w2;
        mapping(n, w2, kk2, p2); for (int j = 0; j < n; j++) t[j] = c[p2[j]];
        mapping(n, K->w1, K->k1, p1); for (int i = 0; i < n; i++) out[i] = t[p1[i]];
    } else {
        int grid[169], ord[169];
        for (int i = 0; i < 169; i++) grid[i] = (K->v & 2) ? c[(i % 13) * 13 + i / 13] : c[i];
        fl_order(K->k1, K->v, ord);
        for (int i = 0; i < 169; i++) out[(K->v & 4) ? 168 - i : i] = grid[ord[i]];
    }
}
static void encrypt_block(const int *p, int n, const Key *K, int *c) {
    int idx[256], cidx[256], i;
    /* on chiffre par inversion de la fonction de déchiffrement appliquée aux indices */
    for (i = 0; i < n; i++) idx[i] = i;
    decrypt_block(idx, n, K, cidx);          /* cidx[i] = position dans le chiffré de la lettre i du clair */
    for (i = 0; i < n; i++) c[cidx[i]] = p[i];
}

static double score_blocks(int blocks[][256], const int *lens, int nb) {
    if (SC == 'Q') {
        double s = 0; int m = 0;
        for (int b = 0; b < nb; b++) for (int i = 0; i + 3 < lens[b]; i++) { const int *p = blocks[b] + i; s += QG[((p[0] * 26 + p[1]) * 26 + p[2]) * 26 + p[3]]; m++; }
        return s / m;
    }
    static int cnt[676], cx[26], cy[26]; memset(cnt, 0, sizeof cnt); memset(cx, 0, sizeof cx); memset(cy, 0, sizeof cy); int m = 0;
    for (int b = 0; b < nb; b++) for (int i = 0; i + 1 < lens[b]; i++) { int a = blocks[b][i], c = blocks[b][i + 1]; cnt[a * 26 + c]++; cx[a]++; cy[c]++; m++; }
    double s = 0, lm = log2(m);
    for (int a = 0; a < 26; a++) { if (!cx[a]) continue; for (int c = 0; c < 26; c++) { int v = cnt[a * 26 + c]; if (v) s += v * (LOG2[v] + lm - LOG2[cx[a]] - LOG2[cy[c]]); } }
    return s / m;
}
static double eval(int cb[][256], const int *lens, int nb, const Key *K) {
    static int out[MAXB][256];
    for (int b = 0; b < nb; b++) decrypt_block(cb[b], lens[b], K, out[b]);
    return score_blocks(out, lens, nb);
}

static void randperm(int *p, int w) { for (int i = 0; i < w; i++) p[i] = i; for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), x = p[i]; p[i] = p[j]; p[j] = x; } }
static void mutate_perm(int *k, int w) {
    int a = rint_(w), b = rint_(w); if (a == b) return; int mv = rint_(3);
    if (mv == 0) { int x = k[a]; k[a] = k[b]; k[b] = x; }
    else if (mv == 1) { if (a > b) { int x = a; a = b; b = x; } while (a < b) { int x = k[a]; k[a] = k[b]; k[b] = x; a++; b--; } }
    else { int v = k[a]; if (a < b) memmove(k + a, k + a + 1, sizeof(int) * (b - a)); else memmove(k + b + 1, k + b, sizeof(int) * (a - b)); k[b] = v; }
}
static void randkey(Key *K) {
    if (FAM == 'F') { for (int i = 0; i <= NORB; i++) K->k1[i] = rint_(4); return; }
    randperm(K->k1, K->w1); if (FAM == 'D') randperm(K->k2, K->w2);
}
static void mutate(Key *K) {
    if (FAM == 'F') { int o = rint_(NORB + 1); K->k1[o] = (K->k1[o] + 1 + rint_(3)) & 3; return; }
    if (FAM == 'D' && rint_(2)) mutate_perm(K->k2, K->w2); else mutate_perm(K->k1, K->w1);
}

static double anneal(int cb[][256], const int *lens, int nb, Key *K0, int R, int I, Key *best) {
    double bs = -1e18, T0 = SC == 'Q' ? 0.3 : 0.02, T1 = SC == 'Q' ? 0.005 : 0.0005;
    if (FAM == 'F') { T0 = SC == 'Q' ? 6.0 / 600 * 3 : 0.02; }
    for (int r = 0; r < R; r++) {
        Key K = *K0; randkey(&K); double cur = eval(cb, lens, nb, &K);
        for (int it = 0; it < I; it++) {
            Key Q = K; mutate(&Q); double s = eval(cb, lens, nb, &Q), T = T0 * pow(T1 / T0, (double)it / I);
            if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; K = Q; if (cur > bs) { bs = cur; *best = K; } }
        }
    }
    return bs;
}
static double search(int cb[][256], const int *lens, int nb, int R, int I, Key *best) {
    double bs = -1e18; Key K = {0}, B = {0};
    if (FAM == 'C') { for (int w = 5; w <= 20; w++) { K.w1 = w; double s = anneal(cb, lens, nb, &K, R, I, &B); if (s > bs) { bs = s; *best = B; } } }
    else if (FAM == 'U') { for (int w = 5; w <= 15; w++) { K.w1 = w; double s = anneal(cb, lens, nb, &K, R, I, &B); if (s > bs) { bs = s; *best = B; } } }
    else if (FAM == 'D') { for (int a = 5; a <= 13; a++) for (int b = 5; b <= 13; b++) { K.w1 = a; K.w2 = b; double s = anneal(cb, lens, nb, &K, R, I, &B); if (s > bs) { bs = s; *best = B; } } }
    else { for (int v = 0; v < 8; v++) { K.v = v; double s = anneal(cb, lens, nb, &K, R, I, &B); if (s > bs) { bs = s; *best = B; } } }
    return bs;
}

static int load_letters(const char *s, int *out, int max) {
    int n = 0; for (; *s && n < max; s++) if (*s >= 'a' && *s <= 'z') out[n++] = *s - 'a'; else if (*s >= 'A' && *s <= 'Z') out[n++] = *s - 'A';
    return n;
}

int main(int argc, char **argv) {
    for (int i = 1; i < 8192; i++) LOG2[i] = log2(i);
    if (argc < 5) return 1;
    FAM = argv[2][0]; SC = argv[3][0]; build13();
    QG = malloc(sizeof(float) * 456976); FILE *fp = fopen(argv[4], "rb");
    if (!fp || fread(QG, sizeof(float), 456976, fp) != 456976) { fprintf(stderr, "qg ?\n"); return 1; } fclose(fp);
    int sizes[6] = {166, 169, 162, 169, 169, 144};
    if (!strcmp(argv[1], "ctrl")) {
        fp = fopen(argv[5], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *tx = malloc(L + 1); if (fread(tx, 1, L, fp) != (size_t)L) return 2; tx[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(tx, txt, L);
        int ne = atoi(argv[6]), R = atoi(argv[7]), I = atoi(argv[8]); rs = strtoull(argv[9], 0, 10) * 2654435761ULL + 51; int ok = 0;
        for (int e = 0; e < ne; e++) {
            int sub[26], lens[6], nb = 0, pb[6][256], cb[6][256]; Key K = {0}, B = {0};
            for (int i = 0; i < 26; i++) sub[i] = i;
            if (SC == 'I') for (int i = 25; i > 0; i--) { int j = rint_(i + 1), x = sub[i]; sub[i] = sub[j]; sub[j] = x; }
            int o = rint_(M - 1100), k = o;
            if (FAM == 'C') K.w1 = 5 + rint_(16); else if (FAM == 'U') K.w1 = 5 + rint_(11);
            else if (FAM == 'D') { K.w1 = 5 + rint_(9); K.w2 = 5 + rint_(9); } else K.v = rint_(8);
            randkey(&K);
            for (int b = 0; b < 6; b++) {
                if (FAM == 'F' && sizes[b] != 169) { k += sizes[b]; continue; }
                lens[nb] = sizes[b]; for (int i = 0; i < sizes[b]; i++) pb[nb][i] = sub[txt[k + i]]; k += sizes[b];
                encrypt_block(pb[nb], lens[nb], &K, cb[nb]); nb++;
            }
            double s = search(cb, lens, nb, R, I, &B);
            int good = 0, tot = 0;
            for (int b = 0; b < nb; b++) {
                int idx[256], cidx[256], oidx[256]; for (int i = 0; i < lens[b]; i++) idx[i] = i;
                encrypt_block(idx, lens[b], &K, cidx); decrypt_block(cidx, lens[b], &B, oidx);
                for (int i = 0; i + 1 < lens[b]; i++) { good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1; tot++; }
            }
            ok += good >= 0.9 * tot;
            printf("essai %d : vrai w=%d,%d v=%d | trouvé w=%d,%d v=%d score=%.4f (vrai %.4f) contacts=%d/%d\n", e, K.w1, K.w2, K.v, B.w1, B.w2, B.v, s,
                   score_blocks(pb, lens, nb), good, tot);
            fflush(stdout);
        }
        printf("SUCCES %d/%d (fam=%c score=%c R=%d I=%d)\n", ok, ne, FAM, SC, R, I);
    } else {
        int isnull = !strcmp(argv[1], "null"), a = isnull ? 7 : 6, nn = isnull ? atoi(argv[6]) : 1;
        int R = atoi(argv[a]), I = atoi(argv[a + 1]); rs = strtoull(argv[a + 2], 0, 10) * 2654435761ULL + 53;
        char *s = strdup(argv[5]); int lens[6], nb = 0, cb0[6][256];
        for (char *tok = strtok(s, ","); tok; tok = strtok(NULL, ",")) {
            int n = load_letters(tok, cb0[nb], 256);
            if (FAM == 'F' && n != 169) continue;
            lens[nb++] = n;
        }
        for (int k = 0; k < nn; k++) {
            int cb[6][256], out[256]; Key B; memcpy(cb, cb0, sizeof cb);
            if (isnull) for (int b = 0; b < nb; b++) for (int i = lens[b] - 1; i > 0; i--) { int j = rint_(i + 1), x = cb[b][i]; cb[b][i] = cb[b][j]; cb[b][j] = x; }
            double sc = search(cb, lens, nb, R, I, &B);
            printf("%s %d score=%.4f w=%d,%d v=%d ", isnull ? "NUL" : "REEL", k, sc, B.w1, B.w2, B.v);
            decrypt_block(cb[0], lens[0], &B, out); for (int i = 0; i < lens[0]; i++) putchar('a' + out[i]);
            putchar('\n'); fflush(stdout);
        }
    }
    return 0;
}
