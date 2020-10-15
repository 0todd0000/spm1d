import power1d

noise   = power1d.noise.ConstantGaussian( J=8, Q=101, mu=0, sigma=1.0 )
noise.plot()