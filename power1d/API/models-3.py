import matplotlib.pyplot as plt
import power1d

J        = 8
Q        = 101
baseline = power1d.geom.Null( Q=Q )
signal   = power1d.geom.GaussianPulse( Q=Q, q=75, fwhm=15, amp=5.0 )
noise    = power1d.noise.Gaussian( J=J, Q=Q, mu=0, sigma=1.0 )
model    = power1d.models.DataSample(baseline, signal, noise, J=J)
plt.close('all')
model.plot(color="b", lw=5)