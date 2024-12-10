import numpy as np
from matplotlib import pyplot
import rft1d
np.random.seed(0)
y = rft1d.randn1d(5, 101, 80.0, pad=True)
pyplot.figure(figsize=(5,3))
pyplot.plot(y.T)
pyplot.plot([0,100],[0,0],'k:')