import os, sys, subprocess, numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *
AN=os.environ.get('K19_CHUNKANA','./chunkana')
Q=os.path.join(ROOT,'data/models/qg_de.bin')
stream=sys.argv[1]; tag=sys.argv[2]; sizes=list(range(int(sys.argv[3]),int(sys.argv[4])+1,int(sys.argv[5])))
n=len(open(stream).read().strip())
def bounds(c,a):
    b=([a] if a else [])+[c]*((n-a)//c); r=n-sum(b)
    if r: b.append(r)
    return b
res={}
for c in sizes:
    row=[]
    for a in range(c):
        fn=f'tmp_b_{tag}.txt'; open(fn,'w').write(' '.join(map(str,bounds(c,a))))
        out=subprocess.run([AN,Q,stream,fn,'3','2000000',str(c*100+a)],capture_output=True,text=True).stdout
        row.append(float(out.split()[0]))
    row=np.array(row); res[c]=row
    print(f'c={c:2d} max {row.max():.4f} at a={row.argmax():2d} | mean {row.mean():.4f} sd {row.std():.4f} | peak z {(row.max()-row.mean())/row.std():+.2f}',flush=True)
