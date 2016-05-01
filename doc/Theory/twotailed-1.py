import numpy as np
from matplotlib import pyplot
import spm1d
np.random.seed(0)
Y = np.random.randn(10,100) +0.21
Y = spm1d.util.smooth(Y, fwhm=10)
t  = spm1d.stats.ttest(Y)
ti0 = t.inference(alpha=0.05, two_tailed=False)
ti1 = t.inference(alpha=0.05, two_tailed=True)
pyplot.figure(figsize=(11,4))
pyplot.subplot(121);  ti0.plot();     ti0.plot_threshold_label(fontsize=10);  pyplot.ylim(-5, 5);  pyplot.text(50, -3, 'One-tailed', ha='center', size=14)
pyplot.subplot(122);  ti1.plot();     ti1.plot_threshold_label(fontsize=10);  pyplot.ylim(-5, 5);  pyplot.text(50, -3, 'Two-tailed', ha='center', size=14)