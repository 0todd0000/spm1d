import numpy as np
from matplotlib import pyplot
import spm1d
np.random.seed(0)
Y = np.random.randn(10,100) +0.21
Y = spm1d.util.smooth(Y, fwhm=10)
t  = spm1d.stats.ttest(Y)
pyplot.figure(figsize=(5,4))
pyplot.axes([0.15,0.15,0.82,0.82])
t.plot()
pyplot.ylim(0, 5)
pyplot.xlabel('Measurement domain q  (%)')
pyplot.ylabel('SPM{t}')