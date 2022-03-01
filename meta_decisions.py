from decisions import prob_matrixer
from decisions import dyn_prog
import numpy as np
from tqdm import tqdm
import pandas as pd

prob_matrixes = prob_matrixer()
a = dyn_prog(0,0,prob_matrixes)[0]


V = np.linspace(.001,.999,50)
P = [10**-4,.001,.003,.01,.1]
Results = pd.DataFrame(index = np.arange(len(P)*len(V)*len(a)),columns=("v","p","resources","action"))

for j in range(len(P)):
    for i in tqdm(range(len(V))):
        fitness, exp,decisions = dyn_prog(p=P[j],v=V[i],prob_matrixes=prob_matrixes)
        Results.v[(len(V)*j + i)*len(a):(len(V)*j + i+1)*len(a)] = V[i]
        Results.p[(len(V)*j + i)*len(a):(len(V)*j + i+1)*len(a)] = P[j]
        Results.resources[(len(V)*j + i)*len(a):(len(V)*j + i+1)*len(a)] = np.linspace(-50,50,1001)
        Results.action[(len(V)*j + i)*len(a):(len(V)*j + i+1)*len(a)] = decisions

np.save("Results/results.npy",Results)
