
import numpy as np
from matplotlib import pyplot
import spm1d



#generate random data:
np.random.seed(0)
Y0     = np.random.randn(10,100) +0.21
Y1     = np.random.randn(10,100) +0.08
Y0     = spm1d.util.smooth(Y0, fwhm=10)
Y1     = spm1d.util.smooth(Y1, fwhm=20)

#compute test statistics:
t0     = spm1d.stats.ttest(Y0)
t1     = spm1d.stats.ttest(Y1)

#conduct inference (uncorrected)
alpha   = 0.05
t0iU    = t0.inference(alpha, two_tailed=False)
t1iU    = t1.inference(alpha, two_tailed=False)

#conduct inference (corrected)
nTests  = 2
p_crit  = spm1d.util.p_critical_bonf(alpha, nTests)
t0i     = t0.inference(p_crit, two_tailed=False)
t1i     = t1.inference(p_crit, two_tailed=False)

#plot:
pyplot.close('all')
ax0=pyplot.subplot(221);  t0iU.plot()
ax1=pyplot.subplot(222);  t1iU.plot()
ax2=pyplot.subplot(223);  t0i.plot()
ax3=pyplot.subplot(224);  t1i.plot()
AX      = [ax0,ax1,ax2,ax3]
labels  = ['Y0, uncorrected', 'Y1, uncorrected', 'Y0, corrected', 'Y1, corrected']
[ax.text(50, 4.5, label, ha='center') for ax,label in zip(AX,labels)]
pyplot.setp(AX, xlim=(0,100), ylim=(0,5))
# pyplot.show()

