import numpy as np
from matplotlib import pyplot as plt
import mwarp1d

#define warp:
Q    = 101                      #domain size
warp = mwarp1d.ManualWarp1D(Q)  #constrained Gaussian kernel warp object
warp.set_center(0.25)           #relative warp center (0 to 1)
warp.set_amp(0.5)               #relative warp amplitude (-1 to 1)
warp.set_head(0.2)              #relative warp head (0 to 1)
warp.set_tail(0.2)              #relative warp tail (0 to 1)

#apply warp:
y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
yw   = warp.apply_warp(y)                    #warped 1D observation

#plot:
plt.figure()
ax = plt.axes()
ax.plot(y, label='Original')
ax.plot(yw, label='Warped')
ax.legend()
ax.set_xlabel('Domain position  (%)', size=13)
ax.set_ylabel('Dependent variable value', size=13)
plt.show()