import sys
mu = float(sys.argv[1])
sigma = float(sys.argv[2])
N = [5,20,50,100,200,300,400,500]
N = [2000]
from model import Population
import pickle
import numpy as np
for n in N:
	for initial_v in [0,1]:
		P = Population(mu,initial_v=initial_v,update_rate=.01,σ=sigma,r=.9,n=n)
		P.round(1000)
		np.save(f"Results/result_low_r_{np.round(mu,2)}_n={n}_v={initial_v}.npy",P.frequencies)
