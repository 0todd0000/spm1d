import power1d

noise0  = power1d.noise.SmoothGaussian( J=3, Q=101, mu=3, sigma=1.0, fwhm=20 )
noise1  = power1d.noise.Gaussian( J=5, Q=101, mu=-3, sigma=1.0 )
noise   = power1d.noise.Mixture(noise0, noise1)
noise.plot()