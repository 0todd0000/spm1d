from matplotlib import pyplot
import power1d

J = 3
Q = 5

ax0      = pyplot.subplot(221)
ax1      = pyplot.subplot(222)
ax2      = pyplot.subplot(223)
AX       = [ax0, ax1, ax2]

# (a) generate noise object:
np.random.seed(12345)
noise    = power1d.noise.Gaussian(J, Q, mu=0, sigma=1)
noise.plot( ax=ax0 )

# (b) create new random data:
noise.random()
noise.plot( ax=ax1 )

# (c) reset noise to its original state:
np.random.seed(12345)
noise.random()
noise.plot( ax=ax2 )

# add panel labels:
labels   = '(a)  Original noise', '(b)  New noise', '(c)  Reset using np.random.seed'
for ax,s in zip( AX , labels ):
        ax.text(0.05, 0.9, s, transform=ax.transAxes, bbox=dict(facecolor='w'))