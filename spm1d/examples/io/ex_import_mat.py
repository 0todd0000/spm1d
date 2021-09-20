
import os
import scipy.io
import matplotlib.pyplot as plt



# load Matlab data:
dir0         = os.path.dirname(__file__)
fname        = os.path.join(dir0, 'data', 'ex_kinematics.mat')
Y            = scipy.io.loadmat(fname)['Y']   #30 curves, 100 nodes

# plot:
plt.close('all')
plt.plot(Y.T, color = 'k')
plt.xlabel('Time (%)', size=20)
plt.ylabel(r'$\theta$ (deg)', size=20)
plt.show()
