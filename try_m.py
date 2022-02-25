import sys
mu = float(sys.argv[1])
m = float(sys.argv[2])
from model import Population
import pickle
import numpy as np
P = Population(mu,N=10**4,m=m,initial_v=0,update_rate=.1,σ=6,n=20)
P.round(500)
np.save(f"result2_{np.round(mu,2)}_m={m}_v=0.npy",P.frequencies)
P = Population(mu,m=m,initial_v=1,update_rate=.1,σ=6,n=20)
P.round(50)
np.save(f"result2_{np.round(mu,2)}_m={m}_v=1.npy",P.frequencies)
