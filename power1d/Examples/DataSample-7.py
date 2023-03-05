import numpy as np
import matplotlib.pyplot as plt
import power1d

J        = 8    # sample size
Q        = 365  # continuum size

# construct baseline geometry:
g0       = power1d.geom.GaussianPulse( Q , q=200 , fwhm=190 , amp=40 )
g1       = power1d.geom.Constant( Q , amp=23 )
baseline = g0 - g1  # subtract the geometries

# construct signal geometry:
signal   = power1d.geom.GaussianPulse( Q , q=200 , fwhm=100 , amp=5 )

# construct noise model:
noise0   = power1d.noise.Gaussian( J , Q , mu = 0 , sigma = 0.3 )
noise1   = power1d.noise.SmoothGaussian( J , Q , mu = 0 , sigma = 3 , fwhm = 70 )
noise    = power1d.noise.Additive( noise0 , noise1 )

# create data sample model:
model    = power1d.models.DataSample( baseline, signal, noise, J=J )

# visualize
fig,axs  = plt.subplots(2, 2, tight_layout=True)
axs[1,1].set_visible( False )

np.random.seed(12345)
model.random()
model.plot( ax=axs[0,0] )

model.random()
model.plot( ax=axs[0,1] )

np.random.seed(12345)
model.random()
model.plot( ax=axs[1,0] )

plt.setp(axs, ylim=(-25, 40))

# add panel labels:
labels   = '(a)  Original model state', '(b)  New state', '(c)  Reset using np.random.seed'
for ax,s in zip( axs.ravel() , labels ):
        ax.text(0.05, 0.9, s, transform=ax.transAxes, bbox=dict(facecolor='w'))