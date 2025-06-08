
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import spm1d.stats.nonparam_old


# load data
dataset    = spm1d.data.uv1d.t2.PlantarArchAngle()
y0,y1        = dataset.get_data()
# # OR create a random dataset:
# np.random.seed(2)
# n  = 10
# y0 = np.random.randn(n,101)
# y1 = np.random.randn(n,101) + 2*np.sin( np.linspace(0,10,101) )
# y0 = spm1d.util.smooth(y0, 8)
# y1 = spm1d.util.smooth(y1, 8)



# conduct inference:
two_tailed = True
niter      = -1
alpha      = 0.05
spmi       = spm1d.stats.ttest_paired(y1, y0).inference(alpha, two_tailed=two_tailed)
snpmi      = spm1d.stats.nonparam.ttest_paired(y1, y0).inference(alpha, iterations=niter, two_tailed=two_tailed)
snpmio     = spm1d.stats.nonparam_old.ttest_paired(y1, y0).inference(alpha, iterations=niter, two_tailed=two_tailed)
print( 'Critical thresholds:')
print( f'   Parametric:           {spmi.zstar:.5f}')
print( f'   Nonparametric:        {snpmi.zstar:.5f}')
print( f'   Nonparametric (old):  {snpmio.zstar:.5f}')



# plot:
plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(8,3), tight_layout=True)
axs[0].plot(y0.T, 'k', lw=0.5)
axs[0].plot(y1.T, 'c', lw=0.5)
ax = axs[1]
spmi.plot(ax=ax)
ax.plot( snpmi.z, 'c' )
ax.axhline(snpmi.zstar, color='c', linestyle='--', label='SnPM')
ax.axhline(snpmio.zstar, color='r', linestyle='--', label='SnPM (old)')
ax.legend()
plt.show()





