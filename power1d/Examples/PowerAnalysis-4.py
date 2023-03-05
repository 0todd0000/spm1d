import numpy as np
import power1d

#(0) Create geometry and noise models:
JA,JB,JC,Q = 5, 7, 12, 101
baseline   = power1d.geom.Null(Q=Q)
signal0    = power1d.geom.Null(Q=Q)
signal1    = power1d.geom.GaussianPulse(Q=101, q=65, amp=1.5, sigma=10)
noise      = power1d.noise.Gaussian(J=5, Q=101, sigma=1)

#(1) Create data sample models:
modelA0   = power1d.models.DataSample(baseline, signal0, noise, J=JA)  #null A
modelB0   = power1d.models.DataSample(baseline, signal0, noise, J=JB)  #null B
modelC0   = power1d.models.DataSample(baseline, signal0, noise, J=JC)  #null C
modelA1   = power1d.models.DataSample(baseline, signal0, noise, J=JA)  #alternative A
modelB1   = power1d.models.DataSample(baseline, signal0, noise, J=JB)  #alternative B
modelC1   = power1d.models.DataSample(baseline, signal1, noise, J=JC)  #alternative C

#(2) Create experiment models:
teststat  = power1d.stats.f_anova1_fn(JA, JB, JC)
expmodel0 = power1d.models.Experiment([modelA0, modelB0, modelC0], teststat)
expmodel1 = power1d.models.Experiment([modelA1, modelB1, modelC1], teststat)

#(3) Simulate experiments:
np.random.seed(0)
sim       = power1d.ExperimentSimulator(expmodel0, expmodel1)
results   = sim.simulate(500, progress_bar=True)
results.plot()