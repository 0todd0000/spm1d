import power1d

noise   = power1d.noise.SmoothGaussian( J=8, Q=101, mu=0, sigma=1.0, fwhm=25, pad=False )
noise.plot()