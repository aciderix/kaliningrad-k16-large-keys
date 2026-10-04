"""K22 — décodeur mot à mot sous contrainte de déplacement.
Le clair est une suite de mots du dictionnaire ; la lettre n° i du clair doit être prise à une position j du flux
avec |j-i| <= D, chaque position une seule fois (on prend toujours l'occurrence libre la plus à gauche, ce qui ne perd
aucune solution). Score : bigrammes de mots interpolés. Faisceau synchronisé sur le nombre de lettres produites."""
import pickle, math, bisect, sys, time
A='abcdefghijklmnopqrstuvwxyz'
class Decoder:
    def __init__(self,lm='lm.pkl',minc=5,maxlen=16,lam=0.7,nullpen=None,nullset='fwn'):
        vocab,bi,ntok=pickle.load(open(lm,'rb'))
        self.vocab={w:c for w,c in vocab.items() if c>=minc and len(w)<=maxlen and (len(w)>1 or w in ('a','i','o'))}
        self.bi=bi; self.ntok=ntok; self.lam=lam
        self.trie={}
        for w in self.vocab:
            node=self.trie
            for ch in w: node=node.setdefault(ch,{})
            node['$']=w
        self.nullpen=nullpen; self.nullset=nullset
    def wscore(self,prev,w):
        pu=self.vocab[w]/self.ntok
        if prev is not None:
            c=self.bi.get((prev,w),0); cp=self.vocab.get(prev,1)
            return math.log(self.lam*c/cp+(1-self.lam)*pu)
        return math.log(pu)
    def setup(self,cipher,D):
        self.C=cipher; self.N=len(cipher); self.D=D
        self.pos={a:[j for j,c in enumerate(cipher) if c==a] for a in A}
    def place(self,ch,i,used):
        lo=max(0,i-self.D); hi=min(self.N-1,i+self.D); P=self.pos.get(ch,[])
        k=bisect.bisect_left(P,lo)
        while k<len(P) and P[k]<=hi:
            j=P[k]
            if not (used>>j)&1: return j
            k+=1
        return -1
    def ok_strand(self,used,i):
        lim=i-self.D
        if lim<=0: return True
        free=~used & (used+1); low=free.bit_length()-1
        return low>=lim
    def expand(self,i,used):
        out=[]
        stack=[(self.trie,i,used,'')]
        while stack:
            node,ii,uu,pre=stack.pop()
            if '$' in node and self.ok_strand(uu,ii): out.append((node['$'],ii,uu))
            if ii>=self.N: continue
            for ch,child in node.items():
                if ch=='$': continue
                j=self.place(ch,ii,uu)
                if j>=0: stack.append((child,ii+1,uu|(1<<j),pre+ch))
        return out
    def decode(self,cipher,D,beam=200,verbose=False):
        self.setup(cipher,D); N=self.N
        bins=[dict() for _ in range(N+1)]
        bins[0][(0,None)]=(0.0,())
        t0=time.time()
        for i in range(N):
            if not bins[i]: continue
            hyps=sorted(bins[i].items(),key=lambda kv:-kv[1][0])[:beam]
            bins[i]=None
            for (used,prev),(sc,words) in hyps:
                for w,ni,nu in self.expand(i,used):
                    s=sc+self.wscore(prev,w); key=(nu,w)
                    b=bins[ni]
                    if key not in b or b[key][0]<s: b[key]=(s,words+(w,))
                if self.nullpen is not None:
                    for ch in self.nullset:
                        j=self.place(ch,i,used)
                        if j>=0:
                            nu=used|(1<<j)
                            if self.ok_strand(nu,i+1):
                                s=sc+self.nullpen; key=(nu,prev); b=bins[i+1]
                                if key not in b or b[key][0]<s: b[key]=(s,words+('['+ch+']',))
            if verbose and i%50==0:
                best=max(bins[i+1].values(),key=lambda v:v[0]) if bins[i+1] else None
                print(f'  i={i} t={time.time()-t0:.0f}s', ' '.join(best[1][-8:]) if best else '',flush=True)
        if not bins[N]: return None
        return max(bins[N].values(),key=lambda v:v[0])
