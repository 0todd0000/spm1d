
import numpy as np
from matplotlib import pyplot
import rft1d
import spm1d





#(0) Load dataset:
# dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()



#(1) Compute confidence interval:
alpha      = 0.05
J,Q        = y.shape
df         = J - 1
### compute residuals:
m,s        = y.mean(axis=0), y.std(axis=0, ddof=1)
residuals  = y - m
### compute critical t statistic
fwhm       = rft1d.geom.estimate_fwhm(residuals)
resels     = rft1d.geom.resel_counts(residuals, fwhm, element_based=False)
zstar      = rft1d.t.isf_resels(0.5*alpha, df, resels)
### compute confidence interval height:
hstar      = zstar * s / J**0.5



#(2) Plot:
pyplot.close('all')
pyplot.figure(figsize=(6,4))
pyplot.get_current_fig_manager().window.move(0, 0)
ax     = pyplot.axes()
### plot mean:
h0     = ax.plot(m, color='k', lw=3)[0]
h10    = ax.plot(m+hstar, 'g')[0]
h11    = ax.plot(m-hstar, 'g')[0]
h20    = ax.plot(m+s, 'r')[0]
h21    = ax.plot(m-s, 'r')[0]
pyplot.legend([h0,h10,h20], ['Mean', '95%s CI'%'%', 'SD'], loc='upper left')
pyplot.show()