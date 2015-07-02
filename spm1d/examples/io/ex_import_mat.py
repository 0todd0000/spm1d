
import os
import scipy.io
from matplotlib import pyplot



# load Matlab data:
dir0         = os.path.dirname(__file__)
fname        = os.path.join(dir0, 'data', 'ex_kinematics.mat')
Y            = scipy.io.loadmat(fname)['Y']   #30 curves, 100 nodes

# plot:
pyplot.close('all')
pyplot.plot(Y.T, color = 'k')
pyplot.xlabel('Time (%)', size=20)
pyplot.ylabel(r'$\theta$ (deg)', size=20)
pyplot.show()
