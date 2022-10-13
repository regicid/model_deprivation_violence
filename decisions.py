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
    






def dyn_prog(p,v,prob_matrixes,T = 200,n=10,γ=1/3,m=.01,λ=.05,ω=.1,β=10,π=20,state_space = np.round(np.linspace(-50,50,1001),1)):
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
            exp_fitness[strat,:] = np.dot(outcomes[strat],fitness*(1-ω*(state_space<0))*(1 - prob_fight[strat]*λ/2))
        decisions = np.argmax(exp_fitness,axis=0)
        fitness = np.max(exp_fitness,axis=0)
    return fitness, exp_fitness, decisions

import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
def panel_plot(name,column,col_min = None,col_max = None):
    def cmap_discretize(cmap, N):
        #Return a discrete colormap from the continuous colormap cmap.
        if type(cmap) == str:
            cmap = plt.get_cmap(cmap)
        colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
        colors_rgba = cmap(colors_i)
        indices = np.linspace(0, 1., N+1)
        cdict = {}
        for ki,key in enumerate(('red','green','blue')):
            cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in range(N+1) ]
        # Return colormap object.
        return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)

    cmap = sns.cubehelix_palette(n_colors=3,start=0, rot=.8, light=0.9, as_cmap=True)
    cmap = cmap_discretize(plt.cm.get_cmap('jet', 3),3)

    Results = np.load("/Users/benoit2c/model/Results/"+name,allow_pickle=True)
    Results = pd.DataFrame(Results).loc[::-1]
    Results.set_axis(["Violence","Stealing","Resources","Actions",column],axis=1,inplace=True)
    if col_min is not None:
        Results = Results.loc[Results.loc[:,column]>=col_min,:]
    if col_max is not None:
        Results = Results.loc[Results.loc[:,column]<=col_max,:]
    Results.Actions= Results.Actions.astype("int8")
    Results.Violence= Results.Violence.astype("float")
    Results.Violence = Results.Violence.round(2)
    Results.Resources= Results.Resources.astype("float")

    def draw_heatmap(*args, **kwargs):
        data = kwargs.pop('data')
        d = data.pivot(index=args[1], columns=args[0], values=args[2])
        sns.heatmap(d, **kwargs)

    sns.set_theme(font_scale=1.3,style="ticks")
    if len(Results.loc[:,column].unique())==1:
        fg = sns.FacetGrid(Results,col="Stealing",sharex=True,sharey=False,margin_titles=True,aspect=1.7,despine=True,legend_out=True)
    else:
        fg = sns.FacetGrid(Results,row="Stealing",col=column,sharex=True,sharey=False,margin_titles=True,aspect=1.7,despine=True,legend_out=True)
    cbar_ax = fg.fig.add_axes([1.02, .15, .03, .7])

    fg.map_dataframe(draw_heatmap,"Resources","Violence","Actions",cmap=cmap,xticklabels=500,yticklabels=49,cbar_ax=cbar_ax, cbar_kws={'ticks':[0.33,1,1.75]},vmin=0,vmax=2)
    fg.set_xticklabels(["","",""])
    
    for ax in fg.axes.ravel():
        ax.invert_yaxis()

    cbar_ax.set_yticklabels(['Submissive','Violent',"Stealing"],size=25)
    cbar_ax.set_ylabel(ylabel="Actions",size=25)
    cbar_ax.set_ylim((0,2))

    fg.set_titles(size=22,fontweight='bold')
    plt.tight_layout()
    fg.savefig(f"/Users/benoit2c/Downloads/{name}_decisions.jpg",dpi=300)
