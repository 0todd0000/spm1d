
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
from ... util import array2shortstr, arraytuple2str, dflist2str, float2string, largeint2str, resels2str, p2string, plist2string, DisplayParams
from ... util import p2string_none, plist2string_none, float2string_none
from ... cfg import SPM1DDeprecationWarning

# p2string_none     = lambda x: p2string(x, allow_none=True, fmt='%.3f')
# plist2string_none = lambda x: plist2string(x, allow_none=True, fmt='%.3f')
# float2string_none = lambda x: float2string(x, allow_none=True, fmt='%.5f')



class SPM1Di(_SPMiParent, SPM1D):
	
	isinference = True


	# def __init__(self, spm, iresults, df_adjusted):
	# 	self._args           = spm._args            # arguments for spm1d.stats function
	# 	self._kwargs         = spm._kwargs          # keyword arguments for spm1d.stats function
	# 	self._iargs          = None                 # arguments for inference
	# 	self._ikwargs        = None                 # keyword arguments for inference
	# 	self.spm             = spm
	# 	self.iresults        = iresults
	# 	self.df_adjusted     = df_adjusted
	# 	# self.extras          = []


	def _set_inference_results(self, iresults, df_adjusted):
		# self._args           = spm._args            # arguments for spm1d.stats function
		# self._kwargs         = spm._kwargs          # keyword arguments for spm1d.stats function
		self._iargs          = None                 # arguments for inference
		self._ikwargs        = None                 # keyword arguments for inference
		# self.spm             = spm
		self.iresults        = iresults
		self.df_adjusted     = df_adjusted
		# self.extras          = []



	# @property
	# def contrast(self):
	# 	return self.spm.contrast
	# @property
	# def design(self):
	# 	return self.spm.design
	# @property
	# def fit(self):
	# 	return self.spm.fit
	# @property
	# def results(self):
	# 	return self.spm.results
	# @property
	# def roi(self):
	# 	return self.spm.roi
	#
	#
	# @property
	# def fwhm(self):
	# 	return self.spm.fwhm
	# @property
	# def resels(self):
	# 	return self.spm.resels


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
	# @property
	# def p(self):
	# 	return self.p_cluster
	# @property
	# def p_cluster(self):
	# 	return [c.p  for c in self.iresults.clusters]
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

		
	# def __repr__(self):
	# 	s        = super().__repr__()
	# 	s       += 'Inference:\n'
	# 	s       += '   SPM.method          :  %s\n'       %self.method
	# 	s       += '   SPM.isparametric    :  %s\n'       %self.isparametric
	# 	if not self.isparametric:
	# 		s   += '   SPM.nperm_possible  :  %d\n'       %self.nperm_possible
	# 		s   += '   SPM.nperm_actual    :  %d\n'       %self.nperm_actual
	# 	s       += '   SPM.alpha           :  %.3f\n'     %self.alpha
	# 	s       += '   SPM.zc              :  %s\n'       %self._zcstr
	# 	s       += '   SPM.h0reject        :  %s\n'       %self.h0reject
	# 	s       += '   SPM.p_max           :  %s\n'       %p2string(self.p_max)
	# 	s       += '   SPM.p_set           :  %s\n'       %p2string(self.p_set, allow_none=True)
	# 	s       += '   SPM.p_cluster       :  (%s)\n'     %plist2string(self.p_cluster)
	# 	s       += '   SPM.clusters        :  %s\n'       %self.clusters.asshortstr()
	# 	return s
	
	
	def __repr__(self):
		s0      = super().__repr__()
		s1      = self.iresults.__repr__()
		return s0 + s1
		# dp      = DisplayParams( self )
		# dp.add_header( 'Inference:' )
		# dp.add( 'method' )
		# dp.add( 'isparametric' )
		# dp.add( 'alpha' )
		# if self.STAT == 'T':
		# 	dp.add( 'dirn' )
		# dp.add( 'zc', float2string_none )
		# dp.add( 'h0reject' )
		# dp.add( 'p_max', p2string_none )
		# dp.add( 'p_set', p2string_none )
		# dp.add( 'p_cluster', plist2string_none )
		# if len( self.extras ) > 0:
		# 	dp.add_header( 'extras:' )
		# 	for k,v in self.extras.items():
		# 		if k=='nperm_possible':
		# 			dp.add(k, largeint2str)
		# 		else:
		# 			dp.add(k)
		# return s0 + dp.asstr()

	# def __repr__(self):
	# 	dp      = DisplayParams( self )
	# 	dp.add_header( self._class_str )
	# 	dp.add( 'testname' )
	# 	dp.add( 'STAT' )
	# 	if self.isanova:
	# 		dp.add( 'name' )
	# 		dp.add( 'ss' , array2shortstr )
	# 		dp.add( 'ms' , array2shortstr )
	# 	dp.add( 'z', fmt=array2shortstr )
	# 	if self.isregress:
	# 		dp.add('r', fmt=array2shortstr )
	# 	dp.add( 'df', fmt=dflist2str )
	# 	dp.add_header( 'Smoothness estimates:' )
	# 	dp.add( 'fwhm', fmt='%.3f' )
	# 	dp.add( 'lkc', fmt='%.3f' )
	# 	dp.add( 'resels', fmt=resels2str )
	#
	#
	# 	dp.add_header( 'Inference:' )
	# 	dp.add( 'method' )
	# 	dp.add( 'isparametric' )
	# 	dp.add( 'alpha' )
	# 	if self.STAT == 'T':
	# 		dp.add( 'dirn' )
	# 	dp.add( 'zc', float2string_none )
	# 	dp.add( 'h0reject' )
	# 	dp.add( 'p_max', p2string_none )
	# 	dp.add( 'p_set', p2string_none )
	# 	dp.add( 'p_cluster', plist2string_none )
	# 	if len( self.extras ) > 0:
	# 		dp.add_header( 'extras:' )
	# 		for k,v in self.extras.items():
	# 			if k=='nperm_possible':
	# 				dp.add(k, largeint2str)
	# 			else:
	# 				dp.add(k)
	#
	#
	#
	# 	return dp.asstr()


	# def __repr__(self):
	# 	dp      = DisplayParams( self )
	# 	dp.add_header( self._class_str )
	# 	dp.add( 'testname' )
	# 	dp.add( 'STAT' )
	# 	if self.isanova:
	# 		dp.add( 'effect_label' )
	# 		dp.add( 'ss' , array2shortstr )
	# 		dp.add( 'ms' , array2shortstr )
	# 	dp.add( 'z', fmt=array2shortstr )
	# 	if self.isregress:
	# 		dp.add('r', fmt=array2shortstr )
	# 	dp.add( 'df', fmt=dflist2str )
	#
	# 	dp.add_header( 'Smoothness estimates:' )
	# 	dp.add( 'fwhm', fmt='%.3f' )
	# 	dp.add( 'lkc', fmt='%.3f' )
	# 	dp.add( 'resels', fmt=resels2str )
	#
	# 	dp.add_header( 'Inference:' )
	# 	dp.add( 'method' )
	# 	dp.add( 'isparametric' )
	# 	dp.add( 'alpha' )
	# 	if self.STAT == 'T':
	# 		dp.add( 'dirn' )
	# 	dp.add( 'zc', float2string_none )
	# 	dp.add( 'h0reject' )
	# 	dp.add( 'p_max', p2string_none )
	# 	dp.add( 'p_set', p2string_none )
	# 	dp.add( 'p_cluster', plist2string_none )
	# 	if len( self.extras ) > 0:
	# 		dp.add_header( 'extras:' )
	# 		for k,v in self.extras.items():
	# 			if k=='nperm_possible':
	# 				dp.add(k, largeint2str)
	# 			else:
	# 				dp.add(k)
	# 	return dp.asstr()
	
	# @property
	# def h0reject(self):
	# 	zc       = self.zc
	# 	if self.dirn in (None,1):
	# 		h       = self.z.max() > zc
	# 	elif self.dirn==0:
	# 		zc0,zc1 = (-zc,zc) if self.isparametric else zc
	# 		h       = (self.z.min() < zc0) or (self.z.max() > zc1)
	# 	elif self.dirn==-1:
	# 		zc0     = -zc if self.isparametric else zc[0]
	# 		h       = self.z.min() < zc0
	# 	return h

	# @property
	# def h0reject(self):
	# 	zc       = self.zc
	# 	if zc is None:
	# 		return False
	# 	if self.dirn in (None,1):
	# 		h       = self.z.max() > zc
	# 	elif self.dirn==0:
	# 		h       = (self.z.min() < -zc) or (self.z.max() > zc)
	# 	elif self.dirn==-1:
	# 		h       = self.z.min() < -zc
	# 	return h
		
	@property
	def h0reject(self):
		return self.iresults.h0reject
		


		
	# # inference proprties:
	# self.method          = iresults.method
	# self.alpha           = iresults.alpha
	# self.zc              = iresults.zc
	# self.p               = iresults.p
	# self.dirn            = iresults.dirn
	# self._add_extras( iresults.extras )
	# self.df_adjusted     = df_adjusted
	#
		
		
	def _repr_summ(self):
		return '{:<5} z={:<18} df={:<16} h0reject={}\n'.format(self.name_s,  self._repr_teststat_short(), dflist2str(self.df), self.h0reject)


	# @property
	# def h0reject(self):
	# 	z,zc  = self.z, self.zc
	# 	if self.dirn==0:
	# 		h = (z.min() < -zc) or (z.max() > zc)
	# 	elif self.dirn==1:
	# 		h = z.max() > zc
	# 	elif self.dirn==-1:
	# 		h = z.min() < -zc
	# 	return h

	# @property
	# def h0reject(self):
	# 	zc       = self.zc
	# 	if (self.dirn is None) or (self.dirn==1):
	# 		h       = self.z.max() > zc
	# 	elif self.dirn==0:
	# 		zc0,zc1 = (-zc,zc) if self.isparametric else zc
	# 		h       = (self.z.min() < zc0) or (self.z.max() > zc1)
	# 	elif self.dirn==-1:
	# 		zc0     = -zc if self.isparametric else zc[0]
	# 		h       = self.z.min() < zc0
	# 	return h


	# @property
	# def p_cluster(self):
	# 	return [c.p for c in self.clusters]
	
	def plot(self, **kwdargs):
		from ... plot import plot_spmi
		return plot_spmi(self, **kwdargs)

	def plot_p_values(self, **kwdargs):
		from ... plot import plot_spmi_p_values
		plot_spmi_p_values(self, **kwdargs)
	
	def plot_threshold_label(self, **kwdargs):
		from ... plot import plot_spmi_threshold_label
		return plot_spmi_threshold_label(self, **kwdargs)






