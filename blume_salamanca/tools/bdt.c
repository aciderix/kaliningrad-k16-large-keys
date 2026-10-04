/* bdt.c — double transposition directe (BLUME SALAMANCA) : deux télégrammes chiffrés avec les mêmes clés K1, K2.
   Conventions identiques à dct_reloaded/tools/dct_solver.c : mapping(n, w, perm) avec perm[j] = colonne lue en j-ième,
   colonnes longues = indices < n % w ; C[pos[i]] = I[i].
   L'IDP (potentiel digraphique de Lasry, Kopal & Wacker 2014) suit CrypTool 2 IDPAnalyser.cs (Apache 2.0) :
   plages exactes de fin de colonne, fenêtre glissante, score de matrice par chaîne gloutonne.
   Modes :
     probe  qg.bin texte n1 n2 w1 w2 graine        sonde du paysage (clé vraie, clés perturbées, clés aléatoires)
   Compilation : gcc -O3 -march=native -fopenmp -o bdt tools/bdt.c -lm */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAXN 1024
#define MAXW 64
static float QG[456976]; static float BG[676]; static float TG[17576]; static float Q4[456976]; static int FIT = 0, KTOP = 6;
static _Thread_local unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int rint_(int n) { return (int)(rnd() % (unsigned long long)n); }
static double rnd01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

static void mapping(int n, int w, const int *perm, int *pos) {
    int h = n / w, r = n % w, start[MAXW], k = 0;
    for (int j = 0; j < w; j++) { int col = perm[j]; start[col] = k; k += h + (col < r); }
    for (int i = 0; i < n; i++) pos[i] = start[i % w] + i / w;
}
static void encrypt2(const int *p, int n, int w1, const int *k1, int w2, const int *k2, int *c) {
    int p1[MAXN], p2[MAXN], t[MAXN]; mapping(n, w1, k1, p1); mapping(n, w2, k2, p2);
    for (int i = 0; i < n; i++) t[p1[i]] = p[i];
    for (int j = 0; j < n; j++) c[p2[j]] = t[j];
}
static void undo(const int *c, int n, int w, const int *k, int *t) { int p[MAXN]; mapping(n, w, k, p); for (int j = 0; j < n; j++) t[j] = c[p[j]]; }
static double quad(const int *p, int n) { double s = 0; for (int i = 0; i + 3 < n; i++) s += QG[((p[i] * 26 + p[i + 1]) * 26 + p[i + 2]) * 26 + p[i + 3]]; return s / (n - 3); }

/* Plages de fin de colonne de K1 (inconnue) pour un texte de n lettres et une largeur w. */
typedef struct { int n, w, full, mine[MAXW], maxe[MAXW]; } Geo;
static void geo_init(Geo *g, int n, int w) {
    int full = n / w, nl = n % w; g->n = n; g->w = w; g->full = full;
    for (int i = 0; i < w; i++) { g->mine[i] = full * (i + 1) - 1; g->maxe[i] = (i < nl) ? full * (i + 1) + i : g->mine[i] + nl; }
    for (int i = 0; i < w; i++) {
        int idx = w - 1 - i;
        if (g->maxe[idx] > n - 1 - full * i) g->maxe[idx] = n - 1 - full * i;
        if (i < nl) { int v = n - 1 - full * i - i; if (g->mine[idx] < v) g->mine[idx] = v; }
        else { int v = g->maxe[idx] - nl; if (g->mine[idx] < v) g->mine[idx] = v; }
    }
}
static double chain_score(float m[MAXW][MAXW], int d) {
    int left[MAXW], right[MAXW]; for (int i = 0; i < d; i++) left[i] = right[i] = -1;
    double sum = 0;
    for (int it = 1; it <= d; it++) {
        float best = -1e30f; int b1 = -1, b2 = -1;
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
/* Matrice des meilleurs appariements de colonnes de K1 (moyenne par rangée). */
static _Thread_local short PA[MAXW][MAXW], PB[MAXW][MAXW];   /* débuts de fenêtre du meilleur alignement */
static void pair_matrix_raw(const int *t, const Geo *g, float m[MAXW][MAXW], int raw) {
    int n = g->n, w = g->w, full = g->full;
    for (int c1 = 0; c1 < w; c1++) for (int c2 = 0; c2 < w; c2++) {
        if (c1 == c2) { m[c1][c2] = -1e30f; continue; }
        float best = -1e30f;
        if (n % w == 0) {
            int p1 = g->mine[c1], p2 = g->mine[c2]; float s = 0;
            for (int l = 0; l < full; l++) s += BG[t[p1 - l] * 26 + t[p2 - l]];
            best = s; PA[c1][c2] = p1 - full + 1; PB[c1][c2] = p2 - full + 1;
        } else {
            int s1 = g->mine[c1] - full + 1, s2 = g->mine[c2] - full + 1, o1 = g->maxe[c1] - g->mine[c1], o2 = g->maxe[c2] - g->mine[c2];
            for (int pass = 0; pass < 2; pass++) {
                int omax = pass == 0 ? o2 : o1;
                for (int off = pass; off <= omax; off++) {
                    int a = s1 + (pass ? off : 0), b = s2 + (pass ? 0 : off); float s = 0;
                    if (a < 0 || b < 0 || a + full > n || b + full > n) continue;
                    for (int i = 0; i < full; i++) s += BG[t[a + i] * 26 + t[b + i]];
                    if (s > best) { best = s; PA[c1][c2] = a; PB[c1][c2] = b; }
                    int q1 = a + full, q2 = b + full, k = 0;
                    while (q1 <= g->maxe[c1] && q2 <= g->maxe[c2]) { s += BG[t[q1] * 26 + t[q2]] - BG[t[a + k] * 26 + t[b + k]]; k++; q1++; q2++; if (s > best) { best = s; PA[c1][c2] = a + k; PB[c1][c2] = b + k; } }
                }
            }
        }
        m[c1][c2] = raw ? best : best / full;
    }
}
static void pair_matrix(const int *t, const Geo *g, float m[MAXW][MAXW]) { pair_matrix_raw(t, g, m, 0); }
static double idp2(const int *t, const Geo *g) { float m[MAXW][MAXW]; pair_matrix(t, g, m); return chain_score(m, g->w); }

/* IDP par triplets (BDT_FIT=3) : pour chaque colonne a, meilleur triplet a→b→c parmi les 4 meilleurs partenaires
   (matrice de bigrammes), noté par trigrammes rangée par rangée avec les alignements trouvés. */
static double idp3(const int *t, const Geo *g) {
    float m[MAXW][MAXW]; pair_matrix_raw(t, g, m, 0); int w = g->w, full = g->full, n = g->n, K = 4, top[MAXW][4];
    for (int a = 0; a < w; a++) { for (int k = 0; k < K; k++) top[a][k] = -1;
        for (int b = 0; b < w; b++) { if (b == a) continue; float v = m[a][b]; int k = K - 1; if (top[a][k] >= 0 && m[a][top[a][k]] >= v) continue;
            while (k > 0 && (top[a][k - 1] < 0 || m[a][top[a][k - 1]] < v)) { top[a][k] = top[a][k - 1]; k--; } top[a][k] = b; } }
    double sum = 0;
    for (int a = 0; a < w; a++) { double best = -1e30;
        for (int i1 = 0; i1 < K; i1++) { int b = top[a][i1]; if (b < 0) continue;
            for (int i2 = 0; i2 < K; i2++) { int c = top[b][i2]; if (c < 0 || c == a) continue;
                int pa = PA[a][b], pb = PB[a][b], d = PB[b][c] - PA[b][c]; double s = 0; int cnt = 0;
                for (int i = 0; i < full; i++) { int x = pa + i, y = pb + i, z = y + d; if (z < 0 || z >= n) continue; s += TG[(t[x] * 26 + t[y]) * 26 + t[z]]; cnt++; }
                if (cnt) { s /= cnt; if (s > best) best = s; } } }
        sum += best; }
    return sum / w;
}

/* Chaînes de 4 colonnes (BDT_FIT=4) : candidats = KTOP meilleurs partenaires par bigrammes, chaînes a→b→c→d notées
   rangée par rangée par quadrigrammes (corrélation totale) ; score de a = meilleure chaîne ; moyenne sur a. */
static double idp4(const int *t, const Geo *g) {
    float m[MAXW][MAXW]; pair_matrix_raw(t, g, m, 0); int w = g->w, full = g->full, n = g->n, K = KTOP < w - 1 ? KTOP : w - 1, top[MAXW][16];
    for (int a = 0; a < w; a++) { int used[MAXW] = {0}; used[a] = 1;
        for (int k = 0; k < K; k++) { int bb = -1; for (int b = 0; b < w; b++) if (!used[b] && (bb < 0 || m[a][b] > m[a][bb])) bb = b; top[a][k] = bb; used[bb] = 1; } }
    double sum = 0;
    for (int a = 0; a < w; a++) { double best = -1e30;
        for (int i1 = 0; i1 < K; i1++) { int b = top[a][i1]; int dab = PB[a][b] - PA[a][b], pa = PA[a][b];
            for (int i2 = 0; i2 < K; i2++) { int c = top[b][i2]; if (c == a) continue; int dbc = PB[b][c] - PA[b][c];
                for (int i3 = 0; i3 < K; i3++) { int d = top[c][i3]; if (d == a || d == b) continue; int dcd = PB[c][d] - PA[c][d];
                    double s = 0; int cnt = 0;
                    for (int i = 0; i < full; i++) { int x = pa + i, y = x + dab, z = y + dbc, u = z + dcd;
                        if (y < 0 || y >= n || z < 0 || z >= n || u < 0 || u >= n) continue;
                        s += Q4[((t[x] * 26 + t[y]) * 26 + t[z]) * 26 + t[u]]; cnt++; }
                    if (cnt > full / 2) { s /= cnt; if (s > best) best = s; } } } }
        sum += best; }
    return sum / w;
}
static double idp(const int *t, const Geo *g) { return FIT == 4 ? idp4(t, g) : FIT == 3 ? idp3(t, g) : idp2(t, g); }


/* Balayage des écarts (Bourdeau, lagscan.py) : pour chaque écart L = 1..n-16 et chaque ordre, somme des bigrammes
   BG(c[i], c[i+L]) normalisée contre des paires tirées des fréquences du texte ; renvoie le z maximal. */
static double lagscan(const int *c, int n) {
    double f[26] = {0}; for (int i = 0; i < n; i++) f[c[i]] += 1.0 / n;
    double mu = 0, m2 = 0; for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double v = BG[a * 26 + b]; mu += f[a] * f[b] * v; m2 += f[a] * f[b] * v * v; }
    double var = m2 - mu * mu, best = -1e9;
    for (int L = 1; L <= n - 16; L++) for (int o = 0; o < 2; o++) {
        double s = 0; int m = n - L;
        for (int i = 0; i < m; i++) s += o ? BG[c[i + L] * 26 + c[i]] : BG[c[i] * 26 + c[i + L]];
        double z = (s - m * mu) / sqrt(m * var); if (z > best) best = z;
    }
    return best;
}

static void randperm(int *p, int w) { for (int i = 0; i < w; i++) p[i] = i; for (int i = w - 1; i > 0; i--) { int j = rint_(i + 1), x = p[i]; p[i] = p[j]; p[j] = x; } }


/* ---- Recherche de K2 : recuit sur l'IDP conjointe des messages (mêmes clés). ---- */
typedef struct { const int *c; int n; Geo g; double wt; } Msg;
static int JOINT = 0, RCMODE = 0, TIES = 0;   /* BDT_TIES=1 : ex aequo numérotés de droite à gauche */
static int JOINT_UNUSED = 0;   /* BDT_RC=1 : convention lignes-puis-colonnes, I = F_K2(C) */
static void fwdT(const int *x, int n, int w, const int *k, int *out);
static void undoK2(const int *c, int n, int w, const int *k, int *t) { if (RCMODE) fwdT(c, n, w, k, t); else undo(c, n, w, k, t); }   /* BDT_JOINT=1 : matrice d'appariement commune (sommes des rangées des deux messages) */
static double fitness(const Msg *m, int nm, int w2, const int *k) {
    int t[MAXN]; double s = 0;
    if (JOINT && nm == 2) {
        float a[MAXW][MAXW], b[MAXW][MAXW]; int w1 = m[0].g.w; double den = m[0].g.full + m[1].wt * m[1].g.full;
        undoK2(m[0].c, m[0].n, w2, k, t); pair_matrix_raw(t, &m[0].g, a, 1);
        undoK2(m[1].c, m[1].n, w2, k, t); pair_matrix_raw(t, &m[1].g, b, 1);
        for (int i = 0; i < w1; i++) for (int j = 0; j < w1; j++) a[i][j] = (float)((a[i][j] + m[1].wt * b[i][j]) / den);
        return chain_score(a, w1);
    }
    for (int i = 0; i < nm; i++) { undoK2(m[i].c, m[i].n, w2, k, t); s += m[i].wt * idp(t, &m[i].g); }
    return s;
}
static int MV[7] = {40, 55, 70, 85, 92, 96, 100};   /* seuils cumulés : même longueur, quelconque, glissement, blocs, bloc glissé, pivot */
static void move(int *k, int w, int n1) {
    int r = rint_(100), rr = n1 % w, tmp[MAXW];
    if (r < MV[0] && rr) {                 /* échange de deux colonnes de même longueur (bornes inchangées) */
        int a, b, tries = 0; do { a = rint_(w); b = rint_(w); } while ((a == b || ((k[a] < rr) != (k[b] < rr))) && ++tries < 100);
        int x = k[a]; k[a] = k[b]; k[b] = x;
    } else if (r < MV[1]) { int a = rint_(w), b = rint_(w), x = k[a]; k[a] = k[b]; k[b] = x; }
    else if (r < MV[2]) {                  /* glissement d'une colonne dans l'ordre de lecture */
        int a = rint_(w), b = rint_(w), v = k[a];
        if (a < b) memmove(k + a, k + a + 1, sizeof(int) * (b - a)); else if (a > b) memmove(k + b + 1, k + b, sizeof(int) * (a - b)); k[b] = v;
    } else if (r < MV[3]) {                /* échange de deux blocs disjoints de même longueur */
        int l = 1 + rint_(w / 2), a = rint_(w - 2 * l + 1), b = a + l + rint_(w - a - 2 * l + 1);
        for (int i = 0; i < l; i++) { int x = k[a + i]; k[a + i] = k[b + i]; k[b + i] = x; }
    } else if (r < MV[4]) {                /* déplacement d'un bloc */
        int l = 1 + rint_(w - 1), a = rint_(w - l + 1), b = rint_(w - l + 1); if (a == b) return;
        int blk[MAXW]; memcpy(blk, k + a, sizeof(int) * l); int m = 0;
        for (int i = 0; i < w; i++) if (i < a || i >= a + l) tmp[m++] = k[i];
        memcpy(k, tmp, sizeof(int) * b); memcpy(k + b, blk, sizeof(int) * l); memcpy(k + b + l, tmp + b, sizeof(int) * (w - l - b));
    } else if (r < MV[5]) { int p = 1 + rint_(w - 1); memcpy(tmp, k, sizeof(int) * w); memcpy(k, tmp + p, sizeof(int) * (w - p)); memcpy(k + w - p, tmp, sizeof(int) * p); }
    else { int sh = 1 + rint_(w - 1); for (int j = 0; j < w; j++) k[j] = (k[j] + sh) % w; }   /* décalage des indices : I décalé */
}
/* Part des lettres de I bien placées (à un décalage global près) : mesure de proximité à la vraie K2. */
static double closeness(int n, int w, const int *k, const int *truek) {
    int a[MAXN], b[MAXN], best = 0; mapping(n, w, k, a); mapping(n, w, truek, b);
    for (int s = -w; s <= w; s++) { int c = 0; for (int p = 0; p < n; p++) { int q = p + s; if (q >= 0 && q < n && a[p] == b[q]) c++; } if (c > best) best = c; }
    return (double)best / n;
}
static double anneal(const Msg *m, int nm, int w2, long iters, double T0, double T1, int *best) {
    int k[MAXW], q[MAXW]; randperm(k, w2); double cur = fitness(m, nm, w2, k), bs = cur; memcpy(best, k, sizeof(int) * w2);
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        memcpy(q, k, sizeof(int) * w2); move(q, w2, m[0].n); double s = fitness(m, nm, w2, q);
        if (s >= cur || rnd01() < exp((s - cur) / T)) { cur = s; memcpy(k, q, sizeof(int) * w2); if (cur > bs) { bs = cur; memcpy(best, k, sizeof(int) * w2); } }
    }
    return bs;
}


