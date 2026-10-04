/* K30 — grille tournante (Fleissner), une clé par bloc, avec le modèle 6-grammes tolérant aux nuls de K30
   (tools/k30/build_lm6.c) au lieu des quadrigrammes. Dérivé de tools/k05_fleissner.c (mêmes conventions, mêmes
   variantes). Si le fichier modèle se termine par « .bin » et fait 26^6 octets, il est lu comme modèle 6-grammes ;
   sinon comme qg_de.bin (quadrigrammes).
   Contrôle : bruit = proportion de NULS INSÉRÉS (f, w, n dans les proportions 32:19:48), pas de lettres remplacées.
   Compilation : gcc -O3 -march=native -fopenmp -o fleiss_lm tools/k30/fleiss_lm.c -lm
   Usage :
     fleiss_lm ctrl  <modèle> <texte_reserve> <q> <nblocs> <nuls> <R> <I> <graine>
     fleiss_lm solve <modèle> <lettres> <R> <I> <graine>
     fleiss_lm null  <modèle> <lettres> <nnull> <R> <I> <graine>
   Variante v (0..7) : bit0 = sens (0 horaire, 1 antihoraire), bit1 = carré lu en colonnes, bit2 = clair à l'envers. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <omp.h>

static float *QG; static uint8_t *LM6;
static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }
static double rnd01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

static int Q, N, NORB, orb[256], rotm[256], center = -1;

static void build(int q) {
    Q = q; N = q * q; NORB = 0; center = -1;
    int seen[256] = {0};
    for (int c = 0; c < N; c++) {
        if (seen[c]) continue;
        int r0 = c / q, c0 = c % q;
        if (q % 2 && r0 == q / 2 && c0 == q / 2) { center = c; seen[c] = 1; orb[c] = -1; rotm[c] = 0; continue; }
        int r = r0, cc = c0;
        for (int m = 0; m < 4; m++) {
            int id = r * q + cc; seen[id] = 1; orb[id] = NORB; rotm[id] = m;
            int nr = cc, nc = q - 1 - r; r = nr; cc = nc;              /* quart de tour horaire */
        }
        NORB++;
    }
}

/* clé : key[0..NORB-1] dans 0..3, key[NORB] = passe de la case centrale */
static void order(const int *key, int v, int *ord) {
    int k = 0, dir = v & 1;
    for (int p = 0; p < 4; p++)
        for (int c = 0; c < N; c++) {
            int pass = (c == center) ? key[NORB] : (dir ? (key[orb[c]] - rotm[c]) & 3 : (rotm[c] - key[orb[c]]) & 3);
            if (pass == p) ord[k++] = c;
        }
}

static void decrypt(const int *cip, const int *key, int v, int *out) {
    int grid[256], ord[256];
    for (int i = 0; i < N; i++) grid[i] = (v & 2) ? cip[(i % Q) * Q + i / Q] : cip[i];
    order(key, v, ord);
    for (int i = 0; i < N; i++) out[(v & 4) ? N - 1 - i : i] = grid[ord[i]];
}

static void encrypt(const int *pt, const int *key, int v, int *cip) {
    int grid[256], ord[256];
    order(key, v, ord);
    for (int i = 0; i < N; i++) grid[ord[i]] = pt[(v & 4) ? N - 1 - i : i];
    for (int i = 0; i < N; i++) { if (v & 2) cip[(i % Q) * Q + i / Q] = grid[i]; else cip[i] = grid[i]; }
}

static double score(const int *p) {
    double s = 0;
    if (LM6) {
        long h = 0; for (int i = 0; i < 5; i++) h = h * 26 + p[i];
        int acc = 0;
        for (int i = 5; i < N; i++) { long idx = (h % 11881376L) * 26 + p[i]; acc += LM6[idx]; h = idx; }
        return -acc / 16.0 * (N - 3) / (N - 5);     /* même échelle (par lettre × N−3) que les quadrigrammes */
    }
    for (int i = 0; i + 3 < N; i++) s += QG[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]];
    return s;
}

static double anneal(const int *cip, int v, int R, int I, int *best) {
    int key[64], out[256], nk = NORB + (center >= 0);
    double bs = -1e18;
    for (int r = 0; r < R; r++) {
        for (int i = 0; i < nk; i++) key[i] = rint_(4);
        if (center < 0) key[NORB] = 0;
        decrypt(cip, key, v, out); double cur = score(out);
        double T0 = 6.0, T1 = 0.2;
        for (int it = 0; it < I; it++) {
            double T = T0 * pow(T1 / T0, (double)it / I);
            int o = rint_(nk), old = key[o], nv = (old + 1 + rint_(3)) & 3;
            key[o] = nv; decrypt(cip, key, v, out); double s = score(out);
            if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; if (cur > bs) { bs = cur; memcpy(best, key, sizeof(int) * 64); } }
            else key[o] = old;
        }
    }
    return bs;
}

