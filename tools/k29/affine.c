/* K29 — suggestion 3 : blocs de 169 (13×13) et 144 (12×12) remplis selon un carré magique ou une marche régulière.
   Famille exhaustive : toutes les marches AFFINES du tore n×n. La k-ième lettre du clair (k = q·n + r) va dans la case
   (r0 + a·r + b·q, c0 + c·r + d·q) mod n, avec [[a,b],[c,d]] inversible mod n ; le chiffré est lu en lignes (sens 0),
   ou l'inverse : clair écrit en lignes, chiffré lu dans l'ordre de la marche (sens 1). Cette famille contient la méthode
   siamoise de La Loubère (pas (−1,+1), décalage (+1,0) : a=−1, b=2, c=1, d=−1) et ses 8 symétries, la méthode de
   Bachet / de la Hire à pas uniformes, les lignes, colonnes, diagonales, sauts de cavalier, etc.
   Blocs incomplets (166, 162 dans un 13×13) : cases restées vides = celles des indices k ≥ longueur, sautées à la
   lecture. Bloc de 144 : marches affines mod 12 + carré magique doublement pair classique (8 symétries).
   Note : quadrigrammes allemands moyens par bloc ; « clé commune » = somme sur les 5 blocs 13×13.
   Compilation : gcc -O3 -march=native -fopenmp -o affine tools/k29/affine.c -lm
   Usage : affine qg.bin chiffre.txt TOPN */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
