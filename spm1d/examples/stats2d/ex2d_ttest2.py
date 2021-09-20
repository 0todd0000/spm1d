
import os
import numpy as np
import matplotlib.pyplot as plt
import spm1d


eps     = np.finfo(float).eps 


#(0) Load data:
dir0    = os.path.dirname(__file__)
fname   = os.path.join(dir0, 'data2d.npy')
Y0      = np.load(fname)
y0      = np.array([yy.flatten() for yy in Y0])
J,Q     = y0.shape



#(1) Remove zero-variance nodes:
yA      = y0[:10]
yB      = y0[10:]
iA      = yA.std(axis=0) > eps
iB      = yB.std(axis=0) > eps
i       = np.logical_and(iA, iB)
y       = y0[:,i]
yA      = y[:10]
yB      = y[10:]



#(2) Run SnPM:
snpm    = spm1d.stats.nonparam.ttest2(yA, yB)
snpmi   = snpm.inference(0.05, two_tailed=True, iterations=1000)



#(3) Visualize:
z       = snpmi.z
zstar   = snpmi.zstar
z0      = np.zeros(Q)
z0[i]   = z
Z0      = np.reshape(z0, Y0.shape[1:])
Z0i     = Z0.copy()
Z0i[np.abs(Z0i)<zstar] = 0
ZZ      = np.hstack( [Z0, Z0i] )


plt.close('all')
plt.figure()
ax = plt.axes()
ax.imshow(np.ma.masked_array(ZZ, ZZ==0), origin='lower', cmap='jet', vmin=-15, vmax=15)
ax.set_title('SPM results')
ax.text(16, 10, 'Raw SPM', ha='center')
ax.text(48, 10, 'Inference', ha='center')
cb = plt.colorbar(mappable=ax.images[0])
cb.set_label('t value')
plt.tight_layout()
plt.show()


