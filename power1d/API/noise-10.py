import power1d

noise   = power1d.noise.Skewed( J=8, Q=101, mu=0, sigma=1.0, alpha=5 )
noise.plot()