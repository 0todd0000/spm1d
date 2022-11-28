
'''
One-sample confidence intervals for 0D data:

NOTES:
1.  If mu=None then explicit hypothesis testing is suppressed (i.e. exploratory analysis)
Note that the hypothesis test is still conducted implicitly (to compute the CI).
However, the explicit null hypothesis rejection decision will not appear when using either "print(ci)" or "ci.plot()".
Note especially that these one-sample CIs are invalid for two-sample, regression and ANOVA-like experiments.
Thus "mu=None" is generally useful only for exploratory purposes.

2.  If mu is a scalar then:
- explicit null hypothesis testing is conducted
- the null hypothesis is rejected if mu lies outside the CI
'''



import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
# dataset = spm1d.data.uv0d.ci1.MinnesotaGeyerRate()
dataset = spm1d.data.uv0d.ci1.WebsterSleep()
y,mu    = dataset.get_data()
print( dataset )



#(1) Compute confidence intervals:
alpha      = 0.05
mu         = 9
ci0        = spm1d.stats.ci_onesample(y, alpha, mu=None)  #hypothesis test results suppressed using "mu=None"
ci1        = spm1d.stats.ci_onesample(y, alpha, mu=mu)    #hypothesis test regarding a specific population mean "mu=9"
print( ci0 )
print( ci1 )



#(2) Plot the CIs:
plt.close('all')
plt.figure(figsize=(8,4))
ax0 = plt.subplot(121);  ci0.plot(ax0);  ax0.set_title('mu=None', size=10)
ax1 = plt.subplot(122);  ci1.plot(ax1);  ax1.set_title('mu=%.5f'%mu, size=10)
plt.suptitle('One-sample CIs')
plt.show()
