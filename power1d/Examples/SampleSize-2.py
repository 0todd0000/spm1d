import numpy as np
from matplotlib import pyplot
import power1d

#(0) Create geometry and noise models:
J          = 5    # sample size
Q          = 101  # continuum size
q          = 65   # signal location
baseline   = power1d.geom.Null(Q=Q)
signal0    = power1d.geom.Null(Q=Q)
signal1    = power1d.geom.GaussianPulse(Q=101, q=q, amp=1.3, sigma=10)
noise      = power1d.noise.Gaussian(J=5, Q=101, sigma=1)

#(1) Create data sample models:
model0     = power1d.models.DataSample(baseline, signal0, noise, J=J)  #null
model1     = power1d.models.DataSample(baseline, signal1, noise, J=J)  #alternative

#(2) Iteratively simulate for a range of sample sizes:
np.random.seed(0)    #seed the random number generator
JJ         = [5, 6, 7, 8, 9, 10]  #sample sizes
tstat      = power1d.stats.t_1sample  #test statistic function
emodel0    = power1d.models.Experiment(model0, tstat) # null
emodel1    = power1d.models.Experiment(model1, tstat) # alternative
sim        = power1d.ExperimentSimulator(emodel0, emodel1)
### loop through the different sample sizes:
power_omni = []
power_coi  = []
coir       = 3
for J in JJ:
        emodel0.set_sample_size( J )
        emodel1.set_sample_size( J )
        results = sim.simulate( 1000 )
        results.set_coi( ( q , coir ) )  #create a COI at the signal location
        power_omni.append( results.p_reject1 )  #omnibus power
        power_coi.append( results.p_coi1[0] )   #coi power

#(3) Plot the results:
ax = pyplot.axes()
ax.plot(JJ, power_omni, 'o-', label='Omnibus')
ax.plot(JJ, power_coi,  'o-', label='COI (radius=%d)' %coir)
ax.axhline(0.8, color='k', linestyle='--')
ax.set_xlabel('Sample size', size=14)
ax.set_ylabel('Power', size=14)
ax.legend()
pyplot.show()