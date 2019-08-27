from matplotlib import pyplot as plt
import mwarp1d

#define warp:
Q      = 101
center = 0.25
amp    = 0.5
head   = 0.2
tail   = 0.2

#apply warp:
y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
yw   = mwarp1d.warp_manual(y, center, amp, head, tail) #warped 1D observation

#plot:
plt.figure()
ax = plt.axes()
ax.plot(y, label='Original')
ax.plot(yw, label='Warped')
ax.legend()
ax.set_xlabel('Domain position  (%)', size=13)
ax.set_ylabel('Dependent variable value', size=13)
plt.show()