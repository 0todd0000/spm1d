
import os
import numpy as np
import matplotlib.pyplot as plt



# load plain-text data (30 rows, 100 columns):
dir0         = os.path.dirname(__file__)
fname        = os.path.join(dir0, 'data', 'ex_kinematics.txt')
Y            = np.loadtxt(fname)   #30 curves, 100 nodes

# plot:
plt.close('all')
plt.plot(Y.T, color = 'k')
plt.xlabel('Time (%)', size=20)
plt.ylabel(r'$\theta$ (deg)', size=20)
plt.show()