# class SPM1Di(_SPMiParent, SPM1D):
#
# 	isinference = True
#
#
# 	def __init__(self, spm, iresults, df_adjusted):
# 		self._args           = spm._args            # arguments for spm1d.stats function
# 		self._kwargs         = spm._kwargs          # keyword arguments for spm1d.stats function
# 		self._iargs          = None                 # arguments for inference
# 		self._ikwargs        = None                 # keyword arguments for inference
# 		self.spm             = spm
# 		self.iresults        = iresults
# 		self.df_adjusted     = df_adjusted
# 		# self.extras          = []
#
#
#
# 	@property
# 	def contrast(self):
# 		return self.spm.contrast
# 	@property
# 	def design(self):
# 		return self.spm.design
# 	@property
# 	def fit(self):
# 		return self.spm.fit
# 	@property
# 	def results(self):
# 		return self.spm.results
# 	@property
# 	def roi(self):
# 		return self.spm.roi
#
#
# 	@property
# 	def fwhm(self):
# 		return self.spm.fwhm
# 	@property
# 	def resels(self):
# 		return self.spm.resels
#
#
# 	# inference results properties
# 	@property
# 	def alpha(self):
# 		return self.iresults.alpha
# 	@property
# 	def dirn(self):
# 		return self.iresults.dirn
# 	@property
# 	def extras(self):
# 		return self.iresults.extras
# 	@property
# 	def method(self):
# 		return self.iresults.method
# 	@property
# 	def nClusters(self):
# 		return len( self.iresults.clusters )
# 	@property
# 	def p(self):
# 		msg = 'Use of "p" is deprecated. Use "p_cluster" to avoid this warning.'
# 		warnings.warn( msg , SPM1DDeprecationWarning , stacklevel=2 )
# 		return self.p_cluster
# 	# @property
# 	# def p(self):
# 	# 	return self.p_cluster
# 	@property
# 	def p_cluster(self):
# 		return [c.p  for c in self.iresults.clusters]
# 	@property
# 	def p_max(self):
# 		return self.iresults.p_max
# 	@property
# 	def p_set(self):
# 		return self.iresults.p_set
# 	@property
# 	def zc(self):
# 		return self.iresults.zc
#
#
# 		# if self.isregress:
# 		# 	self.r              = spm.r
# 		# if self.isanova:
# 		# 	self.effect_label   = spm.effect_label
# 		# 	self.effect_label_s = spm.effect_label_s
# 		# 	self.ss             = spm.ss
# 		# 	self.ms             = spm.ms
# 		# # inference results:
# 		# self.method          = results.method
# 		# self.alpha           = results.alpha
# 		# self.zc              = results.zc
# 		# self.p_max           = results.p_max
# 		# self.p_set           = results.p_set
# 		# self.clusters        = results.clusters
# 		# self.dirn            = results.dirn
# 		# self._add_extras( results.extras )
# 		# self.df_adjusted     = df_adjusted
#
#
# 	# def __repr__(self):
# 	# 	s        = super().__repr__()
# 	# 	s       += 'Inference:\n'
# 	# 	s       += '   SPM.method          :  %s\n'       %self.method
# 	# 	s       += '   SPM.isparametric    :  %s\n'       %self.isparametric
# 	# 	if not self.isparametric:
# 	# 		s   += '   SPM.nperm_possible  :  %d\n'       %self.nperm_possible
# 	# 		s   += '   SPM.nperm_actual    :  %d\n'       %self.nperm_actual
# 	# 	s       += '   SPM.alpha           :  %.3f\n'     %self.alpha
# 	# 	s       += '   SPM.zc              :  %s\n'       %self._zcstr
# 	# 	s       += '   SPM.h0reject        :  %s\n'       %self.h0reject
# 	# 	s       += '   SPM.p_max           :  %s\n'       %p2string(self.p_max)
# 	# 	s       += '   SPM.p_set           :  %s\n'       %p2string(self.p_set, allow_none=True)
# 	# 	s       += '   SPM.p_cluster       :  (%s)\n'     %plist2string(self.p_cluster)
# 	# 	s       += '   SPM.clusters        :  %s\n'       %self.clusters.asshortstr()
# 	# 	return s
#
#
# 	def __repr__(self):
# 		dp      = DisplayParams( self )
# 		dp.add_header( self._class_str )
# 		dp.add( 'testname' )
# 		dp.add( 'STAT' )
# 		if self.isanova:
# 			dp.add( 'effect_label' )
# 			dp.add( 'ss' , array2shortstr )
# 			dp.add( 'ms' , array2shortstr )
# 		dp.add( 'z', fmt=array2shortstr )
# 		if self.isregress:
# 			dp.add('r', fmt=array2shortstr )
# 		dp.add( 'df', fmt=dflist2str )
#
# 		dp.add_header( 'Smoothness estimates:' )
# 		dp.add( 'fwhm', fmt='%.3f' )
# 		dp.add( 'lkc', fmt='%.3f' )
# 		dp.add( 'resels', fmt=resels2str )
#
# 		dp.add_header( 'Inference:' )
# 		dp.add( 'method' )
# 		dp.add( 'isparametric' )
# 		dp.add( 'alpha' )
# 		if self.STAT == 'T':
# 			dp.add( 'dirn' )
# 		dp.add( 'zc', float2string_none )
# 		dp.add( 'h0reject' )
# 		dp.add( 'p_max', p2string_none )
# 		dp.add( 'p_set', p2string_none )
# 		dp.add( 'p_cluster', plist2string_none )
# 		if len( self.extras ) > 0:
# 			dp.add_header( 'extras:' )
# 			for k,v in self.extras.items():
# 				if k=='nperm_possible':
# 					dp.add(k, largeint2str)
# 				else:
# 					dp.add(k)
# 		return dp.asstr()
#
# 	# @property
# 	# def h0reject(self):
# 	# 	zc       = self.zc
# 	# 	if self.dirn in (None,1):
# 	# 		h       = self.z.max() > zc
# 	# 	elif self.dirn==0:
# 	# 		zc0,zc1 = (-zc,zc) if self.isparametric else zc
# 	# 		h       = (self.z.min() < zc0) or (self.z.max() > zc1)
# 	# 	elif self.dirn==-1:
# 	# 		zc0     = -zc if self.isparametric else zc[0]
# 	# 		h       = self.z.min() < zc0
# 	# 	return h
#
# 	@property
# 	def h0reject(self):
# 		zc       = self.zc
# 		if zc is None:
# 			return False
# 		if self.dirn in (None,1):
# 			h       = self.z.max() > zc
# 		elif self.dirn==0:
# 			h       = (self.z.min() < -zc) or (self.z.max() > zc)
# 		elif self.dirn==-1:
# 			h       = self.z.min() < -zc
# 		return h
#
#
# 	# # inference proprties:
# 	# self.method          = iresults.method
# 	# self.alpha           = iresults.alpha
# 	# self.zc              = iresults.zc
# 	# self.p               = iresults.p
# 	# self.dirn            = iresults.dirn
# 	# self._add_extras( iresults.extras )
# 	# self.df_adjusted     = df_adjusted
# 	#
#
#
# 	def _repr_summ(self):
# 		return '{:<5} z={:<18} df={:<9} h0reject={}\n'.format(self.effect_label_s,  self._repr_teststat_short(), dflist2str(self.df), self.h0reject)
#
#
# 	# @property
# 	# def h0reject(self):
# 	# 	z,zc  = self.z, self.zc
# 	# 	if self.dirn==0:
# 	# 		h = (z.min() < -zc) or (z.max() > zc)
# 	# 	elif self.dirn==1:
# 	# 		h = z.max() > zc
# 	# 	elif self.dirn==-1:
# 	# 		h = z.min() < -zc
# 	# 	return h
#
# 	# @property
# 	# def h0reject(self):
# 	# 	zc       = self.zc
# 	# 	if (self.dirn is None) or (self.dirn==1):
# 	# 		h       = self.z.max() > zc
# 	# 	elif self.dirn==0:
# 	# 		zc0,zc1 = (-zc,zc) if self.isparametric else zc
# 	# 		h       = (self.z.min() < zc0) or (self.z.max() > zc1)
# 	# 	elif self.dirn==-1:
# 	# 		zc0     = -zc if self.isparametric else zc[0]
# 	# 		h       = self.z.min() < zc0
# 	# 	return h
#
#
# 	# @property
# 	# def p_cluster(self):
# 	# 	return [c.p for c in self.clusters]
#
# 	def plot(self, **kwdargs):
# 		from ... plot import plot_spmi
# 		return plot_spmi(self, **kwdargs)
#
# 	def plot_p_values(self, **kwdargs):
# 		from ... plot import plot_spmi_p_values
# 		plot_spmi_p_values(self, **kwdargs)
#
# 	def plot_threshold_label(self, **kwdargs):
# 		from ... plot import plot_spmi_threshold_label
# 		return plot_spmi_threshold_label(self, **kwdargs)
#




