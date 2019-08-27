import numpy as np
from matplotlib import pyplot as plt
import mwarp1d

#define landmarks:
Q    = 101         #domain size
x0   = [38, 63]    #initial landmark locations
x1   = [25, 68]    #final landmark locations

#apply warp:
y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
yw   = mwarp1d.warp_landmark(y, x0, x1)      #warped 1D observation

#plot:
plt.figure()
ax    = plt.axes()
c0,c1 = 'blue', 'orange'
ax.plot(y,  color=c0, label='Original')
ax.plot(yw, color=c1, label='Warped')
[ax.plot(xx, y[xx],  'o', color=c0)  for xx in x0]
[ax.plot(xx, yw[xx], 'o', color=c1)    for xx in x1]
ax.legend()
ax.set_xlabel('Domain position  (%)', size=13)
ax.set_ylabel('Dependent variable value', size=13)
plt.show()