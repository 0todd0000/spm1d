
import os
import numpy as np
from matplotlib import pyplot
import spm1d

# load data (30 curves, arbitrary length):
dir0         = os.path.dirname(__file__)
fname        = os.path.join(dir0, 'data', 'ex_kinematics_for_interpolation.npy')
Y0           = np.load(fname)   #30 curves


# interpolate to 101 points:
Y            = spm1d.util.interp(Y0, 101)


# plot:
pyplot.close('all')
pyplot.figure(figsize=(8,3.5))
ax0          = pyplot.axes((0.1,0.15,0.35,0.8))
ax1          = pyplot.axes((0.55,0.15,0.35,0.8))
[ax0.plot(y, 'k')  for y in Y0]
pyplot.plot(Y.T, 'k')
ax0.text(0.5, 0.9, 'Before interpolation', size=14, transform=ax0.transAxes, ha='center')
ax1.text(0.5, 0.9, 'After interpolation', size=14, transform=ax1.transAxes, ha='center')
pyplot.show()

