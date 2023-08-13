
'''
SPMi (inference) module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for inference SPMs.
'''

# Copyright (C) 2023  Todd Pataky

import warnings
from . _base import _SPMiParent
from . _spm1d import SPM1D
from ... cfg import SPM1DDeprecationWarning




class SPM1Di(_SPMiParent, SPM1D):
	
	isinference = True

	def __repr__(self):
		s0      = super().__repr__()
		s1      = self.iresults.__repr__()
		return s0 + s1
	
	
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
	@property
	def extras(self):
		return self.iresults.extras
	@property
	def h0reject(self):
		return self.iresults.h0reject
	@property
	def method(self):
		return self.iresults.method
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
	@property
	def zc(self):
		return self.iresults.zc


		# if self.isregress:
		# 	self.r              = spm.r
		# if self.isanova:
		# 	self.effect_label   = spm.effect_label
		# 	self.effect_label_s = spm.effect_label_s
		# 	self.ss             = spm.ss
		# 	self.ms             = spm.ms
		# # inference results:
		# self.method          = results.method
		# self.alpha           = results.alpha
		# self.zc              = results.zc
		# self.p_max           = results.p_max
		# self.p_set           = results.p_set
		# self.clusters        = results.clusters
		# self.dirn            = results.dirn
		# self._add_extras( results.extras )
		# self.df_adjusted     = df_adjusted

		
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






