
'''
SPMi (inference) module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for inference SPMs.
'''

# Copyright (C) 2022  Todd Pataky

import warnings
from . _spm import _SPM #, _SPMF
from . _spm0d import SPM0D
from . _spm1d import SPM1D
from ... cfg import SPM1DDeprecationWarning
from ... util import dflist2str, p2string



class _SPMiParent(_SPM):
	'''Parent for inference SPM classes.'''
	
	isinference = True
	
	def __repr__(self):
		s0      = super().__repr__()
		s1      = self.iresults.__repr__()
		return s0 + s1

	@property
	def _dirn_str(self):
		s     = '0 (two-tailed)' if self.dirn==0 else f'{self.dirn} (one-tailed)'
		return s
		
	def _set_inference_results(self, iresults, df_adjusted):
		self._iargs          = None                 # arguments for inference
		self._ikwargs        = None                 # keyword arguments for inference
		self.iresults        = iresults
		self.df_adjusted     = df_adjusted
	
	# inference results properties
	@property
	def alpha(self):
		return self.iresults.alpha
	@property
	def dirn(self):
		return self.iresults.dirn
	# @property
	# def eqvar_assumed(self):
	# 	return self.df_adjusted is None
	@property
	def extras(self):
		return self.iresults.extras
	@property
	def h0reject(self):
		return self.iresults.h0reject
	# @property
	# def isparametric(self):
	# 	return self.method in ['param', 'rft', 'fdr', 'bonferroni', 'uncorrected']
	@property
	def isparametric(self):
		return self.iresults.isparametric
	
	@property
	def method(self):
		return self.iresults.method
	@property
	def p(self):
		return self.iresults.p
	@property
	def zc(self):
		return self.iresults.zc
	

	# @property
	# def _zcstr(self):
	# 	if isinstance(self.zc, float):
	# 		s  = f'{self.zc:.3f}'
	# 	else:
	# 		z0,z1 = self.zc
	# 		s  = f'{z0:.3f}, {z1:.3f}'
	# 	return s

	# @property
	# def nperm_actual(self):
	# 	return self.nperm
	#
	# @property
	# def nperm_possible(self):
	# 	return self.permuter.nPermTotal
	
	@property
	def two_tailed(self):
		return self.dirn == 0

	@property
	def zstar(self):   # legacy support ("zc" was "zstar" in spm1d versions < 0.5)
		msg = 'Use of "zstar" is deprecated. Use "zc" to avoid this warning.'
		warnings.warn( msg , SPM1DDeprecationWarning , stacklevel=2 )
		return self.zc

	
	def _reexec(self):
		import spm1d
		fn   = eval(  f'spm1d.stats.{self.testname}'  )
		spm  = fn( *self._args, **self._kwargs )
		if '_nprandstate' in self.extras.keys():
			state0 = np.random.get_state()
			np.random.set_state( self.extras['_nprandstate'] )
			spmi = spm.inference( *self._iargs, **self._ikwargs )
			np.random.set_state( state0 )
		else:
			spmi = spm.inference( *self._iargs, **self._ikwargs )
		return spmi
	

	
	def _repr_summ(self):  # abstract method to be implemented by all subclasses
		pass

	def isequal(self, other, verbose=False):
		import pytest
		super().isequal(other, verbose=verbose)
		if self.iresults != other.iresults:
			return False
		if self.df_adjusted != pytest.approx(other.df_adjusted):
			return False
		return True




class SPM0Di(_SPMiParent, SPM0D):
	def _repr_summ(self):
		# return '{:<5} z={:<8} df={:<15}  p={:<9}  h0reject={}\n'.format(self.name_s,  self._repr_teststat_short(), dflist2str(self.df), p2string(self.p,fmt='%.5f'), self.h0reject)
		return '{:<5} z={:<8} df={:<15}  p={}\n'.format(self.name_s,  self._repr_teststat_short(), dflist2str(self.df), p2string(self.p,fmt='%.5f'))






class SPM1Di(_SPMiParent, SPM1D):
	
	@property
	def clusters(self):
		return self.iresults.clusters
	@property
	def nClusters(self):
		return len( self.iresults.clusters )
	@property
	def p(self):
		msg = 'Use of "p" is deprecated. Use "p_cluster" to avoid this warning.'
		warnings.warn( msg , SPM1DDeprecationWarning , stacklevel=2 )
		return self.p_cluster
	@property
	def p_cluster(self):
		return self.iresults.p_cluster
	@property
	def p_max(self):
		return self.iresults.p_max
	@property
	def p_set(self):
		return self.iresults.p_set


		# if self.isregress:
		# 	self.r              = spm.r
		# if self.isanova:
		# 	self.effect_label   = spm.effect_label
		# 	self.effect_label_s = spm.effect_label_s
		# 	self.ss             = spm.ss
		# 	self.ms             = spm.ms
		# self._add_extras( results.extras )


		
	def _repr_summ(self):
		return '{:<5} z={:<18} df={:<16} h0reject={}\n'.format(self.name_s,  self._repr_teststat_short(), dflist2str(self.df), self.h0reject)


	def plot(self, **kwdargs):
		from ... plot import plot_spmi
		return plot_spmi(self, **kwdargs)

	def plot_p_values(self, **kwdargs):
		from ... plot import plot_spmi_p_values
		plot_spmi_p_values(self, **kwdargs)
	
	def plot_threshold_label(self, **kwdargs):
		from ... plot import plot_spmi_threshold_label
		return plot_spmi_threshold_label(self, **kwdargs)




