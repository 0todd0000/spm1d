import numpy as np
import power1d

#(0) Create geometry and noise models:
J,Q       = 30, 101
x         = np.linspace(0, 2, J)  #regressor (must have J values)
baseline  = power1d.geom.Null(Q=Q)
signal0   = power1d.geom.Null(Q=Q)
signal1   = power1d.geom.GaussianPulse(Q=101, q=65, amp=2.0, sigma=10)
noise     = power1d.noise.Gaussian(J=5, Q=101, sigma=1)

#(1) Create data sample models:
model0    = power1d.models.DataSample(baseline, signal0, noise, J=J, regressor=x)
model1    = power1d.models.DataSample(baseline, signal1, noise, J=J, regressor=x)

#(2) Create experiment models:
teststat  = power1d.stats.t_regress_fn(x)
expmodel0 = power1d.models.Experiment(model0, teststat)
expmodel1 = power1d.models.Experiment(model1, teststat)

#(3) Simulate experiments:
np.random.seed(0)
sim       = power1d.ExperimentSimulator(expmodel0, expmodel1)
results   = sim.simulate(100, progress_bar=True)
results.plot()