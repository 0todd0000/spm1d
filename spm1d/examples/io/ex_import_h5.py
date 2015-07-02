
import os
import numpy as np
from matplotlib import pyplot
import spm1d

# load HDF5 data (30 rows, 100 columns):
dir0         = os.path.dirname(__file__)
fname        = os.path.join(dir0, 'data', 'ex_kinematics.h5')
Y            = spm1d.io.load(fname)   #30 curves, 100 nodes

# plot:
pyplot.close('all')
pyplot.plot(Y.T, color = 'k')
pyplot.xlabel('Time (%)', size=20)
pyplot.ylabel(r'$\theta$ (deg)', size=20)
pyplot.show()
