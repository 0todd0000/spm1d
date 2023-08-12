
'''
SPMi (inference) module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for inference SPMs.
'''

# Copyright (C) 2022  Todd Pataky

import warnings
from . _base import _SPMiParent #, _SPMF
# from . _spm0d import SPM0D
from ... util import tuple2str, dflist2str, largeint2str, p2string, DisplayParams





class SPM0Di(_SPMiParent):
	
	isinference   = True
	
	def __init__(self, spm, iresults, df_adjusted):
		self._spm            = spm
		# self.STAT            = spm.STAT
		# self.testname        = spm.testname
		# self._args           = spm._args            # arguments for spm1d.stats function
		# self._kwargs         = spm._kwargs          # keyword arguments for spm1d.stats function
		self._iargs          = None                 # arguments for inference
		self._ikwargs        = None                 # keyword arguments for inference
		# self.design          = spm.design
		# self.fit             = spm.fit
		# self.contrast        = spm.contrast
		self.iresults        = iresults
		
		
		# self._args           = spm._args            # arguments for spm1d.stats function
		# self._kwargs         = spm._kwargs          # keyword arguments for spm1d.stats function
		# self.design          = spm.design
		# self.fit             = spm.fit
		# self.contrast        = spm.contrast
		# self.z               = spm.z                # test statistic value
		# self.df              = spm.df               # degrees of freedom
		
		
		# self.X               = spm.X                # design matrix
		# self.beta            = spm.beta             # fitted parameters
		# self.residuals       = spm.residuals        # model residuals
		# self.sigma2          = spm.sigma2           # variance
		# self.z               = spm.z                # test statistic value
		# self.df              = spm.df               # degrees of freedom
		if self.isregress:
			self.r              = spm.r
		# if self.isanova:
		# 	self.effect_label   = spm.effect_label
		# 	self.effect_label_s = spm.effect_label_s
		# 	self.ss             = spm.ss
		# 	self.ms             = spm.ms
		# inference results:
		self.method          = iresults.method
		self.alpha           = iresults.alpha
		self.zc              = iresults.zc
		self.p               = iresults.p
		self.dirn            = iresults.dirn
		self._add_extras( iresults.extras )
		self.df_adjusted     = df_adjusted
		
		# if self.STAT=='T':
		# 	self.dirn     = dirn
		# 	# spmi.dirn   = parser.kwargs['dirn']
	


	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_header( self._class_str )
		dp.add( 'testname' )
		dp.add( 'STAT' )
		# if self.isanova:
		# 	dp.add( 'effect_label' )
		# 	dp.add( 'ss' , tuple2str )
		# 	dp.add( 'ms' , tuple2str )
		dp.add( 'z', fmt='%.5f' )
		if self.isregress:
			dp.add('r', fmt='%.5f')
		dp.add( 'df', fmt=dflist2str )
		dp.add_header( 'Inference:' )
		dp.add( 'method' )
		dp.add( 'isparametric' )
		dp.add( 'alpha' )
		if self.STAT == 'T':
			dp.add( 'dirn' )
		dp.add( 'dirn' )
		dp.add( 'zc', fmt='%.5f' )
		dp.add( 'h0reject' )
		dp.add( 'p', fmt='%.5f' )
		if len( self.extras ) > 0:
			dp.add_header( 'extras:' )
			for k,v in self.extras.items():
				if not k.startswith('_'):
					if k=='nperm_possible':
						dp.add(k, largeint2str)
					else:
						dp.add(k)
		return dp.asstr()


	@property
	def _args(self):
		return self._spm._args
	@property
	def _kwargs(self):
		return self._spm._kwargs
	@property
	def STAT(self):
		return self._spm.STAT
	@property
	def contrast(self):
		return self._spm.contrast
	@property
	def design(self):
		return self._spm.design
	@property
	def df(self):
		return self._spm.df
	@property
	def fit(self):
		return self._spm.fit
	@property
	def ms(self):
		return self._spm.ms
	@property
	def ss(self):
		return self._spm.ss
	@property
	def testname(self):
		return self._spm.testname
	@property
	def z(self):
		return self._spm.z



		
	# self._args           = spm._args            # arguments for spm1d.stats function
	# self._kwargs         = spm._kwargs          # keyword arguments for spm1d.stats function
	# self.design          = spm.design
	# self.fit             = spm.fit
	# self.contrast        = spm.contrast
	# self.z               = spm.z                # test statistic value
	# self.df              = spm.df               # degrees of freedom
	

	@property
	def h0reject(self):
		z,zc  = self.z, self.zc
		if self.dirn==0:
			h = (z < -zc) or (z > zc)
		elif self.dirn in (None,1):
			h = z > zc
		elif self.dirn==-1:
			h = z < -zc
		return h

	@property
	def name_s(self):
		return self.contrast.name_s

	# def _repr_summ(self):
	# 	return '{:<5} F = {:<8} df = {:<9} p = {}\n'.format(self.effect_label_s,  '%.3f'%self.z, dflist2str(self.df), p2string(self.p,fmt='%.5f'))
	
	def _repr_summ(self, n=5):  # used only for ANOVA
		fmts = '{:<%s}   F = {:<8} df = {:<15} p = {}\n' %n
		return fmts.format( self.name_s,  '%.3f'%self.z, dflist2str(self.df), p2string(self.p,fmt='%.5f') )


	# @property
	# def eqvar_assumed(self):
	# 	return self.df_adjusted is None
	#
	# @property
	# def nperm_actual(self):
	# 	return self.nperm
	#
	# @property
	# def nperm_possible(self):
	# 	return self.permuter.nPermTotal
	#
	# @property
	# def two_tailed(self):
	# 	return self.dirn == 0




