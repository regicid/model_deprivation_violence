import os
import numpy as np
import pickle
import subprocess
import time
PARAM = np.linspace(5,14,20)
M = [10**-2,.05]
for i in PARAM:
	bash = "srun -N 1 -o logs.out --partition=firstgen,dellgen python3 /home/bdecourson/model/try_m.py " + str(i)
	subprocess.Popen(bash.split(),stdout=subprocess.PIPE)	
