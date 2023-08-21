
import numpy as np
import matplotlib.pyplot as plt


class SimulationResults(object):
	def __init__(self, z, validator):
		self.x         = np.asarray(z, dtype=float)
		self.validator = validator
		
	def __repr__(self):
		s  = f'{self.__class__.__name__}\n'
		s += f'  n       = {self.n}\n'
		s += f'  x       = {self._xstr}\n'
		s += f'  xc      = {self._xcstr}\n'
		s += f'  p       = {self._pstr}\n'
		s += f'  isvalid = {self.isvalid}\n'
		return s
		
		
	@property
	def _pstr(self):
		return f'{self.p:.5f}'
	@property
	def _xstr(self):
		return f'({self.n},) array'
	@property
	def _xcstr(self):
		return f'{self.xc:.5f}'
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
		return abs(self.p - self.validator.alpha) <= self.validator.tol

	@property
	def n(self):
		return self.x.size

	@property
	def p(self):
		if self.valtype=='h0':
			return self.x.mean(axis=0)
		elif self.valtype=='p':
			return (self.x < self.alpha).mean(axis=0)
		elif self.valtype=='z':
			return (self.x > self.xc).mean(axis=0)

	def plot(self):
		plt.close('all')
		plt.figure( figsize=(6,4) )
		ax = plt.axes()
		ax.hist(self.x, bins=21, density=True, color='0.7', ec='0.5')
		ax.axvline(self.xc, color='r', ls='--')
		ax.text(0.03, 0.92, 'p = %0.5f'%self.p, transform=ax.transAxes, color='r' )
		ax.set_xlabel( f'{self.valtype}-value' )
		ax.set_ylabel('Density')
		plt.show()
		
		
class SimulationResultsMultiContrast(SimulationResults):
	@property
	def _pstr(self):
		return str( np.around(self.p, 5) )
	@property
	def _xstr(self):
		return f'({self.n},{self.m}) array'
	@property
	def _xcstr(self):
		return str( np.around(self.xc, 5) )
	@property
	def m(self):
		return self.x.shape[1]
	@property
	def n(self):
		return self.x.shape[0]

	def plot(self):
		from math import ceil
		plt.close('all')
		n       = int( ceil( self.m**0.5 ) )
		fig,axs = plt.subplots( n, n, figsize=(10,7) )
		for ax,x,xc,p in zip(axs.ravel(), self.x.T, self.xc, self.p):
			ax.hist(x, bins=21, density=True, color='0.7', ec='0.5')
			ax.axvline(xc, color='r', ls='--')
			ax.text(0.03, 0.92, 'p = %0.5f'%p, transform=ax.transAxes, color='r' )
			ax.set_xlabel( f'{self.valtype}-value' )
			ax.set_ylabel('Density')
		plt.show()
		
