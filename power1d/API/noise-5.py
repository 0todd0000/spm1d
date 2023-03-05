import power1d

noise   = power1d.noise.ConstantUniform( J=8, Q=101, x0=-0.5, x1=1.3 )
noise.plot()