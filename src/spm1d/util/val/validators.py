
import numpy as np



class FPRValidator(object):
	def __init__(self, fn, rng, alpha=0.05, valtype='h0', u=None, tol=0.005, progress_bar=True):
		if valtype not in ('h0', 'p', 'z'):
			raise ValueError('valtype must be one of: "h0", "p" or "z"')
		self.alpha         = alpha   # false positive rate (FPR)
		self.fn            = fn      # an spm1d.stats LAMBDA function that accepts ONLY y
		self.rng           = rng     # random dataset generator
		# self.ikwargs       = ikwargs # optional dictionary of keyword arguments for inference
		self.valtype       = valtype # results type ("z" or "p")   "z" means test statistic, "p" means p-value
		self.u             = None    # critical threshold (required when valtype="z", otherwise ignored)
		self.results       = None    # simulation results
		self.tol           = tol     # tolerance for validation
		self.progbar       = progress_bar  # whether or not to display a progress bar
		if self.valtype=='z':
			if isinstance(u, (int,float,list,tuple)):
				self.u     = u
			else:
				raise ValueError('When valtype is "z", the critical threshold "u" must also be specified')

	def __repr__(self):
		s  =  'FPRValidator\n'
		s += f'  fn       = {self.fn}\n'
		s += f'  rng      = {self.rng}\n'
		s += f'  alpha    = {self.alpha}\n'
		u  = None if self.u is None else f'{self._ustr}'
		s += f'  u        = {u}\n'
		# s += f'  ikwargs  = {self.ikwargs}\n'
		s += f'  valtype  = {self.valtype}\n'
		s += f'  tol      = {self.tol}\n'
		if self.hasresults:
			s += self.results.__repr__()
		return s
	
	
	@property
	def _ustr(self):
		if isinstance(self, (int,float)):
			s = f'{self.u:.3f}'
		else:
			s = str(  np.around(self.u, 3)  )
		return s
	
	
	def _get_progbar(self, niter):
		if self.progbar:
			from .. prog import ProgressBar
			pbar = ProgressBar(50, niter)
		else:
			from .. prog import NullProgressBar
			pbar = NullProgressBar()
		return pbar
		
	
	@property
	def fpr(self):
		return self.results.fpr if self.hasresults else None

	@property
	def hasresults(self):
		return self.results is not None
	
	@property
	def isvalid(self):
		return self.results.isvalid if self.hasresults else None
	
	def plot_results(self):
		self.results.plot()
	
	def sim_single(self):
		y   = self.rng()
		spm = self.fn(y)
		return spm
	
	def sim(self, niter=1000):
		pbar = self._get_progbar(niter)
		z    = []
		for i in range(niter):
			pbar.update(i)
			spm = self.sim_single()
			if self.valtype == 'h0':
				spm = spm.inference( self.alpha )
				if isinstance(spm, list):
					zz  = [s.h0reject  for s in spm]
				else:
					zz  = spm.h0reject
			if self.valtype == 'p':
				spm = spm.inference( self.alpha )
				if isinstance(spm, list):
					zz  = [s.p if (s.dim == 0) else s.p_max  for s in spm]
				else:
					zz  = spm.p if (spm.dim == 0) else spm.p_max
			elif self.valtype=='z':
				if isinstance(spm, list):
					zz = [s.z if (s.dim == 0) else s.z.max()  for s in spm]
				else:
					zz = spm.z if (spm.dim == 0) else spm.z.max()
			z.append( zz )
		pbar.destroy()
		z            = np.asarray(z)
		if z.ndim == 2:
			from . results import SimulationResultsMultiContrast
			self.results = SimulationResultsMultiContrast(z, self)
		else:
			from . results import SimulationResults
			self.results = SimulationResults(z, self)
