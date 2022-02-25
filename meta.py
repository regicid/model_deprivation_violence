import os
import numpy as np
import pickle
import subprocess

PARAM = np.linspace(10,20,100)

for i in PARAM:
	bash = "srun -N 1 -o logs.out --partition=dellgen python3 /home/bdecourson/model/try.py "+str(i)
	subprocess.Popen(bash.split(),stdout=subprocess.PIPE)	
