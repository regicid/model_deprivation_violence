import sys
mu = float(sys.argv[1])
GAMMA = [1/3,.5,.6,.8]
from model import Population
import pickle
import numpy as np
for γ in GAMMA:
	for initial_v in [0,1]:
		P = Population(mu,γ=γ,initial_v=initial_v,n=50,σ=6,update_rate = .1)
		P.round(100)
		np.save(f"Results/result2_{np.round(mu,2)}_gamma={γ}_v={initial_v}.npy",P.frequencies)
