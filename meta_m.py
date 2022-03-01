import os
import numpy as np
import pickle
import subprocess

PARAM = np.linspace(10,20,100)
M = [10**-3,10**-2,.05,.1,.2]
for i in PARAM:
	for m in M:
		bash = "srun -N 1 -o logs.out --partition=firstgen,dellgen python3 /home/bdecourson/model/try_m.py "+str(i) +" "+ str(m)
		subprocess.Popen(bash.split(),stdout=subprocess.PIPE)	
