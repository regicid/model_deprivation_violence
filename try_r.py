import sys
mu = float(sys.argv[1])
R = [.8,.9,.97,.99,.995]
from model import Population
import pickle
import numpy as np
for r in R:
	for initial_v in [0,1]:
		P = Population(mu,r=r,initial_v=initial_v,n=50,σ=6,update_rate = .01)
		P.round(1000)
		np.save(f"Results/result3_{np.round(mu,2)}_r={r}_v={initial_v}.npy",P.frequencies)
