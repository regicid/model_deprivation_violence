import numpy as np

def prob_matrixer(μ =10,r=.99,σ=4,β=10,π=20,state_space = np.round(np.linspace(-50,50,1001),1)):
    def norm_distrib(x,loc,scale=np.sqrt(1-r**2)*σ):
        x = np.array(x)
        loc = np.array(loc)
        x = np.tile(x,(loc.size,1))
        loc = np.tile(loc,(loc.size,1))
        z = (scale/np.sqrt(2*np.pi))*np.exp(-(x-loc.T)**2/(2*scale**2))
        return z/z.sum(1,keepdims=1)

    def probas(modif):
        z = (norm_distrib(x = state_space,loc = r*state_space + (1-r)*μ + modif,scale = np.sqrt(1-r**2)*σ))
        return(z)
    return np.array([probas(0),probas(-β),probas(β),probas(-π)])
    






def dyn_prog(p,v,prob_matrixes,T = 200,n=10,r=.99,γ=1/3,m=.01,f2=.05,ω=.1,β=10,π=20,state_space = np.round(np.linspace(-50,50,1001),1)):
    p = (1-(1-p)**n)/n
    if v==1: v=.999
    fitness = (100+state_space)/2
    decisions = [0,0]
    #Strategy order: submissive, discriminate violent, indiscriminate violent, steal
    prob_stolen= [np.clip(p*(1-v**n)/(1-v),0,1),np.clip(p*v**(n-1),0,1)]
    prob_success = (1-v**n/2)
    outcomes = [] #Two levels: strategy, outcome
    prob_fight = [0,prob_stolen[1]+(1-prob_stolen[1])*m*v,v**n + (1-v**n)*(prob_stolen[1]+(1-prob_stolen[1])*m*v)]
    outcomes.append(np.einsum('ijk,i->jk',prob_matrixes,np.array([1-prob_stolen[0],prob_stolen[0],0,0])))
    outcomes.append(np.einsum('ijk,i->jk',prob_matrixes,[1-prob_stolen[1]/2,prob_stolen[1]/2,0,0]))
    outcomes.append(np.einsum('ijk,i->jk',prob_matrixes,[(1-γ)*prob_success*prob_stolen[1]/2,(1-γ)*(1-prob_success)*prob_stolen[1]/2,(1-γ)*prob_success*(1-prob_stolen[1]/2),γ]))
    for i in range(T):
        temp_fitness = []
        exp_fitness = np.empty(shape=(3,len(state_space)),dtype = "float")
        for strat in range(3):
            exp_fitness[strat,:] = np.dot(outcomes[strat],fitness*(1-ω*(state_space<0))*(1 - prob_fight[strat]*f2/2))
        decisions = np.argmax(exp_fitness,axis=0)
        fitness = np.max(exp_fitness,axis=0)
    return fitness, exp_fitness, decisions
