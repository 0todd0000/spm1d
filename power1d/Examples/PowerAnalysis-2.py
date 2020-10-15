import numpy as np
import power1d

#(0) Create geometry and noise models:
JA,JB,Q   = 5, 7, 101
baseline  = power1d.geom.Null(Q=Q)
signal0   = power1d.geom.Null(Q=Q)
signal1   = power1d.geom.GaussianPulse(Q=101, q=65, amp=2.5, sigma=10)
noise     = power1d.noise.Gaussian(J=5, Q=101, sigma=1)

#(1) Create data sample models:
modelA0   = power1d.models.DataSample(baseline, signal0, noise, J=JA) #null A
modelB0   = power1d.models.DataSample(baseline, signal0, noise, J=JB) #null N
modelA1   = power1d.models.DataSample(baseline, signal0, noise, J=JA) #alternative A
modelB1   = power1d.models.DataSample(baseline, signal1, noise, J=JB) #alternative B

#(2) Create experiment models:
teststat  = power1d.stats.t_2sample_fn(JA, JB)
expmodel0 = power1d.models.Experiment([modelA0, modelB0], teststat) #null
expmodel1 = power1d.models.Experiment([modelA1, modelB1], teststat) #alternative

#(3) Simulate experiments:
np.random.seed(0)
sim       = power1d.ExperimentSimulator(expmodel0, expmodel1)
results   = sim.simulate(1000, progress_bar=True)
results.plot()