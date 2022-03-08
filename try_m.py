import sys
mu = float(sys.argv[1])
M = [.001,.01,.05,.2]
from model import Population
import pickle
import numpy as np
for m in M:
	P = Population(mu,m=m,initial_v=0,update_rate=.1,σ=4,r=.99,n=50,π = 10,β=5)
	P.round(100)
	np.save(f"Results/result2_{np.round(mu,2)}_m={m}_v=0.npy",P.frequencies)
	P = Population(mu,m=m,initial_v=1,update_rate=.1,σ=4,r=.99,n=50,π = 10,β=5)
	P.round(100)
	np.save(f"Results/result2_{np.round(mu,2)}_m={m}_v=1.npy",P.frequencies)
