import power1d

noise   = power1d.noise.Uniform( J=8, Q=101, x0=0, x1=1.0 )
noise.plot()