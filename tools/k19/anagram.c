/* K19 — anagramme d'une ligne : recuit sur l'ordre des lettres d'une ligne (multiensemble fixé), noté par les
   quadrigrammes allemands joints (data/models/qg_de.bin). Usage : anagram qg.bin restarts iters seed [D] < lignes.txt (D : déplacement maximal de chaque lettre, 0 = libre)
   Chaque ligne d'entrée (a-z) donne : score moyen par quadrigramme, meilleur arrangement. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float QG[456976];
static unsigned long long rs;
static double rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (rs>>11)*(1.0/9007199254740992.0); }
static double score(const int *t,int n){ double s=0; for(int i=0;i+3<n;i++) s+=QG[((t[i]*26+t[i+1])*26+t[i+2])*26+t[i+3]]; return s; }
int main(int argc,char**argv){
    if(argc<5){fprintf(stderr,"usage\n");return 1;}
    FILE*fp=fopen(argv[1],"rb"); if(!fp||fread(QG,4,456976,fp)!=456976){fprintf(stderr,"qg?\n");return 1;} fclose(fp);
    int R=atoi(argv[2]); long I=atol(argv[3]); rs=strtoull(argv[4],0,10)|1; int D=argc>5?atoi(argv[5]):0;
    char line[4096];
    while(fgets(line,sizeof line,stdin)){
        int t[512],n=0; for(char*c=line;*c;c++) if(*c>='a'&&*c<='z') t[n++]=*c-'a';
        if(n<5){printf("0 -\n");continue;}
        int best[512]; double bs=-1e18;
        for(int r=0;r<R;r++){
            int cur[512], org[512]; for(int i=0;i<n;i++){cur[i]=t[i];org[i]=i;}
            if(!D) for(int i=n-1;i>0;i--){int j=(int)(rnd()*(i+1)); int x=cur[i];cur[i]=cur[j];cur[j]=x; x=org[i];org[i]=org[j];org[j]=x;}
            double cs=score(cur,n);
            for(long it=0;it<I;it++){
                double T=3.0*(1.0-(double)it/I)+0.05;
                int a=(int)(rnd()*n), b=(int)(rnd()*n);
                if(D){ b=a+(int)(rnd()*(4*D+1))-2*D; if(b<0||b>=n) continue; }
                if(a==b) continue;
                int nx[512], no[512]; memcpy(nx,cur,sizeof(int)*n); memcpy(no,org,sizeof(int)*n);
                int m=(int)(rnd()*3);
                if(m==0){int x=nx[a];nx[a]=nx[b];nx[b]=x; x=no[a];no[a]=no[b];no[b]=x;}
                else if(m==1){ if(a>b){int x=a;a=b;b=x;} while(a<b){int x=nx[a];nx[a]=nx[b];nx[b]=x; x=no[a];no[a]=no[b];no[b]=x;a++;b--;} }
                else { int x=nx[a], y=no[a]; if(a<b){memmove(nx+a,nx+a+1,sizeof(int)*(b-a)); nx[b]=x; memmove(no+a,no+a+1,sizeof(int)*(b-a)); no[b]=y;} else {memmove(nx+b+1,nx+b,sizeof(int)*(a-b)); nx[b]=x; memmove(no+b+1,no+b,sizeof(int)*(a-b)); no[b]=y;} }
                if(D){int bad=0; for(int i=0;i<n;i++) if(abs(no[i]-i)>D){bad=1;break;} if(bad) continue;}
                double ns=score(nx,n);
                if(ns>=cs || rnd()<exp((ns-cs)/T)){ memcpy(cur,nx,sizeof(int)*n); memcpy(org,no,sizeof(int)*n); cs=ns; }
            }
            if(cs>bs){bs=cs; memcpy(best,cur,sizeof(int)*n);}
        }
        printf("%.4f ",bs/(n-3)); for(int i=0;i<n;i++) putchar('a'+best[i]); putchar('\n'); fflush(stdout);
    }
    return 0;
}