static float *QG;
static int BL[6] = {166, 169, 162, 169, 169, 144}, BO[6];
static unsigned char C[1000];
static double score(const unsigned char *p, int L) {
  double s = 0; int x = (p[0] * 26 + p[1]) * 26 + p[2];
  for (int i = 3; i < L; i++) { x = (x * 26 + p[i]) % 456976; s += QG[x]; }
  return s / (L - 3);
}
/* construit la permutation de déchiffrement : P[k] = C[src[k]], k < len */
static void build(int n, int a, int b, int c, int d, int r0, int c0, int dir, int len, int *src) {
  int N = n * n, cell[200], valid[200], rank[200];
  for (int k = 0; k < N; k++) { int q = k / n, r = k % n;
    int row = ((r0 + a * r + b * q) % n + n) % n, col = ((c0 + c * r + d * q) % n + n) % n; cell[k] = row * n + col; }
  if (dir == 0) { /* case cell[k] contient P[k] si k < len ; chiffré = cases valides en lignes */
    for (int x = 0; x < N; x++) valid[x] = 0;
    for (int k = 0; k < len; k++) valid[cell[k]] = 1;
    int j = 0; for (int x = 0; x < N; x++) rank[x] = valid[x] ? j++ : -1;
    for (int k = 0; k < len; k++) src[k] = rank[cell[k]];
  } else { /* clair en lignes (case x contient P[x] si x < len) ; chiffré = cases valides dans l'ordre de la marche */
    int j = 0; for (int k = 0; k < N; k++) { int x = cell[k]; if (x < len) src[x] = j++; }
  }
}
typedef struct { double s; int a, b, c, d, r0, c0, dir, blk; } Hit;
static void push(Hit *H, int *h, int T, Hit x) {
  if (*h < T) { H[(*h)++] = x; return; }
  int mi = 0; for (int i = 1; i < T; i++) if (H[i].s < H[mi].s) mi = i;
  if (x.s > H[mi].s) H[mi] = x;
}
static int cmp(const void *x, const void *y) { double a = ((Hit *)x)->s, b = ((Hit *)y)->s; return a < b ? 1 : a > b ? -1 : 0; }
static void show(const char *title, Hit *H, int h, int T) {
  qsort(H, h, sizeof(Hit), cmp); printf("%s\n", title);
  for (int i = 0; i < h && i < T; i++) {
    int n = H[i].blk == 5 ? 12 : 13, src[200], len = H[i].blk < 0 ? 169 : BL[H[i].blk]; int blk = H[i].blk < 0 ? 1 : H[i].blk;
    build(n, H[i].a, H[i].b, H[i].c, H[i].d, H[i].r0, H[i].c0, H[i].dir, BL[blk], src); (void)len;
    printf("  %8.4f bloc %s  [[%d,%d],[%d,%d]] départ (%d,%d) sens %d  ", H[i].s, H[i].blk < 0 ? "S1-S5" : (char[]){'S', '1' + H[i].blk, 0},
           H[i].a, H[i].b, H[i].c, H[i].d, H[i].r0, H[i].c0, H[i].dir);
    for (int k = 0; k < 60 && k < BL[blk]; k++) putchar('a' + C[BO[blk] + src[k]]);
    putchar('\n');
  }
}
int main(int argc, char **argv) {
  QG = malloc(456976 * sizeof(float)); FILE *f = fopen(argv[1], "rb");
  if (!f || fread(QG, 4, 456976, f) != 456976) return 1; fclose(f);
  f = fopen(argv[2], "r"); int L = 0, ch; while ((ch = fgetc(f)) != EOF) { if (ch >= 'a' && ch <= 'z') C[L++] = ch - 'a'; } fclose(f);
  if (L != 979) { fprintf(stderr, "L=%d\n", L); return 1; }
  int T = argc > 3 ? atoi(argv[3]) : 10; for (int i = 0, o = 0; i < 6; i++) { BO[i] = o; o += BL[i]; }
  int nt = omp_get_max_threads();
  Hit *HC = calloc(nt * T, sizeof(Hit)), *HB = calloc(nt * 6 * T, sizeof(Hit)); int *hc = calloc(nt, sizeof(int)), *hb = calloc(nt * 6, sizeof(int));
  long long cnt13 = 0, cnt12 = 0;
  /* 13×13 : blocs S1–S5 */
  #pragma omp parallel for schedule(dynamic) reduction(+:cnt13)
  for (int ab = 0; ab < 169; ab++) {
    int t = omp_get_thread_num(), a = ab / 13, b = ab % 13, src[200]; unsigned char P[200];
    for (int c = 0; c < 13; c++) for (int d = 0; d < 13; d++) {
      if (((a * d - b * c) % 13 + 13) % 13 == 0) continue;
      for (int r0 = 0; r0 < 13; r0++) for (int c0 = 0; c0 < 13; c0++) for (int dir = 0; dir < 2; dir++) {
        double tot = 0;
        for (int k = 0; k < 5; k++) {
          build(13, a, b, c, d, r0, c0, dir, BL[k], src);
          for (int i = 0; i < BL[k]; i++) P[i] = C[BO[k] + src[i]];
          double s = score(P, BL[k]); tot += s;
          Hit x = {s, a, b, c, d, r0, c0, dir, k}; push(HB + (t * 6 + k) * T, &hb[t * 6 + k], T, x);
        }
        Hit y = {tot / 5, a, b, c, d, r0, c0, dir, -1}; push(HC + t * T, &hc[t], T, y); cnt13++;
      }
    }
  }
  /* 12×12 : bloc S6, marches affines inversibles mod 12 */
  #pragma omp parallel for schedule(dynamic) reduction(+:cnt12)
  for (int ab = 0; ab < 144; ab++) {
    int t = omp_get_thread_num(), a = ab / 12, b = ab % 12, src[200]; unsigned char P[200];
    for (int c = 0; c < 12; c++) for (int d = 0; d < 12; d++) {
      int det = ((a * d - b * c) % 12 + 12) % 12; if (det % 2 == 0 || det % 3 == 0) continue;
      for (int r0 = 0; r0 < 12; r0++) for (int c0 = 0; c0 < 12; c0++) for (int dir = 0; dir < 2; dir++) {
        build(12, a, b, c, d, r0, c0, dir, 144, src);
        for (int i = 0; i < 144; i++) P[i] = C[BO[5] + src[i]];
        Hit x = {score(P, 144), a, b, c, d, r0, c0, dir, 5}; push(HB + (t * 6 + 5) * T, &hb[t * 6 + 5], T, x); cnt12++;
      }
    }
  }
  printf("marches 13x13 essayées : %lld (x 5 blocs) ; marches 12x12 : %lld\n", cnt13, cnt12);
  /* carré magique doublement pair 12×12 (méthode des diagonales), 8 symétries, 2 sens */
  { int M[144]; double best = -99; char lab[64] = "";
    for (int i = 0; i < 12; i++) for (int j = 0; j < 12; j++) { int v = i * 12 + j; int di = (i % 4 == j % 4) || ((i % 4) + (j % 4) == 3); M[v] = di ? 143 - v : v; }
    unsigned char P[200];
    for (int sym = 0; sym < 8; sym++) for (int dir = 0; dir < 2; dir++) {
      int src[144];
      for (int i = 0; i < 12; i++) for (int j = 0; j < 12; j++) {
        int ii = i, jj = j; if (sym & 1) jj = 11 - jj; if (sym & 2) ii = 11 - ii; if (sym & 4) { int t2 = ii; ii = jj; jj = t2; }
        int cellx = i * 12 + j, k = M[ii * 12 + jj];           /* la case (i,j) porte le nombre k */
        if (dir == 0) src[k] = cellx; else src[cellx] = k;
      }
      for (int i = 0; i < 144; i++) P[i] = C[BO[5] + src[i]];
      double s = score(P, 144); if (s > best) { best = s; sprintf(lab, "sym %d sens %d", sym, dir); }
    }
    printf("carré magique 12x12 doublement pair : meilleure note %.4f (%s)\n", best, lab); }
  Hit *all = malloc(sizeof(Hit) * nt * T); int m = 0;
  for (int t = 0; t < nt; t++) for (int i = 0; i < hc[t]; i++) all[m++] = HC[t * T + i];
  show("== clé commune aux blocs S1-S5 (moyenne des 5 notes)", all, m, T);
  for (int k = 0; k < 6; k++) { m = 0; for (int t = 0; t < nt; t++) for (int i = 0; i < hb[t * 6 + k]; i++) all[m++] = HB[(t * 6 + k) * T + i];
    char title[64]; sprintf(title, "== bloc S%d seul", k + 1); show(title, all, m, 3); }
  /* La Loubère explicite, départ classique (milieu de la première ligne), pour mémoire */
  { int src[200]; unsigned char P[200]; printf("== La Loubère classique (a=-1,b=2,c=1,d=-1, départ (0,6)) :");
    for (int dir = 0; dir < 2; dir++) for (int k = 0; k < 5; k++) { build(13, -1, 2, 1, -1, 0, 6, dir, BL[k], src);
      for (int i = 0; i < BL[k]; i++) P[i] = C[BO[k] + src[i]]; printf(" S%d/sens%d %.3f", k + 1, dir, score(P, BL[k])); }
    printf("\n"); }
  return 0;
}
