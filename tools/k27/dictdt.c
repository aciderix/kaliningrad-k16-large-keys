/* K27 — double transposition en colonnes à clés-mots : attaque exhaustive sur un dictionnaire de clés.
   Pour chaque paire (clé A, clé B) d'une liste de clés (rangs déjà calculés), et pour chacune des 4 conventions
   (clé lue « à l'endroit » ou « à l'envers » à chaque étape), déchiffre C = T_B(T_A(P)) et note le clair aux
   quadrigrammes allemands (data/models/qg_de.bin). Criblage sur les PREF premières lettres, puis note complète.
   Mode "blocks" : chaque bloc de la bouteille (166,169,162,169,169,144) chiffré séparément avec la même paire.
   Compilation : gcc -O3 -march=native -fopenmp -o dictdt tools/k27/dictdt.c -lm
   Usage : dictdt qg.bin chiffre.txt clesA.txt clesB.txt whole|blocks PREF SEUIL TOPN [masque_variantes=51]
   Variantes v = va*4+vb, va et vb dans 0..3 : bit 0 = ordre de la clé à l'envers, bit 1 = sens inverse de l'étape
   (écrire en colonnes dans l'ordre de la clé, lire en lignes). Masque sur 16 bits ; 51 (défaut) = les 4 variantes de base
   (va, vb dans {0,1}) ; 65535 = toutes.
   Fichier de clés : une clé par ligne, « étiquette<TAB>n r0 r1 … r(n-1) » (r = rang 0..n-1 de chaque colonne). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef unsigned short u16;
static float *QG;
typedef struct { char lab[64]; int n; int r[64]; } Key;
static Key *load_keys(const char *f, int *cnt) {
  FILE *fp = fopen(f, "r"); if (!fp) { perror(f); exit(1); }
  int cap = 1024, k = 0; Key *K = malloc(cap * sizeof(Key)); char line[4096];
  while (fgets(line, sizeof line, fp)) {
    char *t = strchr(line, '\t'); if (!t) continue; *t = 0;
    if (k == cap) { cap *= 2; K = realloc(K, cap * sizeof(Key)); }
    strncpy(K[k].lab, line, 63); K[k].lab[63] = 0;
    char *p = t + 1; int n = strtol(p, &p, 10); if (n < 2 || n > 64) continue;
    K[k].n = n; for (int i = 0; i < n; i++) K[k].r[i] = strtol(p, &p, 10);
    k++;
  }
  fclose(fp); *cnt = k; return K;
}
/* e[j] = indice du clair lu en j-ième position du chiffré (transposition en colonnes incomplète) */
static void enc_perm(const Key *K, int inv, int L, int *e) {
  int n = K->n, order[64];
  for (int c = 0; c < n; c++) { if (inv) order[c] = K->r[c]; else order[K->r[c]] = c; }
  int j = 0;
  for (int t = 0; t < n; t++) { int c = order[t]; for (int i = c; i < L; i += n) e[j++] = i; }
}
static void inv_perm(const int *e, int L, u16 *d) { for (int j = 0; j < L; j++) d[e[j]] = (u16)j; }
static inline double score(const unsigned char *p, int L) {
  double s = 0; int x = (p[0] * 26 + p[1]) * 26 + p[2];
  for (int i = 3; i < L; i++) { x = (x * 26 + p[i]) % 456976; s += QG[x]; }
  return s / (L - 3);
}
typedef struct { double s; int a, b, v; } Hit;
int main(int argc, char **argv) {
  if (argc < 9) { fprintf(stderr, "usage\n"); return 1; }
  QG = malloc(456976 * sizeof(float));
  FILE *fq = fopen(argv[1], "rb"); if (!fq || fread(QG, sizeof(float), 456976, fq) != 456976) { fprintf(stderr, "qg\n"); return 1; } fclose(fq);
  FILE *fc = fopen(argv[2], "r"); int L = 0; unsigned char C[8192]; int ch;
  while ((ch = fgetc(fc)) != EOF) { if (ch >= 'a' && ch <= 'z') C[L++] = ch - 'a'; }
  fclose(fc);
  int nA, nB; Key *KA = load_keys(argv[3], &nA), *KB = load_keys(argv[4], &nB);
  int blocks = !strcmp(argv[5], "blocks"); int PREF = atoi(argv[6]); double THR = atof(argv[7]); int TOPN = atoi(argv[8]);
  int vmask = argc > 9 ? atoi(argv[9]) : 51;
  int nb = 1, bl[8] = {L}, bo[8] = {0};
  if (blocks) { int B[6] = {166, 169, 162, 169, 169, 144}; nb = 6; int o = 0; for (int i = 0; i < 6; i++) { bl[i] = B[i]; bo[i] = o; o += B[i]; } if (o != L) { fprintf(stderr, "L=%d != 979\n", L); return 1; } }
  fprintf(stderr, "L=%d clesA=%d clesB=%d mode=%s pref=%d seuil=%.2f\n", L, nA, nB, blocks ? "blocks" : "whole", PREF, THR);
  /* permutations inverses précalculées : d[v][key][block] */
  /* y = e^-1 (étape directe) ou e (étape inverse), pour chaque ordre de clé ; t = sens*2 + ordre */
  u16 *DA[4] = {0}, *DB[4] = {0}; size_t sz = (size_t)L;
  int *e = malloc(sizeof(int) * L);
  int needA[4] = {0}, needB[4] = {0};
  for (int v = 0; v < 16; v++) if (vmask >> v & 1) { needA[v / 4] = 1; needB[v % 4] = 1; }
  for (int t = 0; t < 4; t++) {
    int inv = t & 1, dir = t >> 1;
    if (needA[t]) { DA[t] = malloc(sz * nA * sizeof(u16));
      for (int k = 0; k < nA; k++) for (int b = 0; b < nb; b++) { u16 *y = DA[t] + (size_t)k * L + bo[b]; enc_perm(&KA[k], inv, bl[b], e);
        if (dir) for (int j = 0; j < bl[b]; j++) y[j] = (u16)e[j]; else inv_perm(e, bl[b], y); } }
    if (needB[t]) { DB[t] = malloc(sz * nB * sizeof(u16));
      for (int k = 0; k < nB; k++) for (int b = 0; b < nb; b++) { u16 *y = DB[t] + (size_t)k * L + bo[b]; enc_perm(&KB[k], inv, bl[b], e);
        if (dir) for (int j = 0; j < bl[b]; j++) y[j] = (u16)e[j]; else inv_perm(e, bl[b], y); } }
  }
  int nt = omp_get_max_threads();
  Hit *hits = malloc(sizeof(Hit) * (size_t)nt * TOPN); int *nh = calloc(nt, sizeof(int));
  long long hist[64] = {0}; long long passed = 0, total = 0;
  #pragma omp parallel
  {
    int tid = omp_get_thread_num(); Hit *H = hits + (size_t)tid * TOPN; int h = 0; double hmin = -1e9; int hmi = 0;
    unsigned char P[8192]; long long lhist[64] = {0}; long long lp = 0, lt = 0;
    #pragma omp for schedule(dynamic, 4)
    for (int a = 0; a < nA; a++) {
      for (int va = 0; va < 4; va++) for (int vb = 0; vb < 4; vb++) {
        int v = va * 4 + vb; if (!(vmask >> v & 1)) continue;
        const u16 *da = DA[va] + (size_t)a * L;
        for (int b = 0; b < nB; b++) {
          const u16 *db = DB[vb] + (size_t)b * L; double s;
          if (!blocks) {
            for (int i = 0; i < PREF; i++) P[i] = C[db[da[i]]];
            s = score(P, PREF);
          } else { /* criblage sur le premier bloc */
            int m = PREF < bl[0] ? PREF : bl[0];
            for (int i = 0; i < m; i++) P[i] = C[db[da[i]]];
            s = score(P, m);
          }
          lt++; int hb = (int)((s + 16) * 8); if (hb < 0) hb = 0; if (hb > 63) hb = 63; lhist[hb]++;
          if (s < THR) continue;
          lp++;
          double full = 0;
          if (!blocks) { for (int i = 0; i < L; i++) P[i] = C[db[da[i]]]; full = score(P, L); }
          else { double tot = 0; int nq = 0;
            for (int q = 0; q < nb; q++) { int o = bo[q]; for (int i = 0; i < bl[q]; i++) P[i] = C[o + db[o + da[o + i]]];
              tot += score(P, bl[q]) * (bl[q] - 3); nq += bl[q] - 3; }
            full = tot / nq; }
          if (h < TOPN) { H[h].s = full; H[h].a = a; H[h].b = b; H[h].v = v; h++; if (h == TOPN) { hmin = 1e9; for (int i = 0; i < h; i++) if (H[i].s < hmin) { hmin = H[i].s; hmi = i; } } }
          else if (full > hmin) { H[hmi].s = full; H[hmi].a = a; H[hmi].b = b; H[hmi].v = v; hmin = 1e9; for (int i = 0; i < h; i++) if (H[i].s < hmin) { hmin = H[i].s; hmi = i; } }
        }
      }
    }
    nh[tid] = h;
    #pragma omp critical
    { for (int i = 0; i < 64; i++) hist[i] += lhist[i]; passed += lp; total += lt; }
  }
  /* fusion et tri */
  int m = 0; Hit *all = malloc(sizeof(Hit) * (size_t)nt * TOPN);
  for (int t = 0; t < nt; t++) for (int i = 0; i < nh[t]; i++) all[m++] = hits[(size_t)t * TOPN + i];
  for (int i = 1; i < m; i++) { Hit x = all[i]; int j = i - 1; while (j >= 0 && all[j].s < x.s) { all[j + 1] = all[j]; j--; } all[j + 1] = x; }
  printf("paires x variantes notees : %lld ; au-dessus du seuil %.2f : %lld\n", total, THR, passed);
  printf("histogramme du criblage (score par quadrigramme, pas 0,125) :\n");
  for (int i = 0; i < 64; i++) if (hist[i]) printf("  %7.3f %lld\n", -16 + i / 8.0, hist[i]);
  unsigned char P[8192];
  for (int i = 0; i < m && i < TOPN; i++) {
    int va = all[i].v / 4, vb = all[i].v % 4; const u16 *da = DA[va] + (size_t)all[i].a * L, *db = DB[vb] + (size_t)all[i].b * L;
    for (int q = 0; q < nb; q++) { int o = bo[q]; for (int j = 0; j < bl[q]; j++) P[o + j] = C[o + db[o + da[o + j]]]; }
    printf("%8.4f  A=%s  B=%s  v=%d%d  ", all[i].s, KA[all[i].a].lab, KB[all[i].b].lab, va, vb);
    for (int j = 0; j < L && j < 120; j++) { putchar('a' + P[j]); }
    putchar('\n');
  }
  return 0;
}
