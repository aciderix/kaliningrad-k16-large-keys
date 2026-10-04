/* K08 — double transposition en colonnes (Würfel) : P -> colonnes(k1, w1) -> colonnes(k2, w2) = C.
   Recuit simulé sur les deux clés, score MI(1) (invariant par substitution). Voir experiments/K08_double_transposition/.
   Compilation : gcc -O2 -o k08 tools/k08_double_mi.c -lm
   Usage :
     k08 ctrl  <texte_reserve> <n> <wmin> <wmax> <nessais> <R> <I> <graine> [largeurs_connues 0/1]
     k08 solve <lettres> <wmin> <wmax> <R> <I> <graine>
     k08 null  <lettres> <wmin> <wmax> <nnull> <R> <I> <graine> */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }
static double rnd01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static double LOG2[4096], T0 = 0.02, T1 = 0.0005;
static int SAME = 0;   /* K14 amendement : même clé deux fois (Übchi), w2 = w1, k2 = k1 */
static float *QGQ = 0; /* si défini : score quadrigrammes au lieu de MI */

static double mi(const int *p, int n) {
    if (QGQ) { double q = 0; for (int i = 0; i + 3 < n; i++) q += QGQ[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]; return q / (n - 3); }
    static int cnt[676], cx[26], cy[26];
    memset(cnt, 0, sizeof cnt); memset(cx, 0, sizeof cx); memset(cy, 0, sizeof cy);
    for (int i = 0; i + 1 < n; i++) { cnt[p[i] * 26 + p[i + 1]]++; cx[p[i]]++; cy[p[i + 1]]++; }
    double m = n - 1, s = 0, lm = log2(m);
    for (int a = 0; a < 26; a++) {
        if (!cx[a]) continue;
        for (int b = 0; b < 26; b++) { int c = cnt[a * 26 + b]; if (c) s += c * (LOG2[c] + lm - LOG2[cx[a]] - LOG2[cy[b]]); }
    }
    return s / m;
}

/* pos[i] = position dans la sortie colonnes de la case i du texte écrit en lignes de w */
static void mapping(int n, int w, const int *perm, int *pos) {
    int h = n / w, r = n % w, start[64], k = 0;
    for (int j = 0; j < w; j++) { int col = perm[j]; start[col] = k; k += h + (col < r); }
    for (int i = 0; i < n; i++) pos[i] = start[i % w] + i / w;
}

static void decrypt2(const int *c, int n, int w1, const int *k1, int w2, const int *k2, int *out) {
    int p1[1024], p2[1024];
    mapping(n, w1, k1, p1); mapping(n, w2, k2, p2);
    /* C[p2[j]] = T[j] ; T[p1[i]] = P[i]  =>  P[i] = C[p2[p1[i]]] */
    for (int i = 0; i < n; i++) out[i] = c[p2[p1[i]]];
}

static void encrypt2(const int *p, int n, int w1, const int *k1, int w2, const int *k2, int *c) {
    int p1[1024], p2[1024];
    mapping(n, w1, k1, p1); mapping(n, w2, k2, p2);
    for (int i = 0; i < n; i++) c[p2[p1[i]]] = p[i];
}

static void randperm(int *p, int w) { for (int i = 0; i < w; i++) p[i] = i; for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), t = p[i]; p[i] = p[j]; p[j] = t; } }

static void mutate(int *k, int w) {
    int mv = rint_(3), a = rint_(w), b = rint_(w);
    if (a == b) return;
    if (mv == 0) { int t = k[a]; k[a] = k[b]; k[b] = t; }
    else if (mv == 1) { if (a > b) { int t = a; a = b; b = t; } while (a < b) { int t = k[a]; k[a] = k[b]; k[b] = t; a++; b--; } }
    else { int v = k[a]; if (a < b) memmove(k + a, k + a + 1, sizeof(int) * (b - a)); else memmove(k + b + 1, k + b, sizeof(int) * (a - b)); k[b] = v; }
}

