import sys, time, numpy as np
from kl import structure, F
k=int(sys.argv[1]); lam=float(sys.argv[2]); src=sys.argv[3]; tlimit=float(sys.argv[4])
S=structure(k)
c=np.load(src)
if c.size*3==S["N"]: c=np.tile(c,3)          # lift solution from k-1 to k
t=time.time(); it=0
while time.time()-t<tlimit:
    Fc=F(c,lam,S); r=Fc/c; c=Fc/Fc.min(); it+=1
print(f"k={k} lam={lam} iters={it} min ratio={r.min():.10f} max ratio={r.max():.10f}")
np.save(f"c_k{k}_work.npy",c)
