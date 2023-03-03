import matplotlib.pyplot as plt
import power1d

J        = 8    # sample size
Q        = 365  # continuum size
noise0   = power1d.noise.Gaussian( J , Q , mu = 0 , sigma = 0.3 )
noise1   = power1d.noise.SmoothGaussian( J , Q , mu = 0 , sigma = 3 , fwhm = 70 )
noise    = power1d.noise.Additive( noise0 , noise1 )

fig,axs  = plt.subplots(2, 2, tight_layout=True)
axs[1,1].set_visible( False )

# plot noise objects:
noise0.plot( ax=axs[0,0] )
noise1.plot( ax=axs[0,1] )
noise.plot( ax=axs[1,0] )
plt.setp(axs, ylim=(-9, 9))

# add panel labels:
labels   = 'Gaussian', 'SmoothGaussian', 'Additive'
for ax,s in zip( axs.ravel() , labels ):
        ax.text(0.05, 0.9, s, transform=ax.transAxes, bbox=dict(facecolor='w'))