/* K19 — anagramme par tranches : le flux est découpé en tranches (longueurs données) ; un recuit permute les lettres
   à l'intérieur de chaque tranche ; le score est la somme des quadrigrammes allemands sur TOUT le texte (raccords
   entre tranches compris). Usage : chunkana qg.bin flux.txt tranches.txt restarts iters seed
   tranches.txt : longueurs des tranches successives (entiers), somme = longueur du flux. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float QG[456976];
static unsigned long long rs;
static double rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (rs>>11)*(1.0/9007199254740992.0); }
static int t[4096], n, cs_[4096], ce_[4096], nc, chunk_of[4096];
static double q4(const int*x,int i){ return QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]]; }
static double total(const int*x){ double s=0; for(int i=0;i+3<n;i++) s+=q4(x,i); return s; }
/* local rescoring for positions in [a,b] : quadgrams starting in [a-3,b] */
static double local(const int*x,int a,int b){ double s=0; int lo=a-3<0?0:a-3, hi=b>n-4?n-4:b; for(int i=lo;i<=hi;i++) s+=q4(x,i); return s; }
int main(int argc,char**argv){
    if(argc<7){fprintf(stderr,"usage\n");return 1;}
    FILE*fp=fopen(argv[1],"rb"); if(!fp||fread(QG,4,456976,fp)!=456976) return 1; fclose(fp);
    fp=fopen(argv[2],"r"); int c; n=0; while((c=fgetc(fp))!=EOF) if(c>='a'&&c<='z') t[n++]=c-'a'; fclose(fp);
    fp=fopen(argv[3],"r"); int L, pos=0; nc=0; while(fscanf(fp,"%d",&L)==1){ cs_[nc]=pos; ce_[nc]=pos+L-1; for(int i=pos;i<pos+L&&i<n;i++) chunk_of[i]=nc; pos+=L; nc++; } fclose(fp);
    if(pos!=n){fprintf(stderr,"chunk sum %d != n %d\n",pos,n);return 1;}
    int R=atoi(argv[4]); long I=atol(argv[5]); rs=strtoull(argv[6],0,10)|1;
    static int best[4096], cur[4096]; double bs=-1e18;
    for(int r=0;r<R;r++){
        memcpy(cur,t,sizeof(int)*n);
        for(int k=0;k<nc;k++) for(int i=ce_[k];i>cs_[k];i--){ int j=cs_[k]+(int)(rnd()*(i-cs_[k]+1)); int x=cur[i];cur[i]=cur[j];cur[j]=x; }
        double s=total(cur);
        for(long it=0;it<I;it++){
            double T=2.0*(1.0-(double)it/I)+0.02;
            int k=(int)(rnd()*nc); int len=ce_[k]-cs_[k]+1; if(len<2) continue;
            int a=cs_[k]+(int)(rnd()*len), b=cs_[k]+(int)(rnd()*len); if(a==b) continue;
            if(a>b){int x=a;a=b;b=x;}
            double before=local(cur,a,b);
            int m=(int)(rnd()*3); static int sav[4096]; memcpy(sav+a,cur+a,sizeof(int)*(b-a+1));
            if(m==0){int x=cur[a];cur[a]=cur[b];cur[b]=x;}
            else if(m==1){int i=a,j=b; while(i<j){int x=cur[i];cur[i]=cur[j];cur[j]=x;i++;j--;}}
            else {int x=cur[a]; memmove(cur+a,cur+a+1,sizeof(int)*(b-a)); cur[b]=x;}
            double after=local(cur,a,b), d=after-before;
            if(d>=0 || rnd()<exp(d/T)) s+=d; else memcpy(cur+a,sav+a,sizeof(int)*(b-a+1));
        }
        if(s>bs){bs=s; memcpy(best,cur,sizeof(int)*n);}
    }
    printf("%.5f ",bs/(n-3)); for(int i=0;i<n;i++) putchar('a'+best[i]); putchar('\n');
    return 0;
}
