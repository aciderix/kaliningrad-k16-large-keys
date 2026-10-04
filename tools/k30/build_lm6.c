/* K30 — modèle de langue allemand à 6-grammes de lettres (contexte de 5 lettres), lissage de Witten-Bell jusqu'à
   l'unigramme, tolérant aux nuls : P'(x|h) = (1−λ)·P(x|h) + λ/26. Table dense 26^6 de log P' quantifiés sur un octet
   (q = round(−ln P' × 16), plafonné à 255).
   Compilation : gcc -O3 -o build_lm6 tools/k30/build_lm6.c -lm
   Usage : build_lm6 lettres.txt lambda sortie.bin   (lettres.txt : a–z seulement) */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long n = ftell(f); fseek(f, 0, SEEK_SET);
  unsigned char *t = malloc(n); if (fread(t, 1, n, f) != (size_t)n) return 1; fclose(f);
  long m = 0; for (long i = 0; i < n; i++) if (t[i] >= 'a' && t[i] <= 'z') t[m++] = t[i] - 'a';
  double lam = atof(argv[2]);
  long sz[7]; sz[0] = 1; for (int k = 1; k <= 6; k++) sz[k] = sz[k - 1] * 26;
  uint32_t *c[7]; for (int k = 1; k <= 6; k++) c[k] = calloc(sz[k], 4);
  for (long i = 0; i < m; i++) { long idx = 0; for (int k = 1; k <= 6 && i - k + 1 >= 0; k++) { idx = 0; for (long j = i - k + 1; j <= i; j++) idx = idx * 26 + t[j]; c[k][idx]++; } }
  fprintf(stderr, "%ld lettres\n", m);
  /* P_k(x | h) pour les ordres 1..6, tables float pour 1..5, octet pour 6 */
  float *P[6]; P[1] = malloc(sizeof(float) * 26);
  { double tot = 0; for (int x = 0; x < 26; x++) tot += c[1][x] + 1; for (int x = 0; x < 26; x++) P[1][x] = (c[1][x] + 1) / tot; }
  for (int k = 2; k <= 5; k++) {
    P[k] = malloc(sizeof(float) * sz[k]);
    for (long h = 0; h < sz[k - 1]; h++) {
      double ch = 0, nf = 0; for (int x = 0; x < 26; x++) { uint32_t v = c[k][h * 26 + x]; ch += v; nf += v > 0; }
      long hs = h % sz[k - 2];  /* contexte raccourci (on retire la lettre la plus ancienne) */
      for (int x = 0; x < 26; x++) { double lower = P[k - 1][hs * 26 + x];
        P[k][h * 26 + x] = ch > 0 ? (c[k][h * 26 + x] + nf * lower) / (ch + nf) : lower; }
    }
  }
  uint8_t *Q = malloc(sz[6]);
  for (long h = 0; h < sz[5]; h++) {
    double ch = 0, nf = 0; for (int x = 0; x < 26; x++) { uint32_t v = c[6][h * 26 + x]; ch += v; nf += v > 0; }
    long hs = h % sz[4];
    for (int x = 0; x < 26; x++) { double lower = P[5][hs * 26 + x];
      double p = ch > 0 ? (c[6][h * 26 + x] + nf * lower) / (ch + nf) : lower;
      p = (1 - lam) * p + lam / 26; double q = -log(p) * 16; Q[h * 26 + x] = q > 255 ? 255 : (uint8_t)(q + 0.5); }
  }
  f = fopen(argv[3], "wb"); fwrite(Q, 1, sz[6], f); fclose(f);
  fprintf(stderr, "écrit %ld octets\n", sz[6]); return 0;
}
