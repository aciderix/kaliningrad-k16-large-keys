/* K21 — grille tournante n×n (n pair ou impair), recherche par recuit sur les choix de trous (une case par orbite),
   pour chaque configuration (décalage 0..n²-1, sens du clair, sens de rotation, lecture lignes/colonnes).
   Score : log-rapports de bigrammes allemands (matrice P 26×26) entre lettres consécutives du clair, par paire.
   Usage : grille_sa n P.txt flux.txt restarts iters seed   → meilleure configuration et clair. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
static double P[26][26]; static int x[4096], N;
static int orb[64][4], K, center=-1, n, p;
static void seqof(const int*ch,int ccw,int colm,int*seq){ int L=0, cells[64];
  for(int r=0;r<4;r++){ int m=0; for(int i=0;i<K;i++){ int t=(ch[i]+(ccw?(4-r)%4:r))%4; cells[m++]=orb[i][t]; }
    for(int a=1;a<m;a++){int v=cells[a],b=a-1; while(b>=0&&cells[b]>v){cells[b+1]=cells[b];b--;} cells[b+1]=v;}
    for(int i=0;i<m;i++) seq[L++]=cells[i]; if(r==0&&center>=0) seq[L++]=center; }
  if(colm) for(int i=0;i<L;i++){int rr=seq[i]/n,cc=seq[i]%n; seq[i]=cc*n+rr;} }
int main(int argc,char**argv){
  n=atoi(argv[1]); p=n*n; FILE*f=fopen(argv[2],"r"); for(int i=0;i<26;i++)for(int j=0;j<26;j++) if(fscanf(f,"%lf",&P[i][j])!=1) return 1; fclose(f);
  f=fopen(argv[3],"r"); int c; N=0; while((c=fgetc(f))!=EOF) if(c>='a'&&c<='z') x[N++]=c-'a'; fclose(f);
  int R=atoi(argv[4]); long I=atol(argv[5]); unsigned long long seed=strtoull(argv[6],0,10);
  int seen[256]={0}; K=0;
  for(int r=0;r<n;r++) for(int cc=0;cc<n;cc++){ int id=r*n+cc; if(seen[id]) continue; int rr=r,c2=cc;
    for(int t=0;t<4;t++){ orb[K][t]=rr*n+c2; seen[rr*n+c2]=1; int nr=c2,nc=n-1-rr; rr=nr; c2=nc; }
    if(orb[K][0]==orb[K][1]) center=orb[K][0]; else K++; }
  int NC=p*2*2*2; double gbest=-1e18; int gcfg=-1, gch[64];
  #pragma omp parallel for schedule(dynamic,1)
  for(int cfg=0; cfg<NC; cfg++){
    int off=cfg/8, rv=(cfg>>2)&1, ccw=(cfg>>1)&1, colm=cfg&1;
    double *S=calloc(p*p,sizeof(double)), *Sw=calloc(p*p,sizeof(double)); int cnt=0, prev=-1;
    for(int st=off; st+p<=N; st+=p){ for(int i=0;i<p;i++) for(int j=0;j<p;j++) S[i*p+j]+= rv? P[x[st+j]][x[st+i]] : P[x[st+i]][x[st+j]];
      if(prev>=0) for(int i=0;i<p;i++) for(int j=0;j<p;j++) Sw[i*p+j]+= rv? P[x[st+j]][x[prev+i]] : P[x[prev+i]][x[st+j]]; prev=st; cnt++; }
    int nb=cnt*(p-1)+cnt-1; unsigned long long rs=seed*1000003ULL+cfg*7919ULL+1;
    double lbest=-1e18; int lch[64];
    for(int r=0;r<R;r++){ int ch[64], seq[256]; for(int i=0;i<K;i++){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; ch[i]=rs%4; }
      seqof(ch,ccw,colm,seq); double sc=0; for(int i=0;i+1<p;i++) sc+=S[seq[i]*p+seq[i+1]]; sc+=Sw[seq[p-1]*p+seq[0]];
      for(long it=0; it<I; it++){ double T=(2.0*(1.0-(double)it/I)+0.01)*nb/100.0;
        rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; int o=rs%K; int old=ch[o]; rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; ch[o]=(old+1+rs%3)%4;
        seqof(ch,ccw,colm,seq); double ns=0; for(int i=0;i+1<p;i++) ns+=S[seq[i]*p+seq[i+1]]; ns+=Sw[seq[p-1]*p+seq[0]];
        rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; double u=(rs>>11)*(1.0/9007199254740992.0);
        if(ns>=sc || u<exp((ns-sc)/T)) sc=ns; else ch[o]=old; }
      if(sc>lbest){ lbest=sc; memcpy(lch,ch,sizeof(int)*K);} }
    lbest/=nb;
    #pragma omp critical
    { if(lbest>gbest){ gbest=lbest; gcfg=cfg; memcpy(gch,lch,sizeof(int)*K);} }
    free(S); free(Sw); }
  int off=gcfg/8, rv=(gcfg>>2)&1, ccw=(gcfg>>1)&1, colm=gcfg&1, seq[256]; seqof(gch,ccw,colm,seq);
  printf("n=%d best=%.4f offset=%d rev=%d ccw=%d colmajor=%d grille=",n,gbest,off,rv,ccw,colm); for(int i=0;i<K;i++) printf("%d",gch[i]); printf("\nclair: ");
  char out[4096]; int L=0; for(int st=off; st+p<=N && L<400; st+=p) for(int i=0;i<p;i++) out[L++]='a'+x[st+seq[i]];
  if(rv){ for(int i=0;i<L/2;i++){char t=out[i];out[i]=out[L-1-i];out[L-1-i]=t;} } out[L<200?L:200]=0; printf("%s\n",out);
  return 0; }
