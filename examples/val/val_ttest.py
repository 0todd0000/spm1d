
# validate FPR for ttest

import numpy as np
import matplotlib.pyplot as plt
import spm1d


class SimulationResultsZ(object):
	def __init__(self, z):
		self.z  = z
		
	def plot(self, ax):
		ax.hist(self.z, bins=21, density=True)



class FPRValidator(object):
	def __init__(self, fn, rng, alpha=0.04, **ikwargs):
		self.alpha   = alpha   # false positive rate (FPR)
		self.fn      = fn      # an spm1d.stats LAMBDA function that accepts ONLY y
		self.rng     = rng     # random dataset generator
		self.ikwargs = ikwargs # optional keyword arguments for inference

	def get_zc(self, alpha=0.05):
		spmi = self.sim_single().inference(alpha, **self.ikwargs)
		return spmi.zc
	
	def sim_single(self):
		y   = self.rng()
		spm = self.fn(y)
		return spm
	
	def sim(self, niter=1000, teststat_only=True):
		z = []
		for i in range(niter):
			# report progress
			spm = self.sim_single()
			if teststat_only:
				zz = spm.z if (spm.dim == 0) else spm.z.max()
			else:
				spm = spm.inference(0.05, **self.ikwargs)
				zz  = spm.p if (spm.dim == 0) else spm.p_max
			z.append( zz )
		if teststat_only:
			return SimulationResultsZ(z)
		else:
			return SimulationResultsP(z)
			
			


		# def report(self):
		# 	p = np.asarray(p)
		# 	print( (p<0.05).mean() )
		# 	plt.close('all')
		# 	plt.figure()
		# 	plt.get_current_fig_manager().window.move(0, 0)
		# 	ax = plt.axes()
		# 	ax.hist(p, density=True)
		# 	plt.show()
		#
	
		



np.random.seed(0)

fn  = lambda y: spm1d.stats.ttest(y, 0)
rng = lambda: np.random.randn(8)
# y   = np.random.randn(8)


# y = rng()
# spm = fn(y)
# spm = fn(y)


val = FPRValidator(fn, rng, dirn=1)
# spm = val.sim_single()
# zc = val.get_zc()

res = val.sim( niter=2000 )


plt.close('all')
plt.figure()
plt.get_current_fig_manager().window.move(0, 0)
ax = plt.axes()
res.plot(ax=ax)
plt.show()