static double anneal(const int *c, int n, int w1, int w2, int R, int I, int *b1, int *b2) {
    int k1[64], k2[64], c1[64], c2[64], out[1024]; double best = -1e18;
    for (int r = 0; r < R; r++) {
        randperm(k1, w1); randperm(k2, w2); if (SAME) memcpy(k2, k1, sizeof(int) * w1);
        decrypt2(c, n, w1, k1, w2, k2, out); double cur = mi(out, n);
        for (int it = 0; it < I; it++) {
            memcpy(c1, k1, sizeof(int) * w1); memcpy(c2, k2, sizeof(int) * w2);
            if (SAME) { mutate(c1, w1); memcpy(c2, c1, sizeof(int) * w1); }
            else if (rint_(2)) mutate(c1, w1); else mutate(c2, w2);
            decrypt2(c, n, w1, c1, w2, c2, out); double s = mi(out, n);
            double T = T0 * pow(T1 / T0, (double)it / I);
            if (s >= cur || rnd01() < exp((s - cur) / T)) {
                cur = s; memcpy(k1, c1, sizeof(int) * w1); memcpy(k2, c2, sizeof(int) * w2);
                if (cur > best) { best = cur; memcpy(b1, k1, sizeof(int) * w1); memcpy(b2, k2, sizeof(int) * w2); }
            }
        }
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
    if (getenv("K08_T0")) T0 = atof(getenv("K08_T0"));
    if (getenv("K08_SAME")) SAME = 1;
    if (getenv("K08_QG")) { QGQ = malloc(sizeof(float) * 456976); FILE *fq = fopen(getenv("K08_QG"), "rb"); if (!fq || fread(QGQ, sizeof(float), 456976, fq) != 456976) return 3; fclose(fq); T0 = 0.3; T1 = 0.005; }
    if (argc < 2) return 1;
    if (!strcmp(argv[1], "ctrl")) {
        FILE *fp = fopen(argv[2], "rb"); fseek(fp, 0, SEEK_END); long L = ftell(fp); fseek(fp, 0, SEEK_SET);
        char *t = malloc(L + 1); if (fread(t, 1, L, fp) != (size_t)L) return 2; t[L] = 0; fclose(fp);
        int *txt = malloc(sizeof(int) * (L + 1)); int M = load_letters(t, txt, L);
        int n = atoi(argv[3]), wmin = atoi(argv[4]), wmax = atoi(argv[5]), ne = atoi(argv[6]), R = atoi(argv[7]), I = atoi(argv[8]);
        int known = argc > 10 ? atoi(argv[10]) : 0;
        rs = strtoull(argv[9], 0, 10) * 2654435761ULL + 17; int ok = 0;
        for (int e = 0; e < ne; e++) {
            int p[1024], c[1024], k1[64], k2[64], b1[64], b2[64], idx[1024], cidx[1024], oidx[1024], sub[26];
            randperm(sub, 26); if (QGQ) for (int i = 0; i < 26; i++) sub[i] = i;   /* score allemand : lettres intactes */
            int o = rint_(M - n); for (int i = 0; i < n; i++) p[i] = sub[txt[o + i]];
            int w1 = wmin + rint_(wmax - wmin + 1), w2 = wmin + rint_(wmax - wmin + 1);
            if (SAME) w2 = w1;
            randperm(k1, w1); randperm(k2, w2); if (SAME) memcpy(k2, k1, sizeof(int) * w1); encrypt2(p, n, w1, k1, w2, k2, c);
            double best = -1e18; int bw1 = 0, bw2 = 0, t1[64], t2[64];
            for (int a = (known ? w1 : wmin); a <= (known ? w1 : wmax); a++)
                for (int b = (known ? w2 : wmin); b <= (known ? w2 : wmax); b++) { if (SAME && b != a) continue;
                    double s = anneal(c, n, a, b, R, I, t1, t2);
                    if (s > best) { best = s; bw1 = a; bw2 = b; memcpy(b1, t1, sizeof t1); memcpy(b2, t2, sizeof t2); }
                }
            for (int i = 0; i < n; i++) idx[i] = i;
            encrypt2(idx, n, w1, k1, w2, k2, cidx); decrypt2(cidx, n, bw1, b1, bw2, b2, oidx);
            int good = 0; for (int i = 0; i + 1 < n; i++) good += oidx[i + 1] == oidx[i] + 1 || oidx[i + 1] == oidx[i] - 1;
            ok += good >= 0.9 * (n - 1);
            printf("essai %d : vrai w=%d,%d | trouvé w=%d,%d MI=%.4f (vrai %.4f) contacts=%d/%d\n", e, w1, w2, bw1, bw2, best, mi(p, n), good, n - 1);
            fflush(stdout);
        }
        printf("SUCCES %d/%d (n=%d, w=%d..%d, R=%d, I=%d, largeurs %s)\n", ok, ne, n, wmin, wmax, R, I, known ? "connues" : "cherchées");
    } else {
        int c[1024], n = load_letters(argv[2], c, 1024), wmin = atoi(argv[3]), wmax = atoi(argv[4]);
        int isnull = !strcmp(argv[1], "null"), nn = isnull ? atoi(argv[5]) : 1, a0 = isnull ? 6 : 5;
        int R = atoi(argv[a0]), I = atoi(argv[a0 + 1]); rs = strtoull(argv[a0 + 2], 0, 10) * 2654435761ULL + 19;
        for (int k = 0; k < nn; k++) {
            int cc[1024], out[1024], b1[64], b2[64], t1[64], t2[64], bw1 = 0, bw2 = 0; double best = -1e18;
            memcpy(cc, c, sizeof(int) * n);
            if (isnull) for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), t = cc[i]; cc[i] = cc[j]; cc[j] = t; }
            for (int a = wmin; a <= wmax; a++)
                for (int b = wmin; b <= wmax; b++) { if (SAME && b != a) continue;
                    double s = anneal(cc, n, a, b, R, I, t1, t2);
                    if (s > best) { best = s; bw1 = a; bw2 = b; memcpy(b1, t1, sizeof t1); memcpy(b2, t2, sizeof t2); }
                }
            decrypt2(cc, n, bw1, b1, bw2, b2, out);
            printf("%s %d MI=%.4f w=%d,%d ", isnull ? "NUL" : "REEL", k, best, bw1, bw2);
            for (int i = 0; i < n && i < 200; i++) putchar('a' + out[i]);
            putchar('\n'); fflush(stdout);
        }
    }
    return 0;
}
