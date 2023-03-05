import numpy as np
import matplotlib.pyplot as plt
import power1d

J      = 8  # sample size
Q      = 101  # number of continuum nodes
x      = 5.1 + 5 * np.sin( np.linspace(0, 4*np.pi, Q) )
noise  = power1d.noise.SmoothGaussian( J, Q, fwhm=30 ) # baseline noise model
snoise = power1d.noise.from_array( noise, x ) # scaled noise object

fig,axs = plt.subplots(1, 3, figsize=(10,3), tight_layout=True)
noise.plot( ax=axs[0] )
axs[1].plot( x )
snoise.plot( ax=axs[2] )
labels  = 'Baseline noise model', 'Scaling array', 'Scaled noise'
[ax.set_title(s) for ax,s in zip(axs,labels)]
plt.show()