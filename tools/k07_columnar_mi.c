/* K07, familles 2-3 — transposition en colonnes à clé (dernière ligne incomplète), montée avec redémarrages
   maximisant MI(1) (invariant par substitution). Voir experiments/K07_transposition_sans_langue/PREREGISTRATION.md.
   Compilation : gcc -O2 -o k07c tools/k07_columnar_mi.c -lm
   Usage :
     k07c ctrl  <texte_reserve> <n> <wmin> <wmax> <nessais> <R> <I> <graine>
     k07c solve <lettres> <wmin> <wmax> <R> <I> <graine>              (meilleur sur toutes les largeurs et les 2 sens)
     k07c null  <lettres> <wmin> <wmax> <nnull> <R> <I> <graine>
   Sens 0 (V1) : le chiffré est la suite des colonnes lues dans l'ordre de la clé ; sens 1 : opération inverse. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }
static double LOG2[4096], T0 = 0.02, T1 = 0.0005;

static double mi(const int *p, int n) {
    static int cnt[676], cx[26], cy[26];
    memset(cnt, 0, sizeof cnt); memset(cx, 0, sizeof cx); memset(cy, 0, sizeof cy);
    for (int i = 0; i + 1 < n; i++) { cnt[p[i] * 26 + p[i + 1]]++; cx[p[i]]++; cy[p[i + 1]]++; }
    double m = n - 1, s = 0;
    for (int a = 0; a < 26; a++) {
        if (!cx[a]) continue;
        for (int b = 0; b < 26; b++) {
            int c = cnt[a * 26 + b];
            if (c) s += c * (LOG2[c] + log2(m) - LOG2[cx[a]] - LOG2[cy[b]]);
        }
    }
    return s / m;
}

/* position dans le chiffré de chaque case du clair (ordre des lignes) pour la clé perm, largeur w */
static void mapping(int n, int w, const int *perm, int *pos) {
    int h = n / w, r = n % w, start[64], k = 0;
    for (int j = 0; j < w; j++) { int col = perm[j]; start[col] = k; k += h + (col < r); }
    for (int i = 0; i < n; i++) { int row = i / w, col = i % w; pos[i] = start[col] + row; }
}

static void decrypt(const int *c, int n, int w, const int *perm, int dir, int *out) {
    int pos[1024]; mapping(n, w, perm, pos);
    if (dir == 0) for (int i = 0; i < n; i++) out[i] = c[pos[i]];
    else for (int i = 0; i < n; i++) out[pos[i]] = c[i];
}

static void encrypt(const int *p, int n, int w, const int *perm, int dir, int *c) {
    int pos[1024]; mapping(n, w, perm, pos);
    if (dir == 0) for (int i = 0; i < n; i++) c[pos[i]] = p[i];
    else for (int i = 0; i < n; i++) c[i] = p[pos[i]];
}

static double climb(const int *c, int n, int w, int dir, int R, int I, int *bp) {
    int perm[64], cand[64], out[1024]; double best = -1;
    for (int r = 0; r < R; r++) {
        for (int i = 0; i < w; i++) perm[i] = i;
        for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
        decrypt(c, n, w, perm, dir, out); double cur = mi(out, n);
        for (int it = 0; it < I; it++) {
            memcpy(cand, perm, sizeof(int) * w);
            int mv = rint_(3), a = rint_(w), b = rint_(w);
            if (a == b) continue;
            if (mv == 0) { int t = cand[a]; cand[a] = cand[b]; cand[b] = t; }
            else if (mv == 1) { if (a > b) { int t = a; a = b; b = t; } while (a < b) { int t = cand[a]; cand[a] = cand[b]; cand[b] = t; a++; b--; } }
            else { int v = cand[a]; if (a < b) memmove(cand + a, cand + a + 1, sizeof(int) * (b - a)); else memmove(cand + b + 1, cand + b, sizeof(int) * (a - b)); cand[b] = v; }
            decrypt(c, n, w, cand, dir, out); double s = mi(out, n);
            double T = T0 * pow(T1 / T0, (double)it / I);   /* recuit (amendement 1) ; T0 = 0 => montée pure */
            if (s >= cur || (T0 > 0 && (rnd() >> 11) * (1.0 / 9007199254740992.0) < exp((s - cur) / T))) {
                cur = s; memcpy(perm, cand, sizeof(int) * w);
                if (cur > best) { best = cur; memcpy(bp, perm, sizeof(int) * w); }
            }
        }
        if (cur > best) { best = cur; memcpy(bp, perm, sizeof(int) * w); }
    }
    return best;
}

