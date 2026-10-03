from periodic import *
L=lines_v1(); s=[]
for line in L[:-1]:
    for w in line.split(): s+=tokens(w,'plain')
x=enc(''.join(s)); rng=np.random.default_rng(5)
def sc(y,d): return P[y[:-d],y[d:]].mean()
nul=np.array([[sc(rng.permutation(x),d) for d in range(1,21)] for _ in range(3000)])
obs=np.array([sc(x,d) for d in range(1,21)])
z=(obs-nul.mean(0))/nul.std(0)
for d in range(20): print(f"d={d+1:2d} obs={obs[d]:+.4f} null={nul.mean(0)[d]:+.4f}±{nul.std(0)[d]:.4f} z={z[d]:+.2f} p_high={(nul[:,d]>=obs[d]).mean():.4f}")
# reversed direction score (reading backwards)
xr=x[::-1]; print('reversed d=1 z=%.2f'%((sc(xr,1)-nul.mean(0)[0])/nul.std(0)[0]))
