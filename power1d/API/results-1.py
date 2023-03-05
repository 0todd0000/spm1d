import numpy as np
import matplotlib.pyplot as plt
import power1d

J        = 8
Q        = 101
baseline = power1d.geom.Null( Q=Q )
signal0  = power1d.geom.Null( Q=Q )
signal1  = power1d.geom.GaussianPulse( Q=Q, q=40, fwhm=15, amp=1.0 )
noise    = power1d.noise.Gaussian( J=J, Q=Q, mu=0, sigma=0.3 )
model0   = power1d.models.DataSample(baseline, signal0, noise, J=J)
model1   = power1d.models.DataSample(baseline, signal1, noise, J=J)

emodel0  = power1d.models.Experiment( [model0, model0], fn=power1d.stats.t_2sample )
emodel1  = power1d.models.Experiment( [model0, model1], fn=power1d.stats.t_2sample )

sim      = power1d.models.ExperimentSimulator(emodel0, emodel1)
results  = sim.simulate(iterations=200, progress_bar=True)

plt.close('all')
results.plot()