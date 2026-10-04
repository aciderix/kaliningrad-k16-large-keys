import os, sys, subprocess, numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *
from concurrent.futures import ThreadPoolExecutor
AN=os.environ.get('K19_CHUNKANA','./chunkana')
Q=os.path.join(ROOT,'data/models/qg_de.bin')
L=lines_v1()
if not os.path.exists('bottle_stream.txt'): open('bottle_stream.txt','w').write(''.join(''.join(tokens(l,'plain')) for l in L[:-1])+'\n')
sizes=[len(''.join(tokens(l,'plain'))) for l in L[:-1]]; n=sum(sizes)
def score(bounds,seed):
    fn=f'tmp_lc_{seed}.txt'; open(fn,'w').write(' '.join(map(str,bounds)))
    out=subprocess.run([AN,Q,'bottle_stream.txt',fn,'4','3000000',str(seed)],capture_output=True,text=True).stdout
    return float(out.split()[0])
def shifted(b,s):
    # rotate chunk boundaries by s positions (cyclic), keeping the same chunk lengths
    cuts=np.cumsum([0]+b)[:-1]; cuts=sorted(((cuts+s)%n).tolist()); 
    if cuts[0]!=0: cuts=[0]+cuts
    return [y-x for x,y in zip(cuts,cuts[1:]+[n])]
half=[]
for z in sizes: half+= [z//2, z-z//2]
rng=np.random.default_rng(6)
for name,b in [('lines',sizes),('half-lines',half)]:
    real=score(b,1)
    shifts=rng.integers(3,40,24)
    with ThreadPoolExecutor(4) as ex: nul=list(ex.map(lambda s: score(shifted(b,int(s)),int(s)+100), shifts))
    nul=np.array(nul)
    print(f'{name:10s}: score {real:.4f} | shifted chunkings {nul.mean():.4f}±{nul.std():.4f} (max {nul.max():.4f}) z={(real-nul.mean())/nul.std():+.2f}',flush=True)
