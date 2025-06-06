
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import spm1d.stats.nonparam_old


# load data
dataset    = spm1d.data.uv1d.regress.SimulatedPataky2015c()
dataset    = spm1d.data.uv1d.regress.SpeedGRF()
y,x        = dataset.get_data()
# reduce sample size to check differences between new and old nonparam inference
n          = 7
y,x        = y[:n], x[:n]



# conduct inference:
two_tailed = True
niter      = 1000
alpha      = 0.05
spmi       = spm1d.stats.regress(y, x).inference(alpha, two_tailed=two_tailed)
snpmi      = spm1d.stats.nonparam.regress(y, x).inference(alpha, iterations=niter, two_tailed=two_tailed)
snpmio     = spm1d.stats.nonparam_old.regress(y, x).inference(alpha, iterations=niter, two_tailed=two_tailed)
print( 'Critical thresholds:')
print( f'   Parametric:           {spmi.zstar:.5f}')
print( f'   Nonparametric:        {snpmi.zstar:.5f}')
print( f'   Nonparametric (old):  {snpmio.zstar:.5f}')



# plot:
plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(8,3), tight_layout=True)
axs[0].plot(y.T, 'k', lw=0.5)
ax = axs[1]
spmi.plot(ax=ax)
ax.plot( snpmi.z, 'c' )
ax.axhline(snpmi.zstar, color='c', linestyle='--', label='SnPM')
ax.axhline(snpmio.zstar, color='r', linestyle='--', label='SnPM (old)')
ax.legend()
plt.show()





