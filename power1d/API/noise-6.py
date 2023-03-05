import power1d

noise   = power1d.noise.Gaussian( J=8, Q=101, mu=0, sigma=1.0 )
noise.plot()