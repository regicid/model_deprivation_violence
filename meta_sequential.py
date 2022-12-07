import os
import numpy as np
import pickle
import subprocess
import time
import sys
from tqdm import tqdm
from scipy.stats import norm
script = sys.argv[1]
min_ = float(sys.argv[2])
max_ = float(sys.argv[3])
sigma = float(sys.argv[4])

def desp_rate(mu=15,sigma=sigma):
    return norm.cdf(0,loc=mu,scale=sigma)
MU = np.linspace(8,30,10000)
desp_rates = [desp_rate(mu=mu) for mu in MU]
PARAM = [MU[np.argmin(np.abs(x-desp_rates))] for x in np.linspace(min_,max_,50)]
#PARAM = PARAM[-17:]
for i in tqdm(PARAM):
	bash = "python3 " + script + " " + str(i) + " " + str(sigma)
	os.system(bash)
