import os
import numpy as np
import pickle
import subprocess

os.system("mkdir Results")
PARAM = np.linspace(10,20,15)

for i in PARAM:
	bash = "srun -N 1 -o logs.out --partition=secondgen python3 try.py "+str(i)
	subprocess.Popen(bash.split(),stdout=subprocess.PIPE)	
