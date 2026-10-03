import sys, math, time
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from wdecode import Decoder
from common import *
L=lines_v1(); s=''.join(''.join(tokens(l,'plain')) for l in L[:-1])
a,b,D,beam=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
seg=s[a:b]
dec=Decoder(nullpen=math.log(0.02))
t=time.time(); res=dec.decode(seg,D,beam=beam)
print(f'segment {a}-{b} D={D} beam={beam} t={time.time()-t:.0f}s')
print(' '.join(res[1]) if res else 'aucune solution')
