


'''
Compare two-tailed, two-sample t-test to one-way ANOVA

The tests should be identical, with F = t**2
'''

import numpy as np
import matplotlib.pyplot as plt
import spm1d



# load data:
dataset    = spm1d.data.uv1d.t2.PlantarArchAngle()
y0,y1      = dataset.get_data()


# prepare data for ANOVA:
y          = np.vstack([y0,y1])
A          = np.hstack( [0]*y0.shape[0] + [1]*y1.shape[0] )
S          = np.hstack( [np.arange(y0.shape[0]), np.arange(y1.shape[0])] )



# conduct tests:
alpha      = 0.05
two_tailed = True
niter      = 1000
np.random.seed(0)
ti         = spm1d.stats.nonparam.ttest_paired(y1, y0).inference(alpha, two_tailed=two_tailed, iterations=niter)
np.random.seed(0)
fi         = spm1d.stats.nonparam.anova1rm(y, A, S).inference(alpha, iterations=niter)
print( 'Critical thresholds:')
print( f'   ttest_paired (squared):  {ti.zstar**2:.5f}')
print( f'   anova1rm:                {fi.zstar:.5f}')




# plot:
plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(8,3), tight_layout=True)
axs[0].plot(y0.T, 'k', lw=0.5)
axs[0].plot(y1.T, 'c', lw=0.5)
ax = axs[1]
fi.plot(ax=ax)
ax.plot(ti.z**2, color='m', label='t**2 (from ttest_paired)')
ax.axhline(ti.zstar**2, color='m', linestyle='--', label='zstar**2 (from ttest_paired)')
ax.set_title('anova1rm')
ax.legend()
plt.show()



