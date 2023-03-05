import power1d

#(0) Create geometry and noise models:
J         = 5    # sample size
Q         = 101  # continuum size
q         = 65   # signal location
baseline  = power1d.geom.Null(Q=Q)
signal0   = power1d.geom.Null(Q=Q)
signal1   = power1d.geom.GaussianPulse(Q=101, q=q, amp=1.3, sigma=10)
noise     = power1d.noise.Gaussian(J=5, Q=101, sigma=1)

#(1) Create data sample models:
model0    = power1d.models.DataSample(baseline, signal0, noise, J=J)  #null
model1    = power1d.models.DataSample(baseline, signal1, noise, J=J)  #alternative

#(2) Visualize the models:
model0.plot( color='k' )
model1.plot( color='r' )