from decisions import prob_matrixer
from decisions import dyn_prog
import numpy as np
from tqdm import tqdm
import pandas as pd

prob_matrixes = prob_matrixer()
a = dyn_prog(0,0,prob_matrixes)[0]

M = [10**-3,10**-2,.05,.2]
V = np.linspace(.001,.999,50)
P = [10**-4,.001,.003,.01,.1]
Results = pd.DataFrame(index = np.arange(len(P)*len(V)*len(a)*len(M)),columns=("v","p","resources","action","m"))
for k in range(len(M)):
    for j in range(len(P)):
        for i in tqdm(range(len(V))):
            fitness, exp,decisions = dyn_prog(p=P[j],v=V[i],prob_matrixes=prob_matrixes,m = M[k])
            slice=k*len(Results.index)/len(M)+(len(V)*j + i)*len(a):(len(V)*j + i+1)*len(a)
            Results.v[slice] = V[i]
            Results.p[slice] = P[j]
            Results.resources[slice] = np.linspace(-50,50,1001)
            Results.action[slice] = decisions

np.save("Results/results.npy",Results)
