
import os
import numpy as np
import matplotlib.pyplot as plt
import spm1d

# load data (30 curves, arbitrary length):
dir0         = os.path.dirname(__file__)
fname        = os.path.join(dir0, 'data', 'ex_kinematics_for_interpolation.npy')
Y0           = np.load(fname, encoding='latin1', allow_pickle=True)   #30 curves


# interpolate to 101 points:
Y            = spm1d.util.interp(Y0, 101)


# plot:
plt.close('all')
fig,(ax0,ax1) = plt.subplots(1, 2, figsize=(8,3.5))
[ax0.plot(y, 'k')  for y in Y0]
ax0.plot(Y.T, 'k')
ax0.text(0.5, 0.9, 'Before interpolation', size=14, transform=ax0.transAxes, ha='center')
ax1.text(0.5, 0.9, 'After interpolation', size=14, transform=ax1.transAxes, ha='center')
plt.tight_layout()
plt.show()

