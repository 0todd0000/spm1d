import numpy as np
from matplotlib import pyplot as plt
import mwarp1d

#plot:
plt.close('all')
plt.figure()
ax     = plt.axes()

#plot example pulse:
w = mwarp1d.ManualWarp1D(100)
w.set_center(0.20)
w.set_amp(0.25)
w.set_head(0.9)
w.set_tail(0.3)
dq = w.get_displacement_field()
ax.plot(dq, color='b')
ax.set_xlabel('Domain position  (%)', size=13)
ax.set_ylabel('Displacement  (%)', size=13)
# label parameters:
c = w.center
ax.plot([0,c], [0,0], color='k', ls=':')
ax.plot([c]*2, [0,dq.max()], color='k', ls=':')
xh,xt = 10,58
ax.plot([xh,c], [dq[xh]]*2, color='k', ls=':')
ax.plot([c,xt], [dq[xt]]*2, color='k', ls=':')
# print(dq[xh]/dq.max(), dq[xt]/dq.max())


bbox = dict(facecolor='w', edgecolor='0.7', alpha=0.9)
ax.text(0.5*c, 0, 'center', ha='center', bbox=bbox)
ax.text(c, 0.8*dq.max(), 'amp', ha='center', bbox=bbox)
ax.text(0.5*(xh+c), dq[xh], 'head', ha='center', bbox=bbox)
ax.text(c + 0.5*(xt-c), dq[xt], 'tail', ha='center', bbox=bbox)
ax.legend(['Displacement field'])

plt.show()