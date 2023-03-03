import power1d

J        = 8    # sample size
Q        = 365  # continuum size

# construct baseline geometry:
g0       = power1d.geom.GaussianPulse( Q , q=200 , fwhm=190 , amp=40 )
g1       = power1d.geom.Constant( Q , amp=23 )
baseline = g0 - g1  # subtract the geometries

# construct signal geometry:
signal0  = power1d.geom.Null( Q )
signal1  = power1d.geom.GaussianPulse( Q , q=200 , fwhm=100 , amp=5 )

# construct noise model:
noise0   = power1d.noise.Gaussian( J , Q , mu = 0 , sigma = 0.3 )
noise1   = power1d.noise.SmoothGaussian( J , Q , mu = 0 , sigma = 3 , fwhm = 70 )
noise    = power1d.noise.Additive( noise0 , noise1 )

# create data sample models:
model0   = power1d.models.DataSample( baseline, signal0, noise, J=J )
model1   = power1d.models.DataSample( baseline, signal1, noise, J=J )

# create experiment models:
teststat = power1d.stats.t_1sample
emodel0  = power1d.models.Experiment( model0 , teststat )    # null hypothesis
emodel1  = power1d.models.Experiment( model1 , teststat )    # alternative hypothesis

# simulate the experiments:
sim      = power1d.ExperimentSimulator( emodel0 , emodel1 )
results  = sim.simulate( 5000, progress_bar=True )

# visualize the power results:
results.plot()