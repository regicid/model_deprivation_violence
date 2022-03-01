import sys
mu = float(sys.argv[1])
#m = float(sys.argv[2])
M = [10**-3,10**-2,.05,.1,.2]
from model import Population
import pickle
import numpy as np
for m in M:
	P = Population(mu,m=m,initial_v=0,update_rate=.1,σ=4,n=20,r=.85)
	P.round(50)
	np.save(f"Results/result_{np.round(mu,2)}_m={m}_v=0.npy",P.frequencies)
	P = Population(mu,m=m,initial_v=1,update_rate=.1,σ=4,n=20)
	P.round(50)
	np.save(f"Results/result_{np.round(mu,2)}_m={m}_v=1.npy",P.frequencies)