# class SPM0Di(_SPMiParent):
#
# 	isinference   = True
#
# 	def __init__(self, spm, results, df_adjusted):
# 		self.STAT            = spm.STAT
# 		self.testname        = spm.testname
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
# 		self.p               = results.p
# 		self.dirn            = results.dirn
# 		self._add_extras( results.extras )
# 		self.df_adjusted     = df_adjusted
#
# 		# if self.STAT=='T':
# 		# 	self.dirn     = dirn
# 		# 	# spmi.dirn   = parser.kwargs['dirn']
#
#
# 	# def __repr__(self):
# 	# 	s        = f'{self._class_str}\n'
# 	# 	s       += '   SPM.testname         :  %s\n'        %self.testname
# 	# 	if self.isanova:
# 	# 		s   += '   SPM.effect_label     :  %s\n'        %self.effect_label
# 	# 		s   += '   SPM.ms               :  %s\n'        %tuple2str(self.ms, '%.3f')
# 	# 		s   += '   SPM.ss               :  %s\n'        %tuple2str(self.ss, '%.3f')
# 	# 	s       += '   SPM.z                :  %.5f\n'      %self.z
# 	# 	s       += '   SPM.df               :  %s\n'        %dflist2str(self.df)
# 	# 	if self.isregress:
# 	# 		s   += '   SPM.r                :  %.5f\n'      %self.r
# 	# 	s         += 'Inference:\n'
# 	# 	s         += '   SPM.method            :  %s\n'      %self.method
# 	# 	s         += '   SPM.isparametric      :  %s\n'      %self.isparametric
# 	# 	if self.ismultigroup:
# 	# 		a    = self.eqvar_assumed
# 	# 		s     += '   SPM.eqvar_assumed     :  %s\n'      %a
# 	# 		if not a:
# 	# 			s += '   SPM.df_adjusted       :  %s\n'      %dflist2str(self.df_adjusted)
# 	#
# 	# 	# if not self.isparametric:
# 	# 	# 	s     += '   SPM.nperm_possible    :  %d\n'      %self.nperm_possible
# 	# 	# 	s     += '   SPM.nperm_actual      :  %d\n'      %self.nperm_actual
# 	# 	for k,v in self.extras.items():
# 	# 		s    += f'   SPM.{k}    :  {v}\n'
# 	#
# 	# 	s         += '   SPM.alpha             :  %.3f\n'    %self.alpha
# 	# 	if self.STAT == 'T':
# 	# 		s     += '   SPM.dirn              :  %s\n'      %self._dirn_str
# 	# 	s         += '   SPM.zc                :  %s\n'      %self._zcstr
# 	# 	s         += '   SPM.h0reject          :  %s\n'      %self.h0reject
# 	# 	s         += '   SPM.p                 :  %.5f\n'    %self.p
# 	# 	s         += '\n'
# 	# 	return s
#
# 	def __repr__(self):
# 		dp      = DisplayParams( self )
# 		dp.add_header( self._class_str )
# 		dp.add( 'testname' )
# 		dp.add( 'STAT' )
# 		if self.isanova:
# 			dp.add( 'effect_label' )
# 			dp.add( 'ss' , tuple2str )
# 			dp.add( 'ms' , tuple2str )
# 		dp.add( 'z', fmt='%.5f' )
# 		if self.isregress:
# 			dp.add('r', fmt='%.5f')
# 		dp.add( 'df', fmt=dflist2str )
# 		dp.add_header( 'Inference:' )
# 		dp.add( 'method' )
# 		dp.add( 'isparametric' )
# 		dp.add( 'alpha' )
# 		dp.add( 'dirn' )
# 		dp.add( 'zc', fmt='%.5f' )
# 		dp.add( 'h0reject' )
# 		dp.add( 'p', fmt='%.5f' )
# 		if len( self.extras ) > 0:
# 			dp.add_header( 'extras:' )
# 			for k,v in self.extras.items():
# 				if not k.startswith('_'):
# 					if k=='nperm_possible':
# 						dp.add(k, largeint2str)
# 					else:
# 						dp.add(k)
# 		return dp.asstr()
#
#
# 	# def _add_extras(self, extras):
# 	# 	for k,v in extras.items():
# 	# 		setattr(self, k, v)
#
# 	@property
# 	def h0reject(self):
# 		z,zc  = self.z, self.zc
# 		if self.dirn==0:
# 			h = (z < -zc) or (z > zc)
# 		elif self.dirn in (None,1):
# 			h = z > zc
# 		elif self.dirn==-1:
# 			h = z < -zc
# 		return h
#
# 	def _repr_summ(self):
# 		return '{:<5} F = {:<8} df = {:<9} p = {}\n'.format(self.effect_label_s,  '%.3f'%self.z, dflist2str(self.df), p2string(self.p,fmt='%.5f'))
#
#
#
# 	# @property
# 	# def eqvar_assumed(self):
# 	# 	return self.df_adjusted is None
# 	#
# 	# @property
# 	# def nperm_actual(self):
# 	# 	return self.nperm
# 	#
# 	# @property
# 	# def nperm_possible(self):
# 	# 	return self.permuter.nPermTotal
# 	#
# 	# @property
# 	# def two_tailed(self):
# 	# 	return self.dirn == 0






