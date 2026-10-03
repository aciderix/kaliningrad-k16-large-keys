/* K19 — grille tournante n×n (n impair ou pair, n ≤ 8), recherche exhaustive des 4^k grilles, en C (OpenMP).
   Pour chaque grille : ordre de lecture (rotation horaire ou antihoraire), chiffré lu en lignes ou en colonnes ;
   pour chaque alignement (décalage 0..n²-1) et sens du clair (direct / inversé), score = somme des log-rapports de
   bigrammes allemands entre lettres consécutives du clair, normalisée par paire. Entrées : matrice P (26×26, texte),
   flux (a-z). Usage : grille7 n P.txt flux.txt [topk] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
static double P[26][26];
static int x[4096], N;
int main(int argc,char**argv){
    int n=atoi(argv[1]), p=n*n;
    FILE*f=fopen(argv[2],"r"); for(int i=0;i<26;i++) for(int j=0;j<26;j++) if(fscanf(f,"%lf",&P[i][j])!=1) return 1; fclose(f);
    f=fopen(argv[3],"r"); int c; N=0; while((c=fgetc(f))!=EOF) if(c>='a'&&c<='z') x[N++]=c-'a'; fclose(f);
    /* orbits */
    int orb[32][4], k=0, center=-1, seen[64]={0};
    for(int r=0;r<n;r++) for(int cc=0;cc<n;cc++){ int id=r*n+cc; if(seen[id]) continue; int rr=r,c2=cc;
        for(int t=0;t<4;t++){ orb[k][t]=rr*n+c2; seen[rr*n+c2]=1; int nr=c2, nc=n-1-rr; rr=nr; c2=nc; }
        if(orb[k][0]==orb[k][1]){ center=orb[k][0]; } else k++; }
    /* configurations : offset a, rev ; S[a][rev][i][j] over cells */
    int NA=p, NC=NA*2;
    double *S=malloc(sizeof(double)*NC*p*p), *Sw=malloc(sizeof(double)*NC*p*p); int *nb=malloc(sizeof(int)*NC);
    for(int a=0;a<NA;a++) for(int rv=0;rv<2;rv++){ int cf=a*2+rv; double*s=S+(size_t)cf*p*p,*w=Sw+(size_t)cf*p*p; memset(s,0,sizeof(double)*p*p); memset(w,0,sizeof(double)*p*p); int cnt=0, prev=-1;
        for(int st=a; st+p<=N; st+=p){ for(int i=0;i<p;i++) for(int j=0;j<p;j++) s[i*p+j]+= rv? P[x[st+j]][x[st+i]] : P[x[st+i]][x[st+j]];
            if(prev>=0) for(int i=0;i<p;i++) for(int j=0;j<p;j++) w[i*p+j]+= rv? P[x[st+j]][x[prev+i]] : P[x[prev+i]][x[st+j]];
            prev=st; cnt++; }
        nb[cf]=cnt*(p-1)+(cnt-1); }
    long long total=1; for(int i=0;i<k;i++) total*=4;
    double gbest=-1e18; long long gbest_g=0; int gbest_cfg=0, gbest_var=0;
    #pragma omp parallel
    { double lbest=-1e18; long long lg=0; int lc=0, lv=0; int seq[64], cells[4][32];
      #pragma omp for schedule(dynamic,4096)
      for(long long g=0; g<total; g++){
        int ch[32]; long long gg=g; for(int i=0;i<k;i++){ ch[i]=gg%4; gg/=4; }
        for(int var=0; var<4; var++){ int ccw=var&1, colm=var>>1, L=0;
          for(int r=0;r<4;r++){ int m=0; for(int i=0;i<k;i++){ int t=(ch[i]+(ccw? (4-r)%4 : r))%4; cells[r][m++]=orb[i][t]; }
            for(int a2=1;a2<m;a2++){ int v=cells[r][a2], b2=a2-1; while(b2>=0&&cells[r][b2]>v){cells[r][b2+1]=cells[r][b2]; b2--;} cells[r][b2+1]=v; }
            for(int i=0;i<m;i++) seq[L++]=cells[r][i];
            if(r==0 && center>=0) seq[L++]=center; }
          if(colm) for(int i=0;i<L;i++){ int rr=seq[i]/n, cc=seq[i]%n; seq[i]=cc*n+rr; }
          for(int cf=0; cf<NC; cf++){ const double*s=S+(size_t)cf*p*p; double sc=0; for(int i=0;i+1<p;i++) sc+=s[seq[i]*p+seq[i+1]]; sc+=Sw[(size_t)cf*p*p+seq[p-1]*p+seq[0]]; sc/=nb[cf];
            if(sc>lbest){ lbest=sc; lg=g; lc=cf; lv=var; } } } }
      #pragma omp critical
      { if(lbest>gbest){ gbest=lbest; gbest_g=lg; gbest_cfg=lc; gbest_var=lv; } } }
    printf("n=%d grilles=%lld best=%.4f grille=%lld offset=%d rev=%d ccw=%d colmajor=%d\n",n,total,gbest,gbest_g,gbest_cfg/2,gbest_cfg%2,gbest_var&1,gbest_var>>1);
    return 0;
}