static double search(const int *cip, int R, int I, int *bv, int *bk) {
    double best = -1e18; int key[64];
    for (int v = 0; v < 8; v++) {
        double s = anneal(cip, v, R, I, key);
        if (s > best) { best = s; *bv = v; memcpy(bk, key, sizeof(int) * 64); }
    }
    return best;
}

static int load_letters(const char *s, int *out) {
    int n = 0;
    for (; *s; s++) if (*s >= 'a' && *s <= 'z') out[n++] = *s - 'a'; else if (*s >= 'A' && *s <= 'Z') out[n++] = *s - 'A';
    return n;
}

int main(int argc, char **argv) {
    if (argc < 3) return 1;
    FILE *fp = fopen(argv[2], "rb"); if (!fp) { fprintf(stderr, "modèle ?\n"); return 1; }
    fseek(fp, 0, SEEK_END); long msz = ftell(fp); fseek(fp, 0, SEEK_SET);
    if (msz == 308915776L) { LM6 = malloc(msz); if (fread(LM6, 1, msz, fp) != (size_t)msz) return 1; }
    else { QG = malloc(sizeof(float) * 456976); if (fread(QG, sizeof(float), 456976, fp) != 456976) { fprintf(stderr, "qg ?\n"); return 1; } }
    fclose(fp);
    if (!strcmp(argv[1], "ctrl")) {
        fp = fopen(argv[3], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *t = malloc(L + 1); if (fread(t, 1, L, fp) != (size_t)L) return 2; t[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(t, txt);
        int q = atoi(argv[4]), nb = atoi(argv[5]); double noise = atof(argv[6]); int R = atoi(argv[7]), I = atoi(argv[8]);
        rs = strtoull(argv[9], 0, 10) * 2654435761ULL + 3; build(q);
        int ok = 0;
        for (int b = 0; b < nb; b++) {
            int p[256], c[256], key[64], bk[64], bv, idx[256], cidx[256], oidx[256];
            int o = rint_(M - 2 * N), j = 0;
            for (int i = 0; i < N; i++) {           /* nuls insérés : f, w, n (32:19:48) */
                if ((rnd() % 100000) < noise * 100000) { int u = rint_(99); p[i] = u < 32 ? 5 : u < 51 ? 22 : 13; }
                else p[i] = txt[o + j++];
            }
            for (int i = 0; i < 64; i++) key[i] = rint_(4);
            int v = rint_(8); encrypt(p, key, v, c);
            double s = search(c, R, I, &bv, bk);
            for (int i = 0; i < N; i++) idx[i] = i;
            encrypt(idx, key, v, cidx); decrypt(cidx, bk, bv, oidx);
            int good = 0; for (int i = 0; i + 1 < N; i++) good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1;
            ok += good >= 0.9 * (N - 1);
            printf("bloc %2d q=%d v=%d score=%.3f vrai=%.3f contacts=%d/%d\n", b, q, v, s / (N - 3), score(p) / (N - 3), good, N - 1);
            fflush(stdout);
        }
        printf("SUCCES %d/%d (q=%d, bruit=%.2f, R=%d, I=%d)\n", ok, nb, q, noise, R, I);
    } else {
        int c[256], n = load_letters(argv[3], c), q = n == 169 ? 13 : n == 144 ? 12 : 0;
        if (!q) return 1;
        build(q);
        int isnull = !strcmp(argv[1], "null"), nn = isnull ? atoi(argv[4]) : 1, a = isnull ? 5 : 4;
        int R = atoi(argv[a]), I = atoi(argv[a + 1]); rs = strtoull(argv[a + 2], 0, 10) * 2654435761ULL + 9;
        for (int k = 0; k < nn; k++) {
            int cc[256], bk[64], out[256], bv; memcpy(cc, c, sizeof(int) * n);
            if (isnull) for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), t = cc[i]; cc[i] = cc[j]; cc[j] = t; }
            double s = search(cc, R, I, &bv, bk);
            decrypt(cc, bk, bv, out);
            printf("%s %d score=%.4f v=%d ", isnull ? "NUL" : "REEL", k, s / (n - 3), bv);
            for (int i = 0; i < n; i++) putchar('a' + out[i]);
            putchar('\n'); fflush(stdout);
        }
    }
    return 0;
}
