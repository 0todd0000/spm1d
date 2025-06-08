
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import spm1d.stats.nonparam_old



# load data:
dataset      = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
# dataset      = spm1d.data.uv1d.anova1.Weather()
y,A          = dataset.get_data()



# conduct tests:
np.random.seed(0)
alpha      = 0.05
niter      = 1000
spmi       = spm1d.stats.anova1(y, A, equal_var=True).inference(alpha)
snpmi      = spm1d.stats.nonparam.anova1(y, A).inference(alpha, iterations=niter)
snpmio     = spm1d.stats.nonparam_old.anova1(y, A).inference(alpha, iterations=niter)
print( 'Critical thresholds:')
print( f'   Parametric:           {spmi.zstar:.5f}')
print( f'   Nonparametric:        {snpmi.zstar:.5f}')
print( f'   Nonparametric (old):  {snpmio.zstar:.5f}')



# plot:
plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(8,3), tight_layout=True)
u       = np.unique(A)
nu      = u.size
colors  = plt.cm.jet( np.linspace(0,1,nu) )
for uu,cc in zip(u,colors):
    yy  = y[A==uu]
    axs[0].plot(yy.T, color=cc, lw=0.5)
ax = axs[1]
spmi.plot(ax=ax)
ax.plot( snpmi.z, 'c' )
ax.axhline(snpmi.zstar, color='c', linestyle='--', label='SnPM')
ax.axhline(snpmio.zstar, color='r', linestyle='--', label='SnPM (old)')
ax.legend()
plt.show()