static double search(const int *c, int n, int wmin, int wmax, int R, int I, int *bw, int *bd, int *bp) {
    double best = -1; int perm[64];
    for (int w = wmin; w <= wmax; w++)
        for (int d = 0; d < 2; d++) {
            double s = climb(c, n, w, d, R, I, perm);
            if (s > best) { best = s; *bw = w; *bd = d; memcpy(bp, perm, sizeof(int) * w); }
        }
    return best;
}

static int load_letters(const char *s, int *out, int max) {
    int n = 0;
    for (; *s && n < max; s++) if (*s >= 'a' && *s <= 'z') out[n++] = *s - 'a'; else if (*s >= 'A' && *s <= 'Z') out[n++] = *s - 'A';
    return n;
}

int main(int argc, char **argv) {
    for (int i = 1; i < 4096; i++) LOG2[i] = log2(i);
    if (getenv("K07_T0")) T0 = atof(getenv("K07_T0"));
    if (argc < 2) return 1;
    if (!strcmp(argv[1], "ctrl")) {
        FILE *fp = fopen(argv[2], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *t = malloc(L + 1); if (fread(t, 1, L, fp) != (size_t)L) return 2; t[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(t, txt, L);
        int n = atoi(argv[3]), wmin = atoi(argv[4]), wmax = atoi(argv[5]), ne = atoi(argv[6]), R = atoi(argv[7]), I = atoi(argv[8]);
        rs = strtoull(argv[9], 0, 10) * 2654435761ULL + 5; int ok = 0;
        for (int e = 0; e < ne; e++) {
            int p[1024], c[1024], perm[64], bp[64], sub[26], bw, bd, idx[1024], cidx[1024], oidx[1024];
            for (int i = 0; i < 26; i++) sub[i] = i;
            for (int i = 25; i > 0; i--) { int j = rint_(i + 1), x = sub[i]; sub[i] = sub[j]; sub[j] = x; }
            int o = rint_(M - n); for (int i = 0; i < n; i++) p[i] = sub[txt[o + i]];
            int w = wmin + rint_(wmax - wmin + 1), d = rint_(2);
            for (int i = 0; i < w; i++) perm[i] = i;
            for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), x = perm[i]; perm[i] = perm[j]; perm[j] = x; }
            encrypt(p, n, w, perm, d, c);
            double s = search(c, n, wmin, wmax, R, I, &bw, &bd, bp);
            for (int i = 0; i < n; i++) idx[i] = i;
            encrypt(idx, n, w, perm, d, cidx); decrypt(cidx, n, bw, bp, bd, oidx);
            int good = 0; for (int i = 0; i + 1 < n; i++) good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1;   /* sens indifférent (amendement 1) */
            ok += good >= 0.9 * (n - 1);
            printf("essai %d : vrai w=%d sens=%d | trouvé w=%d sens=%d MI=%.4f (vrai %.4f) contacts=%d/%d\n", e, w, d, bw, bd, s, mi(p, n), good, n - 1);
            fflush(stdout);
        }
        printf("SUCCES %d/%d (n=%d, w=%d..%d, R=%d, I=%d)\n", ok, ne, n, wmin, wmax, R, I);
    } else {
        int c[1024], n = load_letters(argv[2], c, 1024), wmin = atoi(argv[3]), wmax = atoi(argv[4]);
        int isnull = !strcmp(argv[1], "null"), nn = isnull ? atoi(argv[5]) : 1, a = isnull ? 6 : 5;
        int R = atoi(argv[a]), I = atoi(argv[a + 1]); rs = strtoull(argv[a + 2], 0, 10) * 2654435761ULL + 11;
        for (int k = 0; k < nn; k++) {
            int cc[1024], bp[64], out[1024], bw, bd; memcpy(cc, c, sizeof(int) * n);
            if (isnull) for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), t = cc[i]; cc[i] = cc[j]; cc[j] = t; }
            double s = search(cc, n, wmin, wmax, R, I, &bw, &bd, bp);
            decrypt(cc, n, bw, bp, bd, out);
            printf("%s %d MI=%.4f w=%d sens=%d ", isnull ? "NUL" : "REEL", k, s, bw, bd);
            for (int i = 0; i < n && i < 200; i++) putchar('a' + out[i]);
            putchar('\n'); fflush(stdout);
        }
    }
    return 0;
}
