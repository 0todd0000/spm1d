from matplotlib import pyplot
import power1d

J        = 8    # sample size
Q        = 365  # continuum size
noise0   = power1d.noise.Gaussian( J , Q , mu = 0 , sigma = 0.3 )
noise1   = power1d.noise.SmoothGaussian( J , Q , mu = 0 , sigma = 3 , fwhm = 70 )
noise    = power1d.noise.Additive( noise0 , noise1 )

ax0      = pyplot.subplot(221)
ax1      = pyplot.subplot(222)
ax2      = pyplot.subplot(223)
AX       = [ax0, ax1, ax2]

# plot noise objects:
noise0.plot( ax=ax0 )
noise1.plot( ax=ax1 )
noise.plot( ax=ax2 )
pyplot.setp(AX, ylim=(-9, 9))

# add panel labels:
labels   = 'Gaussian', 'SmoothGaussian', 'Additive'
for ax,s in zip( AX , labels ):
        ax.text(0.05, 0.9, s, transform=ax.transAxes, bbox=dict(facecolor='w'))