# class SPM1Di(_SPMiParent, SPM1D):
#
# 	isinference = True
#
#
# 	def __init__(self, spm, results, df_adjusted):
# 		self.STAT            = spm.STAT             # test statistic (string): T, F, X2 or T2
# 		self.testname        = spm.testname         # spm1d.stats function name
# 		self._args           = spm._args            # arguments for spm1d.stats function
# 		self._kwargs         = spm._kwargs          # keyword arguments for spm1d.stats function
# 		self._iargs          = None                 # arguments for inference
# 		self._ikwargs        = None                 # keyword arguments for inference
# 		self.X               = spm.X                # design matrix
# 		self.beta            = spm.beta             # fitted parameters
# 		self.residuals       = spm.residuals        # model residuals
# 		self.sigma2          = spm.sigma2           # variance
# 		self.z               = spm.z                # test statistic value
# 		self.df              = spm.df               # degrees of freedom
# 		self.fwhm            = spm.fwhm
# 		self.resels          = spm.resels
# 		self.roi             = spm.roi
# 		if self.isregress:
# 			self.r              = spm.r
# 		if self.isanova:
# 			self.effect_label   = spm.effect_label
# 			self.effect_label_s = spm.effect_label_s
# 			self.ss             = spm.ss
# 			self.ms             = spm.ms
# 		# inference results:
# 		self.method          = results.method
# 		self.alpha           = results.alpha
# 		self.zc              = results.zc
# 		self.p_max           = results.p_max
# 		self.p_set           = results.p_set
# 		self.clusters        = results.clusters
# 		self.dirn            = results.dirn
# 		self._add_extras( results.extras )
# 		self.df_adjusted     = df_adjusted
#
#
# 	# def __repr__(self):
# 	# 	s        = super().__repr__()
# 	# 	s       += 'Inference:\n'
# 	# 	s       += '   SPM.method          :  %s\n'       %self.method
# 	# 	s       += '   SPM.isparametric    :  %s\n'       %self.isparametric
# 	# 	if not self.isparametric:
# 	# 		s   += '   SPM.nperm_possible  :  %d\n'       %self.nperm_possible
# 	# 		s   += '   SPM.nperm_actual    :  %d\n'       %self.nperm_actual
# 	# 	s       += '   SPM.alpha           :  %.3f\n'     %self.alpha
# 	# 	s       += '   SPM.zc              :  %s\n'       %self._zcstr
# 	# 	s       += '   SPM.h0reject        :  %s\n'       %self.h0reject
# 	# 	s       += '   SPM.p_max           :  %s\n'       %p2string(self.p_max)
# 	# 	s       += '   SPM.p_set           :  %s\n'       %p2string(self.p_set, allow_none=True)
# 	# 	s       += '   SPM.p_cluster       :  (%s)\n'     %plist2string(self.p_cluster)
# 	# 	s       += '   SPM.clusters        :  %s\n'       %self.clusters.asshortstr()
# 	# 	return s
#
#
# 	def __repr__(self):
# 		dp      = DisplayParams( self )
# 		dp.add_header( self._class_str )
# 		dp.add( 'testname' )
# 		dp.add( 'STAT' )
# 		if self.isanova:
# 			dp.add( 'effect_label' )
# 			dp.add( 'ss' , arraytuple2str )
# 			dp.add( 'ms' , arraytuple2str )
# 		dp.add( 'z', fmt=array2shortstr )
# 		if self.isregress:
# 			dp.add('r', fmt=array2shortstr )
# 		dp.add( 'df', fmt=dflist2str )
#
# 		dp.add_header( 'Smoothness estimates:' )
# 		dp.add( 'fwhm', fmt='%.3f' )
# 		dp.add( 'lkc', fmt='%.3f' )
# 		dp.add( 'resels', fmt=resels2str )
#
# 		dp.add_header( 'Inference:' )
# 		dp.add( 'method' )
# 		dp.add( 'isparametric' )
# 		dp.add( 'alpha' )
# 		dp.add( 'dirn' )
# 		dp.add( 'zc', float2string_none )
# 		dp.add( 'h0reject' )
# 		dp.add( 'p_max', p2string_none )
# 		dp.add( 'p_set', p2string_none )
# 		dp.add( 'p_cluster', plist2string_none )
# 		if len( self.extras ) > 0:
# 			dp.add_header( 'extras:' )
# 			for k,v in self.extras.items():
# 				if k=='nperm_possible':
# 					dp.add(k, largeint2str)
# 				else:
# 					dp.add(k)
# 		return dp.asstr()
#
# 	# @property
# 	# def h0reject(self):
# 	# 	zc       = self.zc
# 	# 	if self.dirn in (None,1):
# 	# 		h       = self.z.max() > zc
# 	# 	elif self.dirn==0:
# 	# 		zc0,zc1 = (-zc,zc) if self.isparametric else zc
# 	# 		h       = (self.z.min() < zc0) or (self.z.max() > zc1)
# 	# 	elif self.dirn==-1:
# 	# 		zc0     = -zc if self.isparametric else zc[0]
# 	# 		h       = self.z.min() < zc0
# 	# 	return h
#
# 	@property
# 	def h0reject(self):
# 		zc       = self.zc
# 		if zc is None:
# 			return False
# 		if self.dirn in (None,1):
# 			h       = self.z.max() > zc
# 		elif self.dirn==0:
# 			h       = (self.z.min() < -zc) or (self.z.max() > zc)
# 		elif self.dirn==-1:
# 			h       = self.z.min() < -zc
# 		return h
#
# 	def _repr_summ(self):
# 		return '{:<5} z={:<18} df={:<9} h0reject={}\n'.format(self.effect_label_s,  self._repr_teststat_short(), dflist2str(self.df), self.h0reject)
#
#
# 	# @property
# 	# def h0reject(self):
# 	# 	z,zc  = self.z, self.zc
# 	# 	if self.dirn==0:
# 	# 		h = (z.min() < -zc) or (z.max() > zc)
# 	# 	elif self.dirn==1:
# 	# 		h = z.max() > zc
# 	# 	elif self.dirn==-1:
# 	# 		h = z.min() < -zc
# 	# 	return h
#
# 	# @property
# 	# def h0reject(self):
# 	# 	zc       = self.zc
# 	# 	if (self.dirn is None) or (self.dirn==1):
# 	# 		h       = self.z.max() > zc
# 	# 	elif self.dirn==0:
# 	# 		zc0,zc1 = (-zc,zc) if self.isparametric else zc
# 	# 		h       = (self.z.min() < zc0) or (self.z.max() > zc1)
# 	# 	elif self.dirn==-1:
# 	# 		zc0     = -zc if self.isparametric else zc[0]
# 	# 		h       = self.z.min() < zc0
# 	# 	return h
#
# 	@property
# 	def nClusters(self):
# 		return len( self.clusters )
#
# 	@property
# 	def p(self):
# 		msg = 'Use of "p" is deprecated. Use "p_cluster" to avoid this warning.'
# 		warnings.warn( msg , SPM1DDeprecationWarning , stacklevel=2 )
# 		return self.p_cluster
#
# 	@property
# 	def p_cluster(self):
# 		return [c.p for c in self.clusters]
#
# 	def plot(self, **kwdargs):
# 		from ... plot import plot_spmi
# 		return plot_spmi(self, **kwdargs)
#
# 	def plot_p_values(self, **kwdargs):
# 		from ... plot import plot_spmi_p_values
# 		plot_spmi_p_values(self, **kwdargs)
#
# 	def plot_threshold_label(self, **kwdargs):
# 		from ... plot import plot_spmi_threshold_label
# 		return plot_spmi_threshold_label(self, **kwdargs)
#
#
# # class SPM1Di_F(_SPMF, _SPM1Dinference):
# # 	'''An SPM{F} inference continuum.'''
# # 	def _repr_summ(self):
# # 		return '{:<5} z={:<18} df={:<9} h0reject={}\n'.format(self.effect_short,  self._repr_teststat_short(), dflist2str(self.df), self.h0reject)
#
#


