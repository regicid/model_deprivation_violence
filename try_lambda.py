import sys
mu = float(sys.argv[1])
LAMBDA = [.01,.05,.1,.3]
from model import Population
import pickle
import numpy as np
for f2 in LAMBDA:
	for initial_v in [0,1]:
		P = Population(mu,f2=f2,initial_v=0,n=50,σ=6,update_rate = .1)
		P.round(100)
		np.save(f"Results/result2_{np.round(mu,2)}_lambda={f2}_v={initial_v}.npy",P.frequencies)
