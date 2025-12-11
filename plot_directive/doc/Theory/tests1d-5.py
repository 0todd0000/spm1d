import numpy as np
from matplotlib import pyplot
import spm1d
np.random.seed(0)
Y  = np.random.randn(10,100) +0.21
Y  = spm1d.util.smooth(Y, fwhm=10)
t  = spm1d.stats.ttest(Y)
ti = t.inference(alpha=0.05, two_tailed=False)
pyplot.figure(figsize=(5,4))
pyplot.axes([0.15,0.15,0.82,0.82])
ti.plot()
ti.plot_threshold_label(fontsize=10)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
pyplot.xlim(0, 100)
pyplot.ylim(0, 5)
pyplot.xlabel('Measurement domain q (%)', size=14)