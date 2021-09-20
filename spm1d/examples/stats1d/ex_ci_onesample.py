
'''
One-sample confidence intervals for 1D data:

NOTES:
1.  If mu=None then explicit hypothesis testing is suppressed (i.e. exploratory analysis)
Note that the hypothesis test is still conducted implicitly (to compute the CI).
However, the explicit null hypothesis rejection decision will not appear when using either "print(ci)" or "ci.plot()".
Note especially that these one-sample CIs are invalid for two-sample, regression and ANOVA-like experiments.
Thus "mu=None" is generally useful only for exploratory purposes.

2.  If mu is a 0D scalar or a 1D scalar field then:
- Explicit null hypothesis testing is conducted
- The null hypothesis is rejected if mu lies outside the CI at any point in the 1D field
- A 0D scalar value for mu represents a constant 1D field
'''


import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
# dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()
### create arbitrary population means to which the data will be compared:
mu0        = 0
mu1        = 5*np.sin( np.linspace(0, np.pi, y.shape[1]) )




#(1) Compute confidence intervals:
alpha      = 0.05
ci0        = spm1d.stats.ci_onesample(y, alpha, mu=mu0)
ci1        = spm1d.stats.ci_onesample(y, alpha, mu=mu1)
print( ci0 )
print( ci1 )



#(2) Plot the CIs:
plt.close('all')
plt.figure(figsize=(14,7))


### FIRST POPULATION MEAN

### plot means and SD:
ax = plt.subplot(231)
spm1d.plot.plot_mean_sd(y-mu0, ax=ax)
ax.set_title('Mean and SD', size=10)
spm1d.plot.legend_manual(ax, labels=['Mean', 'SD'], colors=['k','0.85'], linestyles=['-', '-'], linewidths=[3, 10], loc='upper left', fontsize=10)

### plot hypothesis test results:
ax = plt.subplot(232)
spmi = spm1d.stats.ttest(y, mu0).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_p_values()
ax.set_title('Hypothesis test', size=10)

### plot CIs:
ax = plt.subplot(233)
ci0.plot(ax)
ax.set_title('CI  (criterion: mu=0)', size=10)
spm1d.plot.legend_manual(ax, labels=['Mean', 'CI', 'Criterion'], colors=['k','0.85','r'], linestyles=['-', '-','--'], linewidths=[3, 10, 1], loc='upper left', fontsize=10)


### SECOND POPULATION MEAN

### plot means and SD:
ax = plt.subplot(234)
spm1d.plot.plot_mean_sd(y-mu1, ax=ax)
ax.set_title('Mean and SD  (y - mu1)', size=10)

### plot hypothesis test results:
ax = plt.subplot(235)
spmi = spm1d.stats.ttest(y, mu1).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_p_values()
ax.set_title('Hypothesis test (y - mu1)', size=10)

### plot CIs:
ax = plt.subplot(236)
ci1.plot(ax)
ax.set_title('CI  (criterion: mu1)', size=10)


plt.suptitle('One-sample analysis')
plt.show()