/* ---- Étape K1 : K2 connue, recuit sur K1 noté par les quadrigrammes des deux clairs. ---- */
static void mutate1(int *k, int w) {
    int a = rint_(w), b = rint_(w); if (a == b) return; int mv = rint_(3);
    if (mv == 0) { int x = k[a]; k[a] = k[b]; k[b] = x; }
    else if (mv == 1) { if (a > b) { int x = a; a = b; b = x; } while (a < b) { int x = k[a]; k[a] = k[b]; k[b] = x; a++; b--; } }
    else { int v = k[a]; if (a < b) memmove(k + a, k + a + 1, sizeof(int) * (b - a)); else memmove(k + b + 1, k + b, sizeof(int) * (a - b)); k[b] = v; }
}
static double k1score(const int *const *I, const int *ns, int nm, int w1, const int *k, int *out0) {
    double s = 0; int tot = 0, p[MAXN];
    for (int m = 0; m < nm; m++) { undo(I[m], ns[m], w1, k, p); s += quad(p, ns[m]) * (ns[m] - 3); tot += ns[m] - 3; if (m == 0 && out0) memcpy(out0, p, sizeof(int) * ns[0]); }
    return s / tot;
}
static double solve_k1(const int *const *I, const int *ns, int nm, int w1, int R, long iters, int *bk) {
    double best = -1e18;
    for (int r = 0; r < R; r++) {
        int k[MAXW], q[MAXW]; randperm(k, w1); double cur = k1score(I, ns, nm, w1, k, 0), lb = cur; int lk[MAXW]; memcpy(lk, k, sizeof(int) * w1);
        for (long it = 0; it < iters; it++) {
            double T = 0.3 * pow(0.005 / 0.3, (double)it / iters);
            memcpy(q, k, sizeof(int) * w1); mutate1(q, w1); double v = k1score(I, ns, nm, w1, q, 0);
            if (v >= cur || rnd01() < exp((v - cur) / T)) { cur = v; memcpy(k, q, sizeof(int) * w1); if (cur > lb) { lb = cur; memcpy(lk, k, sizeof(int) * w1); } }
        }
        if (lb > best) { best = lb; memcpy(bk, lk, sizeof(int) * w1); }
    }
    return best;
}

/* ---- Optimisation alternée (BDT_ALT=1) : chaîne de K1 figée (voisins + fenêtres d'alignement de la meilleure K2),
   recuit rapide de K2 contre cette chaîne, puis nouvelle chaîne. ---- */
