import numpy as np
import power1d

Q       = 101
noise0  = power1d.noise.Gaussian( J=5, Q=Q, mu=0, sigma=1.0 )
scale   = np.linspace(0, 1, Q)
noise   = power1d.noise.Scaled(noise0, scale)
noise.plot()