
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
# dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()



#(1) Compute confidence interval:
### get critical t statistic
alpha      = 0.05
spmi       = spm1d.stats.ttest(y, mu).inference(alpha, two_tailed=True)
zstar      = spmi.zstar
### compute confidence interval height:
J          = y.shape[0]              #number of observations
m          = y.mean(axis=0)          #mean continuum
sd         = y.std(axis=0, ddof=1)   #standard deviation continuum
hstar      = zstar * sd / J**0.5      #confidence interval height continuum



#(2) Plot:
pyplot.close('all')
pyplot.figure(figsize=(6,4))
pyplot.get_current_fig_manager().window.move(0, 0)
ax     = pyplot.axes()
### plot mean:
ax.plot(m, color='k', lw=3)
### plot confidence interval:
spm1d.plot.plot_errorcloud(m, hstar,   ax=ax, facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True)
### compare to standard deviation:
spm1d.plot.plot_errorcloud(m, sd, ax=ax, facecolor='r', edgecolor='r', alpha=0.5, autoset_ylim=True)
pyplot.show()