static void chain_links(float m[MAXW][MAXW], int d, int *right) {
    int left[MAXW]; for (int i = 0; i < d; i++) left[i] = right[i] = -1;
    for (int it = 1; it <= d; it++) {
        float best = -1e30f; int b1 = -1, b2 = -1;
        for (int p1 = 0; p1 < d; p1++) {
            if (right[p1] != -1) continue;
            int head = p1; if (it != d) while (left[head] != -1) head = left[head];
            for (int p2 = 0; p2 < d; p2++) { if (left[p2] != -1 || (it != d && head == p2) || p1 == p2) continue; if (m[p1][p2] > best) { best = m[p1][p2]; b1 = p1; b2 = p2; } }
        }
        if (b1 != -1) { left[b2] = b1; right[b1] = b2; }
    }
}
typedef struct { int na; short a[2 * MAXW * 64], b[2 * MAXW * 64]; unsigned char msg[2 * MAXW * 64]; } Links;   /* paires de positions de I */
static void build_links(const Msg *m, int nm, int w2, const int *k, Links *L) {
    L->na = 0; int t[MAXN]; float mat[MAXW][MAXW]; int right[MAXW];
    for (int q = 0; q < nm; q++) {
        undo(m[q].c, m[q].n, w2, k, t); pair_matrix_raw(t, &m[q].g, mat, 0);
        if (q == 0 || !JOINT) chain_links(mat, m[q].g.w, right);   /* la même chaîne de K1 sert aux deux messages */
        for (int a = 0; a < m[q].g.w; a++) { int b = right[a]; if (b < 0) continue;
            for (int i = 0; i < m[q].g.full; i++) { L->a[L->na] = PA[a][b] + i; L->b[L->na] = PB[a][b] + i; L->msg[L->na] = q; L->na++; } }
    }
}
static double link_score(const Msg *m, int nm, int w2, const int *k, const Links *L) {
    int t[2][MAXN]; double s = 0;
    for (int q = 0; q < nm; q++) undo(m[q].c, m[q].n, w2, k, t[q]);
    for (int i = 0; i < L->na; i++) { int q = L->msg[i]; s += (q ? m[1].wt : 1.0) * BG[t[q][L->a[i]] * 26 + t[q][L->b[i]]]; }
    return s;
}
static long ALT_IN = 20000; static int ALT_OUT = 50;
static double alt_search(const Msg *m, int nm, int w2, double T0, double T1, int *best) {
    int k[MAXW], q[MAXW]; static _Thread_local Links L; randperm(k, w2);
    double bestf = fitness(m, nm, w2, k); memcpy(best, k, sizeof(int) * w2);
    for (int outer = 0; outer < ALT_OUT; outer++) {
        build_links(m, nm, w2, k, &L);
        double cur = link_score(m, nm, w2, k, &L);
        for (long it = 0; it < ALT_IN; it++) {
            double T = T0 * pow(T1 / T0, (double)it / ALT_IN);
            memcpy(q, k, sizeof(int) * w2); move(q, w2, m[0].n); double v = link_score(m, nm, w2, q, &L);
            if (v >= cur || rnd01() < exp((v - cur) / T)) { cur = v; memcpy(k, q, sizeof(int) * w2); }
        }
        double f = fitness(m, nm, w2, k);
        if (f > bestf) { bestf = f; memcpy(best, k, sizeof(int) * w2); } else if (rnd01() < 0.5) memcpy(k, best, sizeof(int) * w2);
    }
    return bestf;
}

/* Finition : montée la plus raide sur le voisinage complet (décalages d'indices, échanges, glissements). */
static double polish(const Msg *m, int nm, int w2, int *k, double cur) {
    int q[MAXW], bq[MAXW];
    for (int pass = 0; pass < 60; pass++) {
        double best = cur; int found = 0;
        for (int sh = 1; sh < w2; sh++) { for (int j = 0; j < w2; j++) q[j] = (k[j] + sh) % w2; double v = fitness(m, nm, w2, q); if (v > best) { best = v; memcpy(bq, q, sizeof(int) * w2); found = 1; } }
        for (int a = 0; a < w2; a++) for (int b = a + 1; b < w2; b++) { memcpy(q, k, sizeof(int) * w2); int x = q[a]; q[a] = q[b]; q[b] = x; double v = fitness(m, nm, w2, q); if (v > best) { best = v; memcpy(bq, q, sizeof(int) * w2); found = 1; } }
        for (int a = 0; a < w2; a++) for (int b = 0; b < w2; b++) if (a != b) { memcpy(q, k, sizeof(int) * w2); int v0 = q[a];
            if (a < b) memmove(q + a, q + a + 1, sizeof(int) * (b - a)); else memmove(q + b + 1, q + b, sizeof(int) * (a - b)); q[b] = v0;
            double v = fitness(m, nm, w2, q); if (v > best) { best = v; memcpy(bq, q, sizeof(int) * w2); found = 1; } }
        if (!found) break; cur = best; memcpy(k, bq, sizeof(int) * w2);
    }
    return cur;
}
/* Recuit puis recherche locale itérée (perturbation de 2 à 4 mouvements + finition, acceptée si meilleure). */
static long ILS = 0;
static int ALT = 0;
static double anneal_ils(const Msg *m, int nm, int w2, long iters, double T0, double T1, int *best) {
    double v = ALT ? alt_search(m, nm, w2, T0, T1, best) : anneal(m, nm, w2, iters, T0, T1, best);
    v = polish(m, nm, w2, best, v);
    for (long r = 0; r < ILS; r++) {
        int q[MAXW]; memcpy(q, best, sizeof(int) * w2); int nk = 2 + rint_(3); for (int i = 0; i < nk; i++) move(q, w2, m[0].n);
        double u = polish(m, nm, w2, q, fitness(m, nm, w2, q));
        if (u > v) { v = u; memcpy(best, q, sizeof(int) * w2); }
    }
    return v;
}

/* ---- Clé unique (K1 = K2, type ÜBCHI) : recuit sur K, note = quadrigrammes des clairs complets (T1 + T2). ---- */
static double same_score(const int *const *C, const int *ns, int nm, int w, const int *k) {
    double s = 0; int tot = 0, t[MAXN], p[MAXN];
    for (int q = 0; q < nm; q++) { undo(C[q], ns[q], w, k, t); undo(t, ns[q], w, k, p); s += quad(p, ns[q]) * (ns[q] - 3); tot += ns[q] - 3; }
    return s / tot;
}
static double same_anneal(const int *const *C, const int *ns, int nm, int w, long iters, double T0, double T1, int *best) {
    int k[MAXW], q[MAXW]; randperm(k, w); double cur = same_score(C, ns, nm, w, k), bs = cur; memcpy(best, k, sizeof(int) * w);
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        memcpy(q, k, sizeof(int) * w); move(q, w, ns[0]); double v = same_score(C, ns, nm, w, q);
        if (v >= cur || rnd01() < exp((v - cur) / T)) { cur = v; memcpy(k, q, sizeof(int) * w); if (cur > bs) { bs = cur; memcpy(best, k, sizeof(int) * w); } }
    }
    return bs;
}

/* ---- Conventions « faciles » (BDT : lagscan2) ----
   F_K = colonne directe (écrire en lignes, lire les colonnes dans l'ordre de K) ; G_K = F_K⁻¹ (écrire en colonnes, lire en lignes).
   inversée (G∘G) : C = G_K2(G_K1(P))  ⇒  J = F_K2(C) = G_K1(P)
   mixte colonnes-puis-lignes : C = F_K2(G_K1(P))  ⇒  J = F_K2⁻¹(C) = G_K1(P)
   Dans les deux cas J = G_K1(P) : les voisins du clair sont à l'écart w1 dans J, quel que soit K1, et P = F_K1(J). */
static void fwdT(const int *x, int n, int w, const int *k, int *out) { int pos[MAXN]; mapping(n, w, k, pos); for (int i = 0; i < n; i++) out[pos[i]] = x[i]; }
static double LT0 = 2.0, LT1 = 0.05; static int CONV = 0;   /* 0 : inversée (J = F_K2(C)) ; 1 : mixte colonnes-puis-lignes (J = F_K2⁻¹(C)) */
static double lagfit_cr(const int *const *C, const int *ns, int nm, int w1, int w2, const int *k) {
    /* convention colonnes-puis-lignes, tolérante aux bornes : segments de C d'après K2, lien colonne c → c + w1 (mod w2)
       avec décalage de rangée ρ = ⌊(c + w1)/w2⌋, meilleur de ρ−1, ρ, ρ+1 */
    double s = 0;
    for (int q = 0; q < nm; q++) {
        int n = ns[q], h = n / w2, r = n % w2, start[MAXW], len[MAXW], pos = 0;
        for (int j = 0; j < w2; j++) { int col = k[j]; start[col] = pos; len[col] = h + (col < r); pos += len[col]; }
        for (int c = 0; c < w2; c++) {
            int c2 = (c + w1) % w2, rho = (c + w1) / w2; double best = -1e18;
            for (int d = -1; d <= 1; d++) { double t = 0; int cnt = 0, sh = rho + d;
                for (int R = 0; R < len[c]; R++) { int R2 = R + sh; if (R2 < 0 || R2 >= len[c2]) continue; t += BG[C[q][start[c] + R] * 26 + C[q][start[c2] + R2]]; cnt++; }
                if (cnt && t > best) best = t; }
            if (best > -1e17) s += best;
        }
    }
    return s;
}
static double lagfit(const int *const *C, const int *ns, int nm, int w1, int w2, const int *k) {
    if (CONV == 2) return lagfit_cr(C, ns, nm, w1, w2, k);
    double s = 0; int J[MAXN];
    for (int q = 0; q < nm; q++) { if (CONV == 0) fwdT(C[q], ns[q], w2, k, J); else undo(C[q], ns[q], w2, k, J);
        for (int i = 0; i + w1 < ns[q]; i++) s += BG[J[i] * 26 + J[i + w1]]; }
    return s;
}
static double lag_polish(const int *const *C, const int *ns, int nm, int w1, int w2, int *k) {
    int q[MAXW], bq[MAXW]; double cur = lagfit(C, ns, nm, w1, w2, k);
    for (int pass = 0; pass < 200; pass++) { double best = cur; int found = 0;
        for (int a = 0; a < w2; a++) for (int b = a + 1; b < w2; b++) { memcpy(q, k, sizeof(int) * w2); int x = q[a]; q[a] = q[b]; q[b] = x; double v = lagfit(C, ns, nm, w1, w2, q); if (v > best) { best = v; memcpy(bq, q, sizeof(int) * w2); found = 1; } }
        for (int a = 0; a < w2; a++) for (int b = 0; b < w2; b++) if (a != b) { memcpy(q, k, sizeof(int) * w2); int v0 = q[a];
            if (a < b) memmove(q + a, q + a + 1, sizeof(int) * (b - a)); else memmove(q + b + 1, q + b, sizeof(int) * (a - b)); q[b] = v0;
            double v = lagfit(C, ns, nm, w1, w2, q); if (v > best) { best = v; memcpy(bq, q, sizeof(int) * w2); found = 1; } }
        if (!found) break; cur = best; memcpy(k, bq, sizeof(int) * w2); }
    return cur;
}

static double lag_anneal(const int *const *C, const int *ns, int nm, int w1, int w2, long iters, double T0, double T1, int *best) {
    int k[MAXW], q[MAXW]; randperm(k, w2); double cur = lagfit(C, ns, nm, w1, w2, k), bs = cur; memcpy(best, k, sizeof(int) * w2);
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        memcpy(q, k, sizeof(int) * w2); move(q, w2, ns[0]); double v = lagfit(C, ns, nm, w1, w2, q);
        if (v >= cur || rnd01() < exp((v - cur) / T)) { cur = v; memcpy(k, q, sizeof(int) * w2); if (cur > bs) { bs = cur; memcpy(best, k, sizeof(int) * w2); } }
    }
    return bs;
}

