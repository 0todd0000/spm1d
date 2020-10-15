import numpy as np
from matplotlib import pyplot
import power1d

Q        = 101
x        = np.array( [False] * Q )
x[40:60] = True
roi      = power1d.roi.RegionOfInterest(x)

pyplot.close('all')
roi.plot()