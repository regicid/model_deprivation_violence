import sys
mu = float(sys.argv[1])
from model import Population
import pickle
import numpy as np
P = Population(mu)
P.round(10)
np.save(f"result_{mu}.npy",P.frequencies)
