
import numpy as np


class SimulationResults(object):
	def __init__(self, z, validator):
		self.x         = np.asarray(z, dtype=float)
		self.validator = validator
		
	def __repr__(self):
		s  =  'SimulationResults\n'
		s += f'  n       = {self.n}\n'
		s += f'  x       = ({self.n},) array\n'
		s += f'  xc      = {self.xc}\n'
		s += f'  p       = {self.p:.5f}\n'
		s += f'  isvalid = {self.isvalid}\n'
		return s
		
	@property
	def alpha(self):
		return self.validator.alpha
	@property
	def xc(self):
		if self.valtype=='z':
			return self.validator.u
		else:
			return self.alpha
	@property
	def valtype(self):
		return self.validator.valtype
	
	@property
	def isvalid(self):
		return abs(self.p - self.validator.alpha) < self.validator.tol

	@property
	def n(self):
		return self.x.size

	@property
	def p(self):
		if self.valtype=='h0':
			return self.x.mean()
		elif self.valtype=='p':
			return (self.x < self.alpha).mean()
		elif self.valtype=='z':
			return (self.x > self.xc).mean()

	def plot(self, ax):
		ax.hist(self.x, bins=21, density=True, color='0.7', ec='0.5')
		ax.axvline(self.xc, color='r', ls='--')
		ax.text(0.03, 0.92, 'p = %0.5f'%self.p, transform=ax.transAxes, color='r' )
		ax.set_xlabel( f'{self.valtype}-value' )
		ax.set_ylabel('Density')