/* Étape K1 commune aux conventions faciles : P = F_K1(J) ; recuit aux quadrigrammes sur T1 (+ T2). */
static double k1stage_fwd(const int *J1, const int *J2, int n1, int n2, int w1, int restarts, long iters, int *bk1) {
    double bq = -1e18; int P1[MAXN], P2[MAXN];
    for (int r = 0; r < restarts; r++) { int k[MAXW], q[MAXW]; randperm(k, w1); double cur = -1e18;
        for (long it = 0; it < iters; it++) { double T = 0.3 * pow(0.005 / 0.3, (double)it / iters);
            memcpy(q, k, sizeof(int) * w1); if (it) mutate1(q, w1); fwdT(J1, n1, w1, q, P1); double v = quad(P1, n1);
            if (n2) { fwdT(J2, n2, w1, q, P2); v = (v * (n1 - 3) + quad(P2, n2) * (n2 - 3)) / (n1 + n2 - 6); }
            if (v >= cur || rnd01() < exp((v - cur) / T)) { cur = v; memcpy(k, q, sizeof(int) * w1); if (cur > bq) { bq = cur; memcpy(bk1, k, sizeof(int) * w1); } } } }
    return bq;
}
static int gcdi(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
/* colonnes-puis-lignes : rotations relatives des cycles c → c + w1 (mod w2) quand pgcd(w1, w2) > 1 ; garde la meilleure par K1 */
static void cr_rotations(const int *C1, const int *C2, int n1, int n2, int w1, int w2, int *k) {
    int g = gcdi(w1, w2), m = w2 / g; if (g == 1) return;
    int cyc[MAXW][MAXW], seg_of[MAXW], vis[MAXW] = {0}, nc = 0;
    for (int j = 0; j < w2; j++) seg_of[k[j]] = j;
    for (int c0 = 0; c0 < w2; c0++) if (!vis[c0]) { int c = c0; for (int i = 0; i < m; i++) { cyc[nc][i] = c; vis[c] = 1; c = (c + w1) % w2; } nc++; }
    long combos = 1; for (int t = 1; t < nc; t++) { combos *= m; if (combos > 400) { combos = 400; break; } }
    double bestq = -1e18; int bestk[MAXW]; memcpy(bestk, k, sizeof(int) * w2);
    for (long cb = 0; cb < combos; cb++) {
        int rot[MAXW] = {0}; long x = cb; for (int t = 1; t < nc; t++) { rot[t] = (combos == 400 && nc > 3) ? rint_(m) : (int)(x % m); x /= m; }
        int ns_of[MAXW], kn[MAXW];
        for (int t = 0; t < nc; t++) for (int i = 0; i < m; i++) ns_of[cyc[t][i]] = seg_of[cyc[t][(i + rot[t]) % m]];
        for (int c = 0; c < w2; c++) kn[ns_of[c]] = c;
        int J1[MAXN], J2[MAXN], k1[MAXW]; undo(C1, n1, w2, kn, J1); if (n2) undo(C2, n2, w2, kn, J2);
        double q = k1stage_fwd(J1, J2, n1, n2, w1, 2, 40000, k1);
        if (q > bestq) { bestq = q; memcpy(bestk, kn, sizeof(int) * w2); }
    }
    memcpy(k, bestk, sizeof(int) * w2);
}

static int load_letters_file(const char *path, int *out, int max) {
    FILE *f = fopen(path, "r"); if (!f) return -1; int n = 0, ch;
    while ((ch = fgetc(f)) != EOF && n < max) { if (ch >= 'a' && ch <= 'z') out[n++] = ch - 'a'; else if (ch >= 'A' && ch <= 'Z') out[n++] = ch - 'A'; }
    fclose(f); return n;
}
static void load_model(const char *path) {
    FILE *fp = fopen(path, "rb");
    if (!fp || fread(QG, sizeof(float), 456976, fp) != 456976) { fprintf(stderr, "modèle ?\n"); exit(1); } fclose(fp);
    double L[676];
    for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double s = 0; for (int c = 0; c < 676; c++) s += exp(QG[(a * 26 + b) * 676 + c]); L[a * 26 + b] = log(s); }
    if (getenv("BDT_PMI")) {
        double U[26] = {0}, V[26] = {0}, tot = 0;
        for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) { double e = exp(L[a * 26 + b]); U[a] += e; V[b] += e; tot += e; }
        for (int a = 0; a < 26; a++) for (int b = 0; b < 26; b++) L[a * 26 + b] = L[a * 26 + b] - log(U[a] / tot) - log(V[b] / tot) - log(tot);
    }
    for (int i = 0; i < 676; i++) BG[i] = (float)L[i];
    {   /* trigrammes : log P(abc) − log P(a) − log P(b) − log P(c) (corrélation totale) */
        static double T3[17576]; double U[26] = {0}, tot = 0;
        for (int i = 0; i < 17576; i++) { double e = 0; for (int d = 0; d < 26; d++) e += exp(QG[i * 26 + d]); T3[i] = e; tot += e; }
        for (int i = 0; i < 17576; i++) U[i / 676] += T3[i] / tot;
        for (int i = 0; i < 17576; i++) TG[i] = (float)(log(T3[i] / tot) - log(U[i / 676]) - log(U[(i / 26) % 26]) - log(U[i % 26]));
        /* quadrigrammes : log P(abcd) − Σ log P(lettre) */
        double Z = 0; for (int i = 0; i < 456976; i++) Z += exp(QG[i]);
        for (int i = 0; i < 456976; i++) Q4[i] = (float)(QG[i] - log(Z) - log(U[i / 17576]) - log(U[(i / 676) % 26]) - log(U[(i / 26) % 26]) - log(U[i % 26]));
    }
}

