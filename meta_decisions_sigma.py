from decisions import prob_matrixer
from decisions import dyn_prog
import numpy as np
from tqdm import tqdm
import pandas as pd

prob_matrixes = prob_matrixer()
a = dyn_prog(0,0,prob_matrixes)[0]

M = [4,8,12,16]
V = np.linspace(.001,.999,50)
P = [10**-4,.001,.003,.01,.1]
Results = pd.DataFrame(index = np.arange(len(P)*len(V)*len(a)*len(M)),columns=("v","p","resources","action","sigma"))
for k in range(len(M)):
    prob_matrixes = prob_matrixer()
    for j in range(len(P)):
        for i in tqdm(range(len(V))):
            fitness, exp,decisions = dyn_prog(p=P[j],v=V[i],prob_matrixes=prob_matrixes,σ = M[k])
            slice_b = int(k*len(Results.index)/len(M) + (len(V)*j + i)*len(a))
            slice_e = int(k*len(Results.index)/len(M) + (len(V)*j + i+1)*len(a))
            Results.v[slice_b:slice_e] = V[i]
            Results.p[slice_b:slice_e] = P[j]
            Results.resources[slice_b:slice_e] = np.linspace(-50,50,1001)
            Results.action[slice_b:slice_e] = decisions
            Results.sigma[slice_b:slice_e] = M[k]

np.save("Results/decisions_f.npy",Results)
