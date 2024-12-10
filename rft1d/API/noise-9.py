import numpy as np
import power1d

Q       = 101
noise0  = power1d.noise.Gaussian( J=5, Q=Q, mu=0, sigma=1.0 )
signal  = power1d.geom.GaussianPulse(Q=Q, q=60, amp=3, fwhm=15)
fn      = lambda n,s: n + (n * s**3)
noise   = power1d.noise.SignalDependent(noise0, signal, fn)
noise.plot()