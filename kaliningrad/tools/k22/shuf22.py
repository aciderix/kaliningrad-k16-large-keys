import sys, math, random
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from wdecode import Decoder
from common import *
L=lines_v1(); s=''.join(''.join(tokens(l,'plain')) for l in L[:-1])
seg=list(s[0:166]); random.Random(int(sys.argv[1])).shuffle(seg)
res=Decoder(nullpen=math.log(0.02)).decode(''.join(seg),50,beam=30)
print('mélange',sys.argv[1],':',' '.join(res[1]) if res else None)
