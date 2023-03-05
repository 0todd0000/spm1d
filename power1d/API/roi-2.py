import numpy as np
import matplotlib.pyplot as plt
import power1d

Q        = 101
x        = np.array( [False] * Q )
x[40:60] = True
roi      = power1d.roi.RegionOfInterest(x)

plt.close('all')
roi.plot()