

'''
Compare two-tailed, two-sample t-test to one-way ANOVA

The tests should be identical, with F = t**2
(within numerical tolerance give different random permutations)
'''

import numpy as np
import matplotlib.pyplot as plt
import spm1d
import spm1d.stats.nonparam_old


# load data:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
# dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
# dataset      = spm1d.data.uv1d.t2.SmallSampleLargePosNegEffects()
y0,y1      = dataset.get_data()


# prepare data for ANOVA:
y          = np.vstack([y0,y1])
A          = np.hstack( [0]*y0.shape[0] + [1]*y1.shape[0] )



# conduct tests:
alpha      = 0.05
two_tailed = True
niter      = 1000
np.random.seed(0)
ti         = spm1d.stats.nonparam.ttest2(y1, y0).inference(alpha, two_tailed=two_tailed, iterations=niter)
np.random.seed(0)
fi         = spm1d.stats.nonparam.anova1(y, A).inference(alpha, iterations=niter)
print( 'Critical thresholds:')
print( f'   ttest2 (squared):     {ti.zstar**2:.5f}')
print( f'   anova1:               {fi.zstar:.5f}')




# plot:
plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(8,3), tight_layout=True)
axs[0].plot(y0.T, 'k', lw=0.5)
axs[0].plot(y1.T, 'c', lw=0.5)
ax = axs[1]
fi.plot(ax=ax)
ax.plot(ti.z**2, color='m', label='t**2 (from ttest2)')
ax.axhline(ti.zstar**2, color='m', linestyle='--', label='zstar**2 (from ttest2)')
ax.set_title('anova1')
ax.legend()
plt.show()


