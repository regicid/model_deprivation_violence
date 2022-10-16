# Code of  "Why is violence high and persistent in deprived communities? A formal model"

This repository contains the code needed to run the model, to generate the results presented in the paper and to reproduce the figures. 

If you are here to play a bit with the model, you should rather have a look at the [model explorer](https://colab.research.google.com/drive/1wf3KBd95YO_WTluGztaR-8l-1zOD-e0o?usp=sharing), a colab notebook that one can run directly online from a browser, without installing anything.

The results presented in the paper would take (I presume) days on a standard laptop, so we used a computer cluster. The `meta.py` and `meta_sigma.py`script paralellizes simulations. It is designed to run on Linux and requires the utility `slurm`, but can easily adapted to other configurations. If you want to run it sequentially, you can use the script meta_sequential instead. 

These script runs simulations for different values of the desperation range by calling the `try_*.py`scripts (. It is designed to be used in command line with, as arguments, the script launching the simulation and desired minimum and maximum desperation rates. Between the simulations, the scripts will vary $\mu$ (for `meta.py`) or $\sigma$ (for `meta_sigma.py`) so that the populations' desperation rates are evenly spaced from the minimum to the maximum, like in Fig. 3 of the paper. 

The name of the `try_*.py` script indicates which parameter vary. In `try_sigma.py` (to use with `meta_sigma.py`, only $\sigma$ varies, to produce the Figure 3. The other ones are used to produce the sensitivity analysis presented in the Supplementary Materials. For instance, `python3 meta.py try_n.py .00005 .03` will vary both the desperation rate (through $\mu$) and $n$ (the lists of $n$ values being defined in `try_n.py`.

The simulations are pre-run and stored in the folder Results/. In the jupyter notebooks `Figures.ipynb`and `Supplementary_materials_figure.ipynb`, the results are imported from the Results/ folder.