/* Perturbations de K2 : k échanges quelconques, ou k échanges entre colonnes de même longueur (bornes inchangées). */
static void perturb(int *k, int w, int n, int nswap, int samelen) {
    int r = n % w;
    for (int s = 0; s < nswap; s++) {
        int a, b, tries = 0;
        do { a = rint_(w); b = rint_(w); tries++; } while ((a == b || (samelen && r && ((k[a] < r) != (k[b] < r)))) && tries < 1000);
        int x = k[a]; k[a] = k[b]; k[b] = x;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage : voir l'en-tête\n"); return 1; }
    JOINT = getenv("BDT_JOINT") != NULL; RCMODE = getenv("BDT_RC") != NULL; TIES = getenv("BDT_TIES") != NULL; (void)JOINT_UNUSED; ILS = getenv("BDT_ILS") ? atol(getenv("BDT_ILS")) : 0; FIT = getenv("BDT_FIT") ? atoi(getenv("BDT_FIT")) : 0; KTOP = getenv("BDT_K") ? atoi(getenv("BDT_K")) : 6;
    ALT = getenv("BDT_ALT") != NULL; if (getenv("BDT_ALTIN")) ALT_IN = atol(getenv("BDT_ALTIN")); if (getenv("BDT_ALTOUT")) ALT_OUT = atoi(getenv("BDT_ALTOUT"));
    load_model(argv[2]);
    if (!strcmp(argv[1], "lagcal")) {   /* lagcal qg texte n w1min w1max w2min w2max plants graine : z max des plantés */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n = atoi(argv[4]), a1 = atoi(argv[5]), b1 = atoi(argv[6]), a2 = atoi(argv[7]), b2 = atoi(argv[8]), np = atoi(argv[9]);
        rs = strtoull(argv[10], 0, 10) * 2654435761ULL + 11;
        for (int w1 = a1; w1 <= b1; w1++) for (int w2 = a2; w2 <= b2; w2++) {
            double zs[1000]; int P[MAXN], C[MAXN], k1[MAXW], k2[MAXW];
            for (int p = 0; p < np; p++) { int o = rint_(N - n); memcpy(P, txt + o, sizeof(int) * n); randperm(k1, w1); randperm(k2, w2); encrypt2(P, n, w1, k1, w2, k2, C); zs[p] = lagscan(C, n); }
            int below = 0; double sum = 0; for (int p = 0; p < np; p++) { sum += zs[p]; }
            printf("%d %d moy %.2f", w1, w2, sum / np); for (int p = 0; p < np; p++) printf(" %.1f", zs[p]); printf("\n"); (void)below;
        }
        return 0;
    }
    if (!strcmp(argv[1], "lag")) { int c[MAXN], n = load_letters_file(argv[3], c, MAXN); printf("lag z max %.2f\n", lagscan(c, n)); return 0; }
    if (!strcmp(argv[1], "single")) {   /* single qg chiffré wmin wmax : IDP de colonne simple, z contre 200 mélanges */
        int c[MAXN], n = load_letters_file(argv[3], c, MAXN), a = atoi(argv[4]), b = atoi(argv[5]), sh[MAXN];
        for (int w = a; w <= b; w++) {
            Geo g; geo_init(&g, n, w); double v = idp(c, &g), s = 0, ss = 0;
            for (int r = 0; r < 200; r++) { memcpy(sh, c, sizeof(int) * n); for (int i = n - 1; i > 0; i--) { int j = rint_(i + 1), x = sh[i]; sh[i] = sh[j]; sh[j] = x; } double u = idp(sh, &g); s += u; ss += u * u; }
            double m = s / 200, sd = sqrt(ss / 200 - m * m); printf("w=%d z=%.1f\n", w, (v - m) / sd);
        }
        return 0;
    }
    if (!strcmp(argv[1], "ctrl")) {   /* ctrl qg texte n1 n2 w1 w2 R iters graine [T0 T1] : plante puis R recuits indépendants */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n1 = atoi(argv[4]), n2 = atoi(argv[5]), w1 = atoi(argv[6]), w2 = atoi(argv[7]), R = atoi(argv[8]); long I = atol(argv[9]);
        unsigned long long seed = strtoull(argv[10], 0, 10); rs = seed * 2654435761ULL + 7;
        double T0 = argc > 11 ? atof(argv[11]) : 0.02, T1 = argc > 12 ? atof(argv[12]) : 0.002;
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        int o1 = rint_(N - n1 - n2 - 10000), o2 = o1 + n1 + rint_(5000);
        static int P1[MAXN], P2[MAXN], C1[MAXN], C2[MAXN]; int k1[MAXW], k2[MAXW];
        memcpy(P1, txt + o1, sizeof(int) * n1); memcpy(P2, txt + o2, sizeof(int) * n2);
        randperm(k1, w1); randperm(k2, w2);
        encrypt2(P1, n1, w1, k1, w2, k2, C1); if (n2) encrypt2(P2, n2, w1, k1, w2, k2, C2);
        Msg m[2]; int nm = n2 ? 2 : 1; double wt2 = getenv("BDT_W2") ? atof(getenv("BDT_W2")) : 0.5;
        m[0].c = C1; m[0].n = n1; geo_init(&m[0].g, n1, w1); m[0].wt = 1; if (n2) { m[1].c = C2; m[1].n = n2; geo_init(&m[1].g, n2, w1); m[1].wt = wt2; }
        double tru = fitness(m, nm, w2, k2); int ok = 0;
        #pragma omp parallel for schedule(dynamic) reduction(+:ok)
        for (int r = 0; r < R; r++) {
            rs = (seed * 1000003ULL + r) * 0x9e3779b97f4a7c15ULL + 1; int b[MAXW];
            double v = anneal_ils(m, nm, w2, I, T0, T1, b); int good = 0; for (int j = 0; j < w2; j++) good += b[j] == k2[j];
            if (v >= tru - 1e-9) ok++;
            #pragma omp critical
            printf("  essai %d : %.4f (vraie %.4f) colonnes justes %d/%d, I juste %.0f%%%s\n", r, v, tru, good, w2, 100 * closeness(n1, w2, b, k2), v >= tru - 1e-9 ? "  TROUVÉE" : "");
        }
        printf("w1=%d w2=%d : %d/%d recuits trouvent la vraie K2\n", w1, w2, ok, R);
        return 0;
    }
    if (!strcmp(argv[1], "shiftprobe")) {   /* shiftprobe qg texte n w1 w2 graine : IDP de la vraie K2 décalée d'indice */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n = atoi(argv[4]), w1 = atoi(argv[5]), w2 = atoi(argv[6]); rs = strtoull(argv[7], 0, 10) * 2654435761ULL + 7;
        int o = rint_(N - n), P[MAXN], C[MAXN], k1[MAXW], k2[MAXW], kk[MAXW], t[MAXN]; memcpy(P, txt + o, sizeof(int) * n);
        randperm(k1, w1); randperm(k2, w2); encrypt2(P, n, w1, k1, w2, k2, C); Geo g; geo_init(&g, n, w1);
        for (int sh = 0; sh < w2; sh++) { for (int j = 0; j < w2; j++) kk[j] = (k2[j] + sh) % w2; undo(C, n, w2, kk, t);
            printf("décalage %d : IDP %.4f  I juste %.0f%%\n", sh, idp(t, &g), 100 * closeness(n, w2, kk, k2)); }
        return 0;
    }
    if (!strcmp(argv[1], "sameprobe")) {   /* sameprobe qg texte n w graine : paysage de la clé unique (K1 = K2) */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n = atoi(argv[4]), w = atoi(argv[5]); rs = strtoull(argv[6], 0, 10) * 2654435761ULL + 7;
        int o = rint_(N - n), P[MAXN], C[MAXN], k[MAXW], kk[MAXW], t[MAXN], pl[MAXN]; memcpy(P, txt + o, sizeof(int) * n);
        randperm(k, w); encrypt2(P, n, w, k, w, k, C);
        #define SQ(K) (undo(C, n, w, K, t), undo(t, n, w, K, pl), quad(pl, n))
        double s = 0, ss = 0; for (int r = 0; r < 300; r++) { randperm(kk, w); double v = SQ(kk); s += v; ss += v * v; }
        double m = s / 300, sd = sqrt(ss / 300 - m * m); printf("n=%d w=%d aléatoire %.3f±%.3f vraie %.3f z=%.1f\n", n, w, m, sd, SQ(k), (SQ(k) - m) / sd);
        for (int sl = 0; sl < 2; sl++) { printf("  %s", sl ? "même longueur" : "quelconques  ");
            for (int ns = 1; ns <= 10; ns++) { double z = 0; for (int r = 0; r < 60; r++) { memcpy(kk, k, sizeof(int) * w); perturb(kk, w, n, ns, sl); z += (SQ(kk) - m) / sd; } printf("  %d:%.1f", ns, z / 60); }
            printf("\n"); }
        return 0;
    }
    if (!strcmp(argv[1], "scan")) {   /* scan qg c1 c2|- w1a w1b w2a w2b R iters graine [T0 T1] : recherche réelle */
        static int C1[MAXN], C2[MAXN]; int n1 = load_letters_file(argv[3], C1, MAXN), n2 = strcmp(argv[4], "-") ? load_letters_file(argv[4], C2, MAXN) : 0;
        int a1 = atoi(argv[5]), b1 = atoi(argv[6]), a2 = atoi(argv[7]), b2 = atoi(argv[8]), R = atoi(argv[9]); long I = atol(argv[10]);
        unsigned long long seed = strtoull(argv[11], 0, 10); double T0 = argc > 12 ? atof(argv[12]) : 0.02, T1 = argc > 13 ? atof(argv[13]) : 0.002;
        double zmin = getenv("BDT_ZK1") ? atof(getenv("BDT_ZK1")) : 12; double wt2 = getenv("BDT_W2") ? atof(getenv("BDT_W2")) : 0.5;
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        int shard = 0, nshard = 1, idx = -1; if (getenv("BDT_SHARD")) sscanf(getenv("BDT_SHARD"), "%d/%d", &shard, &nshard);
        for (int w2 = a2; w2 <= b2; w2++) for (int w1 = a1; w1 <= b1; w1++) {
            if (++idx % nshard != shard) continue;
            Msg m[2]; int nm = n2 ? 2 : 1;
            m[0].c = C1; m[0].n = n1; geo_init(&m[0].g, n1, w1); m[0].wt = 1; if (n2) { m[1].c = C2; m[1].n = n2; geo_init(&m[1].g, n2, w1); m[1].wt = wt2; }
            /* distribution des clés aléatoires (T1 seul et T2 seul) pour normaliser */
            rs = (seed * 7919ULL + w1 * 131 + w2) * 0x9e3779b97f4a7c15ULL + 3; int kk[MAXW], t[MAXN];
            double s1 = 0, q1 = 0, s2 = 0, q2 = 0; int NR = 300;
            for (int r = 0; r < NR; r++) { randperm(kk, w2); undoK2(C1, n1, w2, kk, t); double v = idp(t, &m[0].g); s1 += v; q1 += v * v;
                if (n2) { undoK2(C2, n2, w2, kk, t); double u = idp(t, &m[1].g); s2 += u; q2 += u * u; } }
            double mu1 = s1 / NR, sd1 = sqrt(q1 / NR - mu1 * mu1), mu2 = n2 ? s2 / NR : 0, sd2 = n2 ? sqrt(q2 / NR - mu2 * mu2) + 1e-12 : 1;
            double best = -1e18; int bk[MAXW];
            #pragma omp parallel for schedule(dynamic)
            for (int r = 0; r < R; r++) {
                rs = (seed * 1000003ULL + (unsigned long long)r * 7777 + w1 * 131 + w2) * 0x9e3779b97f4a7c15ULL + 1; int b[MAXW];
                double v = anneal_ils(m, nm, w2, I, T0, T1, b);
                #pragma omp critical
                if (v > best) { best = v; memcpy(bk, b, sizeof(int) * w2); }
            }
            undoK2(C1, n1, w2, bk, t); double z1 = (idp(t, &m[0].g) - mu1) / sd1, z2 = 0; static int I1[MAXN], I2[MAXN]; memcpy(I1, t, sizeof(int) * n1);
            if (n2) { undoK2(C2, n2, w2, bk, I2); z2 = (idp(I2, &m[1].g) - mu2) / sd2; }
            printf("w1=%d w2=%d  z(T1)=%.1f z(T2)=%.1f  K2", w1, w2, z1, z2); for (int j = 0; j < w2; j++) printf(" %d", bk[j]); printf("\n");
            if (z1 >= zmin) {
                const int *Is[2] = {I1, I2}; int ns[2] = {n1, n2}, k1[MAXW], out[MAXN];
                double q = solve_k1(Is, ns, nm, w1, 8, 300000, k1); k1score(Is, ns, 1, w1, k1, out);
                printf("   K1 quadrigrammes %.3f  K1", q); for (int j = 0; j < w1; j++) printf(" %d", k1[j]); printf("\n   T1 ");
                for (int i = 0; i < n1; i++) putchar('a' + out[i]); printf("\n");
                if (n2) { int p2[MAXN]; undo(I2, n2, w1, k1, p2); printf("   T2 "); for (int i = 0; i < n2; i++) putchar('a' + p2[i]); printf("\n"); }
            }
            fflush(stdout);
        }
        return 0;
    }
    if (!strcmp(argv[1], "probefit")) {   /* probefit qg texte n1 n2 w1 w2 graine : z de la fitness (BDT_JOINT, BDT_W2) vs échanges même longueur */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n1 = atoi(argv[4]), n2 = atoi(argv[5]), w1 = atoi(argv[6]), w2 = atoi(argv[7]); rs = strtoull(argv[8], 0, 10) * 2654435761ULL + 7;
        int o1 = rint_(N - n1 - n2 - 10000), o2 = o1 + n1 + rint_(5000);
        static int P1[MAXN], P2[MAXN], C1[MAXN], C2[MAXN]; int k1[MAXW], k2[MAXW], kk[MAXW];
        memcpy(P1, txt + o1, sizeof(int) * n1); memcpy(P2, txt + o2, sizeof(int) * n2); randperm(k1, w1); randperm(k2, w2);
        encrypt2(P1, n1, w1, k1, w2, k2, C1); if (n2) encrypt2(P2, n2, w1, k1, w2, k2, C2);
        Msg m[2]; int nm = n2 ? 2 : 1; double wt2 = getenv("BDT_W2") ? atof(getenv("BDT_W2")) : 0.5;
        m[0].c = C1; m[0].n = n1; geo_init(&m[0].g, n1, w1); m[0].wt = 1; if (n2) { m[1].c = C2; m[1].n = n2; geo_init(&m[1].g, n2, w1); m[1].wt = wt2; }
        double s = 0, ss = 0; int R = 400; for (int r = 0; r < R; r++) { randperm(kk, w2); double v = fitness(m, nm, w2, kk); s += v; ss += v * v; }
        double mu = s / R, sd = sqrt(ss / R - mu * mu), tr = fitness(m, nm, w2, k2);
        printf("w1=%d w2=%d vraie z=%.1f |", w1, w2, (tr - mu) / sd);
        for (int ns = 1; ns <= 8; ns++) { double z = 0; for (int r = 0; r < 80; r++) { memcpy(kk, k2, sizeof(int) * w2); perturb(kk, w2, n1, ns, 1); z += (fitness(m, nm, w2, kk) - mu) / sd; } printf(" %d:%.1f", ns, z / 80); }
        printf("\n");
        /* oracle : K1 vraie connue, somme des bigrammes du clair */
        { int t[MAXN], pl[MAXN]; double so = 0, sso = 0;
          #define ORA(K) (undo(C1, n1, w2, K, t), undo(t, n1, w1, k1, pl), ({ double z_ = 0; for (int i = 0; i + 1 < n1; i++) z_ += BG[pl[i] * 26 + pl[i + 1]]; z_; }))
          for (int r = 0; r < R; r++) { randperm(kk, w2); double v = ORA(kk); so += v; sso += v * v; }
          double mo = so / R, sdo = sqrt(sso / R - mo * mo); printf("   oracle K1 : vraie z=%.1f |", (ORA(k2) - mo) / sdo);
          for (int ns = 1; ns <= 8; ns++) { double z = 0; double cl = 0; for (int r = 0; r < 80; r++) { memcpy(kk, k2, sizeof(int) * w2); perturb(kk, w2, n1, ns, 1); z += (ORA(kk) - mo) / sdo; cl += closeness(n1, w2, kk, k2); } printf(" %d:%.1f(%.0f%%)", ns, z / 80, 100 * cl / 80); }
          printf("\n"); }
        return 0;
    }
    if (!strcmp(argv[1], "known")) {   /* known qg chiffré w1 phrase R iters graine [T0 T1] : recuit aveugle sur un chiffré dont K2 est connue */
        static int C[MAXN]; int n = load_letters_file(argv[3], C, MAXN), w1 = atoi(argv[4]); const char *ph = argv[5]; int w2 = (int)strlen(ph), k2[MAXW];
        for (int r = 0, j = 0; r < 26; r++) for (int i = 0; i < w2; i++) if (ph[i] - 'a' == r) k2[j++] = i;
        int R = atoi(argv[6]); long I = atol(argv[7]); unsigned long long seed = strtoull(argv[8], 0, 10);
        double T0 = argc > 9 ? atof(argv[9]) : 0.02, T1 = argc > 10 ? atof(argv[10]) : 0.002;
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        Msg m[1]; m[0].c = C; m[0].n = n; geo_init(&m[0].g, n, w1); m[0].wt = 1; double tru = fitness(m, 1, w2, k2); int ok = 0;
        #pragma omp parallel for schedule(dynamic) reduction(+:ok)
        for (int r = 0; r < R; r++) {
            rs = (seed * 1000003ULL + r) * 0x9e3779b97f4a7c15ULL + 1; int b[MAXW];
            double v = anneal_ils(m, 1, w2, I, T0, T1, b); if (v >= tru - 1e-9) ok++;
            #pragma omp critical
            printf("  essai %d : %.4f (vraie %.4f) I juste %.0f%%\n", r, v, tru, 100 * closeness(n, w2, b, k2));
        }
        printf("%d/%d\n", ok, R); return 0;
    }
    if (!strcmp(argv[1], "knownprobe")) {   /* knownprobe qg chiffré w1 phrase : pente de l'IDP autour de la vraie K2 */
        static int C[MAXN]; int n = load_letters_file(argv[3], C, MAXN), w1 = atoi(argv[4]); const char *ph = argv[5]; int w2 = (int)strlen(ph), k2[MAXW], kk[MAXW];
        for (int r = 0, j = 0; r < 26; r++) for (int i = 0; i < w2; i++) if (ph[i] - 'a' == r) k2[j++] = i;
        Msg m[1]; m[0].c = C; m[0].n = n; geo_init(&m[0].g, n, w1); m[0].wt = 1;
        double s = 0, ss = 0; int R = 400; for (int r = 0; r < R; r++) { randperm(kk, w2); double v = fitness(m, 1, w2, kk); s += v; ss += v * v; }
        double mu = s / R, sd = sqrt(ss / R - mu * mu), tr = fitness(m, 1, w2, k2);
        printf("w1=%d w2=%d vraie z=%.1f |", w1, w2, (tr - mu) / sd);
        for (int ns = 1; ns <= 8; ns++) { double z = 0; for (int r = 0; r < 80; r++) { memcpy(kk, k2, sizeof(int) * w2); perturb(kk, w2, n, ns, 1); z += (fitness(m, 1, w2, kk) - mu) / sd; } printf(" %d:%.1f", ns, z / 80); }
        printf("\n"); return 0;
    }
    if (!strcmp(argv[1], "samectrl")) {   /* samectrl qg texte n1 n2 w R iters graine [T0 T1] : clé unique plantée */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n1 = atoi(argv[4]), n2 = atoi(argv[5]), w = atoi(argv[6]), R = atoi(argv[7]); long I = atol(argv[8]); unsigned long long seed = strtoull(argv[9], 0, 10);
        double T0 = argc > 10 ? atof(argv[10]) : 0.3, T1 = argc > 11 ? atof(argv[11]) : 0.005; rs = seed * 2654435761ULL + 7;
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        int o1 = rint_(N - n1 - n2 - 10000), o2 = o1 + n1 + rint_(5000); static int P1[MAXN], P2[MAXN], C1[MAXN], C2[MAXN]; int k[MAXW];
        memcpy(P1, txt + o1, sizeof(int) * n1); memcpy(P2, txt + o2, sizeof(int) * n2); randperm(k, w);
        encrypt2(P1, n1, w, k, w, k, C1); if (n2) encrypt2(P2, n2, w, k, w, k, C2);
        const int *Cs[2] = {C1, C2}; int ns[2] = {n1, n2}, nm = n2 ? 2 : 1; double tru = same_score(Cs, ns, nm, w, k); int ok = 0;
        #pragma omp parallel for schedule(dynamic) reduction(+:ok)
        for (int r = 0; r < R; r++) { rs = (seed * 1000003ULL + r) * 0x9e3779b97f4a7c15ULL + 1; int b[MAXW]; double v = same_anneal(Cs, ns, nm, w, I, T0, T1, b); if (v >= tru - 1e-9) ok++; }
        printf("clé unique w=%d : %d/%d (vraie %.3f)\n", w, ok, R, tru); return 0;
    }
    if (!strcmp(argv[1], "dict")) {   /* dict qg c1 c2|- cles.txt w1a w1b w2a w2b top : clés-phrases, IDP T1 (z) + clé unique (z) */
        static int C1[MAXN], C2[MAXN]; int n1 = load_letters_file(argv[3], C1, MAXN), n2 = strcmp(argv[4], "-") ? load_letters_file(argv[4], C2, MAXN) : 0;
        int a1 = atoi(argv[6]), b1 = atoi(argv[7]), a2 = atoi(argv[8]), b2 = atoi(argv[9]), top = atoi(argv[10]);
        static Geo G1[MAXW], G2[MAXW]; static double MU[MAXW][MAXW], SD[MAXW][MAXW], SMU[MAXW], SSD[MAXW];
        const int *Cs[2] = {C1, C2}; int ns[2] = {n1, n2}, nm = n2 ? 2 : 1;
        for (int w1 = a1; w1 <= b1; w1++) { geo_init(&G1[w1], n1, w1); if (n2) geo_init(&G2[w1], n2, w1); }
        rs = 12345;
        #pragma omp parallel for schedule(dynamic) collapse(2)
        for (int w2 = a2; w2 <= b2; w2++) for (int w1 = a1; w1 <= b1; w1++) {
            rs = (w1 * 1000 + w2) * 0x9e3779b97f4a7c15ULL + 5; int kk[MAXW], t[MAXN]; double s = 0, ss = 0;
            for (int r = 0; r < 200; r++) { randperm(kk, w2); undo(C1, n1, w2, kk, t); double v = idp(t, &G1[w1]); s += v; ss += v * v; }
            MU[w1][w2] = s / 200; SD[w1][w2] = sqrt(ss / 200 - MU[w1][w2] * MU[w1][w2]);
        }
        for (int w = a2; w <= b2; w++) { int kk[MAXW]; double s = 0, ss = 0; for (int r = 0; r < 300; r++) { randperm(kk, w); double v = same_score(Cs, ns, nm, w, kk); s += v; ss += v * v; } SMU[w] = s / 300; SSD[w] = sqrt(ss / 300 - SMU[w] * SMU[w]); }
        FILE *f = fopen(argv[5], "r"); if (!f) { fprintf(stderr, "clés ?\n"); return 1; }
        typedef struct { double z; int w1, w2, kind; char key[64]; } Hit; static Hit H[4096]; int nh = 0; long nk = 0, ntr = 0;
        char line[256]; static char batch[65536][40]; int nb;
        double hist[8] = {0};
        while (1) {
            nb = 0; while (nb < 65536 && fgets(line, sizeof line, f)) { int L = 0; for (char *c = line; *c && L < 39; c++) if (*c >= 'a' && *c <= 'z') batch[nb][L++] = *c; batch[nb][L] = 0; if (L >= a2 && L <= b2) nb++; }
            if (!nb) break;
            #pragma omp parallel for schedule(dynamic, 64)
            for (int i = 0; i < nb; i++) {
                int w2 = (int)strlen(batch[i]), k2[MAXW], t[MAXN];
                for (int r = 0, j = 0; r < 26; r++) for (int cc = 0; cc < w2; cc++) { int c = TIES ? w2 - 1 - cc : cc; if (batch[i][c] - 'a' == r) k2[j++] = c; }
                undo(C1, n1, w2, k2, t);
                Hit loc[40]; int nl = 0;
                for (int w1 = a1; w1 <= b1; w1++) { double z = (idp(t, &G1[w1]) - MU[w1][w2]) / SD[w1][w2];
                    if (z > 4.5) { loc[nl].z = z; loc[nl].w1 = w1; loc[nl].w2 = w2; loc[nl].kind = 0; strcpy(loc[nl].key, batch[i]); nl++; } }
                double zs = (same_score(Cs, ns, nm, w2, k2) - SMU[w2]) / SSD[w2];
                if (zs > 4.5) { loc[nl].z = zs; loc[nl].w1 = w2; loc[nl].w2 = w2; loc[nl].kind = 1; strcpy(loc[nl].key, batch[i]); nl++; }
                #pragma omp critical
                { for (int j = 0; j < nl; j++) { if (nh < 4096) H[nh++] = loc[j]; int b = (int)loc[j].z - 4; if (b > 7) b = 7; if (b >= 0) hist[b]++; } }
            }
            nk += nb; ntr += (long)nb * (b1 - a1 + 2);
        }
        fclose(f);
        for (int i = 1; i < nh; i++) { Hit x = H[i]; int j = i - 1; while (j >= 0 && H[j].z < x.z) { H[j + 1] = H[j]; j--; } H[j + 1] = x; }
        printf("clés=%ld essais=%ld  z>4.5 : ", nk, ntr); for (int b = 0; b < 8; b++) printf("[%d,%d):%.0f ", b + 4, b + 5, hist[b]); printf("\n");
        for (int i = 0; i < nh && i < top; i++) {
            double z2 = 0;
            if (n2 && H[i].kind == 0) { int w2 = H[i].w2, k2[MAXW], t[MAXN], kk[MAXW]; for (int r = 0, j = 0; r < 26; r++) for (int cc = 0; cc < w2; cc++) { int c = TIES ? w2 - 1 - cc : cc; if (H[i].key[c] - 'a' == r) k2[j++] = c; }
                double s = 0, ss = 0; for (int r = 0; r < 200; r++) { randperm(kk, w2); undo(C2, n2, w2, kk, t); double v = idp(t, &G2[H[i].w1]); s += v; ss += v * v; }
                undo(C2, n2, w2, k2, t); z2 = (idp(t, &G2[H[i].w1]) - s / 200) / sqrt(ss / 200 - (s / 200) * (s / 200)); }
            printf("%.2f %s w1=%d w2=%d z(T2)=%.1f %s\n", H[i].z, H[i].kind ? "CLE_UNIQUE" : "IDP", H[i].w1, H[i].w2, z2, H[i].key);
        }
        return 0;
    }
    if (!strcmp(argv[1], "samescan")) {   /* samescan qg c1 c2|- wa wb R iters graine : clé unique (K1 = K2), recherche réelle */
        static int C1[MAXN], C2[MAXN]; int n1 = load_letters_file(argv[3], C1, MAXN), n2 = strcmp(argv[4], "-") ? load_letters_file(argv[4], C2, MAXN) : 0;
        int a = atoi(argv[5]), b = atoi(argv[6]), R = atoi(argv[7]); long I = atol(argv[8]); unsigned long long seed = strtoull(argv[9], 0, 10);
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        int shard = 0, nshard = 1, idx = -1; if (getenv("BDT_SHARD")) sscanf(getenv("BDT_SHARD"), "%d/%d", &shard, &nshard);
        const int *Cs[2] = {C1, C2}; int ns[2] = {n1, n2}, nm = n2 ? 2 : 1;
        for (int w = a; w <= b; w++) {
            if (++idx % nshard != shard) continue;
            rs = seed * 7919ULL + w; int kk[MAXW]; double s = 0, ss = 0;
            for (int r = 0; r < 500; r++) { randperm(kk, w); double v = same_score(Cs, ns, nm, w, kk); s += v; ss += v * v; }
            double mu = s / 500, sd = sqrt(ss / 500 - mu * mu), best = -1e18; int bk[MAXW];
            #pragma omp parallel for schedule(dynamic)
            for (int r = 0; r < R; r++) { rs = (seed * 1000003ULL + (unsigned long long)r * 7777 + w) * 0x9e3779b97f4a7c15ULL + 1; int bb[MAXW];
                double v = same_anneal(Cs, ns, nm, w, I, 0.3, 0.005, bb);
                #pragma omp critical
                if (v > best) { best = v; memcpy(bk, bb, sizeof(int) * w); } }
            printf("w=%d  meilleur %.3f  z=%.1f  K", w, best, (best - mu) / sd); for (int j = 0; j < w; j++) printf(" %d", bk[j]);
            int t[MAXN], p[MAXN]; undo(C1, n1, w, bk, t); undo(t, n1, w, bk, p); printf("\n   T1 "); for (int i = 0; i < 120; i++) putchar('a' + p[i]);
            if (n2) { undo(C2, n2, w, bk, t); undo(t, n2, w, bk, p); printf("\n   T2 "); for (int i = 0; i < 80; i++) putchar('a' + p[i]); }
            printf("\n"); fflush(stdout);
        }
        return 0;
    }
    if (!strcmp(argv[1], "bench")) {   /* bench qg c1 w1 w2 : µs par évaluation IDP */
        static int C1[MAXN]; int n1 = load_letters_file(argv[3], C1, MAXN), w1 = atoi(argv[4]), w2 = atoi(argv[5]), kk[MAXW], t[MAXN];
        Geo g; geo_init(&g, n1, w1); double acc = 0; struct timespec a, b; clock_gettime(CLOCK_MONOTONIC, &a);
        for (int r = 0; r < 3000; r++) { randperm(kk, w2); undo(C1, n1, w2, kk, t); acc += idp(t, &g); }
        clock_gettime(CLOCK_MONOTONIC, &b); printf("w1=%d w2=%d : %.1f µs/éval (%g)\n", w1, w2, ((b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec)) / 3000 / 1e3, acc); return 0;
    }
    if (!strcmp(argv[1], "ctrlgrid")) {   /* ctrlgrid qg texte n1 n2 w1a w1b w2a w2b plantés R iters graine : succès par paire */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n1 = atoi(argv[4]), n2 = atoi(argv[5]), a1 = atoi(argv[6]), b1 = atoi(argv[7]), a2 = atoi(argv[8]), b2 = atoi(argv[9]), NP = atoi(argv[10]), R = atoi(argv[11]);
        long I = atol(argv[12]); unsigned long long seed = strtoull(argv[13], 0, 10); double wt2 = getenv("BDT_W2") ? atof(getenv("BDT_W2")) : 0.5;
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        int shard = 0, nshard = 1, idx = -1; if (getenv("BDT_SHARD")) sscanf(getenv("BDT_SHARD"), "%d/%d", &shard, &nshard);
        for (int w2 = a2; w2 <= b2; w2++) for (int w1 = a1; w1 <= b1; w1++) {
            if (++idx % nshard != shard) continue;
            int ok = 0, tot = 0;
            for (int pl = 0; pl < NP; pl++) {
                rs = (seed * 31 + pl * 977 + w1 * 131 + w2) * 2654435761ULL + 7;
                int o1 = rint_(N - n1 - n2 - 10000), o2 = o1 + n1 + rint_(5000);
                static int P1[MAXN], P2[MAXN], C1[MAXN], C2[MAXN]; int k1[MAXW], k2[MAXW];
                memcpy(P1, txt + o1, sizeof(int) * n1); memcpy(P2, txt + o2, sizeof(int) * n2); randperm(k1, w1); randperm(k2, w2);
                encrypt2(P1, n1, w1, k1, w2, k2, C1); if (n2) encrypt2(P2, n2, w1, k1, w2, k2, C2);
                Msg m[2]; int nm = n2 ? 2 : 1;
                m[0].c = C1; m[0].n = n1; geo_init(&m[0].g, n1, w1); m[0].wt = 1; if (n2) { m[1].c = C2; m[1].n = n2; geo_init(&m[1].g, n2, w1); m[1].wt = wt2; }
                double tru = fitness(m, nm, w2, k2);
                #pragma omp parallel for schedule(dynamic) reduction(+:ok, tot)
                for (int r = 0; r < R; r++) { rs = (seed * 1000003ULL + pl * 7919 + r) * 0x9e3779b97f4a7c15ULL + 1; int b[MAXW];
                    double v = anneal_ils(m, nm, w2, I, 0.02, 0.002, b); ok += v >= tru - 1e-9; tot++; }
            }
            printf("calib w1=%d w2=%d : %d/%d\n", w1, w2, ok, tot); fflush(stdout);
        }
        return 0;
    }
    if (!strcmp(argv[1], "consensus")) {   /* consensus qg texte n w1 w2 R iters graine : fréquence des vraies paires de K1 dans les chaînes */
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n = atoi(argv[4]), w1 = atoi(argv[5]), w2 = atoi(argv[6]), R = atoi(argv[7]); long I = atol(argv[8]); unsigned long long seed = strtoull(argv[9], 0, 10);
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        rs = seed * 2654435761ULL + 7; int o = rint_(N - n); static int P[MAXN], C[MAXN]; int k1[MAXW], k2[MAXW], inv1[MAXW];
        memcpy(P, txt + o, sizeof(int) * n); randperm(k1, w1); randperm(k2, w2); encrypt2(P, n, w1, k1, w2, k2, C);
        for (int r = 0; r < w1; r++) inv1[k1[r]] = r;
        int truer[MAXW]; for (int a = 0; a < w1; a++) { int j = k1[a]; truer[a] = j + 1 < w1 ? inv1[j + 1] : -1; }
        Msg m[1]; m[0].c = C; m[0].n = n; geo_init(&m[0].g, n, w1); m[0].wt = 1;
        static int cnt[MAXW][MAXW]; int hits = 0, links = 0;
        #pragma omp parallel for schedule(dynamic) reduction(+:hits, links)
        for (int r = 0; r < R; r++) {
            rs = (seed * 1000003ULL + r) * 0x9e3779b97f4a7c15ULL + 1; int b[MAXW], t[MAXN], right[MAXW]; float mat[MAXW][MAXW];
            anneal(m, 1, w2, I, 0.02, 0.002, b); undo(C, n, w2, b, t); pair_matrix_raw(t, &m[0].g, mat, 0); chain_links(mat, w1, right);
            for (int a = 0; a < w1; a++) if (right[a] >= 0) { links++; if (right[a] == truer[a]) hits++;
                #pragma omp atomic
                cnt[a][right[a]]++; }
        }
        printf("liens %d, vrais %d (%.1f%% ; hasard %.1f%%)\n", links, hits, 100.0 * hits / links, 100.0 / (w1 - 1));
        int top_true = 0; for (int a = 0; a < w1; a++) { if (truer[a] < 0) continue; int bb = -1; for (int b = 0; b < w1; b++) if (bb < 0 || cnt[a][b] > cnt[a][bb]) bb = b; top_true += bb == truer[a]; }
        printf("vote majoritaire : %d/%d vrais voisins\n", top_true, w1 - 1); return 0;
    }
    if (!strcmp(argv[1], "exh")) {   /* exh qg chiffré w1a w1b w2a w2b top : toutes les K2 (w2 ≤ 10), IDP, puis K1 aux quadrigrammes sur les meilleures */
        static int C[MAXN]; int n = load_letters_file(argv[3], C, MAXN), a1 = atoi(argv[4]), b1 = atoi(argv[5]), a2 = atoi(argv[6]), b2 = atoi(argv[7]), top = atoi(argv[8]);
        for (int w2 = a2; w2 <= b2; w2++) for (int w1 = a1; w1 <= b1; w1++) {
            Geo g; geo_init(&g, n, w1); int kk[MAXW], t[MAXN]; double s = 0, ss = 0; rs = 99 + w1 * 31 + w2;
            for (int r = 0; r < 300; r++) { randperm(kk, w2); undo(C, n, w2, kk, t); double v = idp(t, &g); s += v; ss += v * v; }
            double mu = s / 300, sd = sqrt(ss / 300 - mu * mu);
            /* énumération par rang lexicographique, répartie entre fils */
            long tot = 1; for (int i = 2; i <= w2; i++) tot *= i;
            typedef struct { double v; int k[MAXW]; } Cand; Cand best[64]; int nb = 0;
            #pragma omp parallel
            {
                Cand loc[64]; int nl = 0; int tt[MAXN];
                #pragma omp for schedule(dynamic, 4096)
                for (long idx = 0; idx < tot; idx++) {
                    int k[MAXW], used[MAXW] = {0}; long x = idx, f = tot;
                    for (int i = 0; i < w2; i++) { f /= (w2 - i); int d = (int)(x / f); x %= f; int c = -1; while (d >= 0) { c++; if (!used[c]) d--; } used[c] = 1; k[i] = c; }
                    undo(C, n, w2, k, tt); double v = idp(tt, &g);
                    if (nl < top || v > loc[nl - 1].v) { int j = nl < top ? nl++ : nl - 1; while (j > 0 && loc[j - 1].v < v) { loc[j] = loc[j - 1]; j--; } loc[j].v = v; memcpy(loc[j].k, k, sizeof(int) * w2); }
                }
                #pragma omp critical
                for (int i = 0; i < nl; i++) { double v = loc[i].v; if (nb < top || v > best[nb - 1].v) { int j = nb < top ? nb++ : nb - 1; while (j > 0 && best[j - 1].v < v) { best[j] = best[j - 1]; j--; } best[j] = loc[i]; } }
            }
            double bq = -1e9; int bi = -1, bk1[MAXW], out[MAXN];
            for (int i = 0; i < nb; i++) { undo(C, n, w2, best[i].k, t); const int *Is[1] = {t}; int ns[1] = {n}, k1[MAXW];
                double q = solve_k1(Is, ns, 1, w1, 4, 60000, k1); if (q > bq) { bq = q; bi = i; memcpy(bk1, k1, sizeof(int) * w1); k1score(Is, ns, 1, w1, k1, out); } }
            printf("w1=%d w2=%d  IDP z max %.1f  meilleur clair (quadrigrammes) %.3f : ", w1, w2, (best[0].v - mu) / sd, bq);
            for (int i = 0; i < n && i < 90; i++) putchar('a' + out[i]); printf("\n"); fflush(stdout);
        }
        return 0;
    }
    if (!strcmp(argv[1], "lagscan2")) {   /* lagscan2 qg c1 c2|- conv w1a w1b w2a w2b R iters graine : conventions faciles */
        static int C1[MAXN], C2[MAXN]; int n1 = load_letters_file(argv[3], C1, MAXN), n2 = strcmp(argv[4], "-") ? load_letters_file(argv[4], C2, MAXN) : 0;
        if (getenv("BDT_LT")) sscanf(getenv("BDT_LT"), "%lf,%lf", &LT0, &LT1);
        CONV = atoi(argv[5]); int a1 = atoi(argv[6]), b1 = atoi(argv[7]), a2 = atoi(argv[8]), b2 = atoi(argv[9]), R = atoi(argv[10]); long I = atol(argv[11]);
        unsigned long long seed = strtoull(argv[12], 0, 10); double zmin = getenv("BDT_ZK1") ? atof(getenv("BDT_ZK1")) : 8;
        if (getenv("BDT_MV")) sscanf(getenv("BDT_MV"), "%d,%d,%d,%d,%d,%d,%d", MV, MV + 1, MV + 2, MV + 3, MV + 4, MV + 5, MV + 6);
        int shard = 0, nshard = 1, idx = -1; if (getenv("BDT_SHARD")) sscanf(getenv("BDT_SHARD"), "%d/%d", &shard, &nshard);
        const int *Cs[2] = {C1, C2}; int ns[2] = {n1, n2}, nm = n2 ? 2 : 1;
        for (int w2 = a2; w2 <= b2; w2++) for (int w1 = a1; w1 <= b1; w1++) {
            if (++idx % nshard != shard) continue;
            rs = seed * 7919ULL + w1 * 131 + w2; int kk[MAXW]; double s = 0, ss = 0;
            for (int r = 0; r < 300; r++) { randperm(kk, w2); double v = lagfit(Cs, ns, nm, w1, w2, kk); s += v; ss += v * v; }
            double mu = s / 300, sd = sqrt(ss / 300 - mu * mu), best = -1e18; int bk[MAXW];
            #pragma omp parallel for schedule(dynamic)
            for (int r = 0; r < R; r++) { rs = (seed * 1000003ULL + (unsigned long long)r * 7777 + w1 * 131 + w2) * 0x9e3779b97f4a7c15ULL + 1; int bb[MAXW];
                double v = lag_anneal(Cs, ns, nm, w1, w2, I, LT0, LT1, bb);
                #pragma omp critical
                if (v > best) { best = v; memcpy(bk, bb, sizeof(int) * w2); } }
            double z = (best - mu) / sd;
            if (CONV == 2) { CONV = 1; lag_polish(Cs, ns, nm, w1, w2, bk); CONV = 2; }   /* finition à la note exacte */
            printf("conv=%d w1=%d w2=%d  z=%.1f  K2", CONV, w1, w2, z); for (int j = 0; j < w2; j++) printf(" %d", bk[j]); printf("\n");
            if (z >= zmin) {
                if (CONV == 2) cr_rotations(C1, C2, n1, n2, w1, w2, bk);
                static int J1[MAXN], J2[MAXN]; if (CONV == 0) { fwdT(C1, n1, w2, bk, J1); if (n2) fwdT(C2, n2, w2, bk, J2); } else {  /* conv 1 et 2 */ undo(C1, n1, w2, bk, J1); if (n2) undo(C2, n2, w2, bk, J2); }
                int bk1[MAXW], P1[MAXN], P2[MAXN]; double bq = k1stage_fwd(J1, J2, n1, n2, w1, 8, 200000, bk1);
                fwdT(J1, n1, w1, bk1, P1); printf("   K1 quadrigrammes %.3f\n   T1 ", bq); for (int i = 0; i < n1; i++) putchar('a' + P1[i]);
                if (n2) { fwdT(J2, n2, w1, bk1, P2); printf("\n   T2 "); for (int i = 0; i < n2; i++) putchar('a' + P2[i]); } printf("\n");
            }
            fflush(stdout);
        }
        return 0;
    }
    if (!strcmp(argv[1], "probe")) {
        static int txt[2000000]; int N = load_letters_file(argv[3], txt, 2000000);
        int n1 = atoi(argv[4]), n2 = atoi(argv[5]), w1 = atoi(argv[6]), w2 = atoi(argv[7]);
        rs = strtoull(argv[8], 0, 10) * 2654435761ULL + 7;
        int o1 = rint_(N - n1 - n2 - 10000), o2 = o1 + n1 + rint_(5000);
        int P1[MAXN], P2[MAXN], C1[MAXN], C2[MAXN], k1[MAXW], k2[MAXW], t[MAXN];
        memcpy(P1, txt + o1, sizeof(int) * n1); memcpy(P2, txt + o2, sizeof(int) * n2);
        randperm(k1, w1); randperm(k2, w2);
        encrypt2(P1, n1, w1, k1, w2, k2, C1); if (n2) encrypt2(P2, n2, w1, k1, w2, k2, C2);
        Geo g1, g2; geo_init(&g1, n1, w1); if (n2) geo_init(&g2, n2, w1);
        #define F1(K) (undo(C1, n1, w2, K, t), idp(t, &g1))
        #define F2(K) (n2 ? (undo(C2, n2, w2, K, t), idp(t, &g2)) : 0)
        double s1 = 0, ss1 = 0, s2 = 0, ss2 = 0, mx1 = -1e9; int R = 400, kk[MAXW];
        for (int r = 0; r < R; r++) { randperm(kk, w2); double a = F1(kk), b = F2(kk); s1 += a; ss1 += a * a; s2 += b; ss2 += b * b; if (a > mx1) mx1 = a; }
        double m1 = s1 / R, sd1 = sqrt(ss1 / R - m1 * m1), m2 = s2 / R, sd2 = sqrt(ss2 / R - m2 * m2) + 1e-9;
        double tr1 = F1(k2), tr2 = F2(k2);
        printf("n1=%d n2=%d w1=%d w2=%d  aléatoire T1 %.4f±%.4f (max %.4f)  vraie T1 %.4f z=%.1f | T2 vraie z=%.1f\n",
               n1, n2, w1, w2, m1, sd1, mx1, tr1, (tr1 - m1) / sd1, (tr2 - m2) / sd2);
        for (int sl = 0; sl < 2; sl++) {
            printf("  %s :", sl ? "échanges même longueur" : "échanges quelconques ");
            for (int ns = 1; ns <= 8; ns++) {
                double z = 0, zj = 0; int T = 60;
                for (int r = 0; r < T; r++) { memcpy(kk, k2, sizeof(int) * w2); perturb(kk, w2, n1, ns, sl); z += (F1(kk) - m1) / sd1; zj += (F2(kk) - m2) / sd2; }
                printf("  %d:%.1f/%.1f", ns, z / T, zj / T);
            }
            printf("\n");
        }
        return 0;
    }
    fprintf(stderr, "mode inconnu\n"); return 1;
}
