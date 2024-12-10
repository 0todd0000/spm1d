import matplotlib.pyplot as plt
import power1d

J        = 20
Q        = 101
baseline = power1d.geom.Null( Q=Q )
signal   = power1d.geom.GaussianPulse( Q=Q, q=40, fwhm=15, amp=3.5 )
noise    = power1d.noise.SmoothGaussian( J=J, Q=Q, mu=0, sigma=1.0, fwhm=20 )
model    = power1d.models.DataSample(baseline, signal, noise, J=J)
plt.close('all')
model.plot(color="g", lw=5)