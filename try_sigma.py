import sys
mu = 15
sigma = float(sys.argv[1])
N = [50]
m = .2
from model import Population
import pickle
import numpy as np
for n in N:
	for initial_v in [0,1]:
		P = Population(mu,σ=sigma,λ=.1,m=m,β=5,π=10,initial_v=initial_v,update_rate=.1,r=.99,n=n)
		P.round(200)
		np.save(f"Results/result4_sigma={np.round(sigma,2)}_n={n}_v={initial_v}.npy",P.frequencies)
