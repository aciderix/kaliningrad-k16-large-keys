import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
import glob
rng=np.random.default_rng(3)
Ps=P+P.T
def band(y,a=1,b=10): return np.mean([Ps[y[:-d],y[d:]].mean() for d in range(a,b+1)])
def zb(y,nn=800):
    o=band(y); nb=np.array([band(rng.permutation(y)) for _ in range(nn)]); return (o-nb.mean())/nb.std()
for f in sorted(glob.glob(sys.argv[1] if len(sys.argv)>1 else 'wc_*.txt')):
    y=enc(open(f).read().strip()); print(f'{f:22s} band z(d1-10) = {zb(y):+.2f}',flush=True)
