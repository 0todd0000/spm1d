
import numpy as np
import matplotlib.pyplot as plt
import spm1d
from spm1d import rft1d





#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()



#(1) Compute confidence interval:
alpha      = 0.05                   #Type I error rate
J          = y.shape[0]             #sample size
df         = J - 1                  #degrees of freedom
m          = y.mean(axis=0)         #sample mean
s          = y.std(axis=0, ddof=1)  #sample standard deviation
residuals  = y - m                  #model residuals
fwhm       = rft1d.geom.estimate_fwhm(residuals)    #1D field smoothness
resels     = rft1d.geom.resel_counts(residuals, fwhm, element_based=False)   #resloution element counts
zstar      = rft1d.t.isf_resels(0.5*alpha, df, resels)    #critical test statistic value (using Random Field Theory)
hstar      = zstar * s / J**0.5     #confidence interval height
ci         = m - hstar, m + hstar   #confidence interval



#(2) Compare to spm1d result:
ci_spm1d   = spm1d.stats.ci_onesample(y, alpha, mu)



#(3) Plot the CIs:
plt.close('all')
plt.figure(figsize=(10,4))

### plot parametric CI:
ax = plt.subplot(121)
ax.plot(m, color='b', lw=3)
ax.plot(ci[0], color='b', lw=1, linestyle=':')
ax.plot(ci[1], color='b', lw=1, linestyle=':')
ax.axhline(0, color='k', linestyle='--')
ax.set_title('Manually computed CI', size=10)
ax.set_ylim(-7, 13)
### plot parametric CI:
ax = plt.subplot(122)
ci_spm1d.plot(ax)
ax.set_title('spm1d result', size=10)
plt.suptitle('One-sample CIs')
ax.set_ylim(-7, 13)
plt.show()