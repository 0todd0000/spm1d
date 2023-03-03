import numpy as np
import matplotlib.pyplot as plt
import power1d

J = 3
Q = 5

fig,axs  = plt.subplots(2, 2, tight_layout=True)
axs[1,1].set_visible(False)

# (a) generate noise object:
np.random.seed(12345)
noise    = power1d.noise.Gaussian(J, Q, mu=0, sigma=1)
noise.plot( ax=axs[0,0] )

# (b) create new random data:
noise.random()
noise.plot( ax=axs[0,1] )

# (c) reset noise to its original state:
np.random.seed(12345)
noise.random()
noise.plot( ax=axs[1,0] )

# add panel labels:
labels   = '(a)  Original noise', '(b)  New noise', '(c)  Reset using np.random.seed'
for ax,s in zip( axs.ravel() , labels ):
        ax.text(0.05, 0.9, s, transform=ax.transAxes, bbox=dict(facecolor='w'))