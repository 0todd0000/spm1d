import power1d

noise0  = power1d.noise.SmoothGaussian( J=8, Q=501, mu=0, sigma=1.0, fwhm=100 )
noise1  = power1d.noise.Gaussian( J=8, Q=501, mu=0, sigma=0.1 )
noise   = power1d.noise.Additive(noise0, noise1)
noise.plot()