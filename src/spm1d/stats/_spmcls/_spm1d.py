
'''
SPM1D class definition
'''

# Copyright (C) 2023  Todd Pataky

from copy import deepcopy
import numpy as np
from . _base import _SPMParent
from ... import prob
# from ... plot import plot_spm, plot_spm_design
# from ... plot import plot_spmi, plot_spmi_p_values, plot_spmi_threshold_label
from ... util import array2shortstr, arraytuple2str, dflist2str, resels2str, DisplayParams




class SPM1D(_SPMParent):
	dim                     = 1

	def __init__(self, design, model, fit, teststat, roi=None):
		self._args          = None            # arguments for spm1d.stats function
		self._kwargs        = None            # keyword arguments for spm1d.stats function
		self.design         = design
		self.model          = model
		self.fit            = fit
		self.teststat       = teststat
		# self.results        = results
		self.sm             = None  # smoothness estimates
		self.roi            = roi
		self._estimate_smoothness()
		
		
		# # self.testname       = None            # hypothesis test name (set using set_testname method)
		# self.design         = design
		# self.contrast       = contrast
		# self.fit            = fit
		# self.results        = results
		# self.roi            = roi
		# self.sm             = None  # smoothness estimates
		# # self.fwhm           = None
		# # self.resels         = None
		# self._estimate_smoothness()


	# def __init__(self, STAT, z, df, beta=None, residuals=None, sigma2=None, X=None, fwhm=None, resels=None, roi=None):
	# 	self.STAT           = STAT             # test statistic ("T" or "F")
	# 	self.testname       = None             # hypothesis test name (set using set_testname method)
	# 	self.X              = X                # design matrix
	# 	self.beta           = beta             # fitted parameters
	# 	self.residuals      = residuals        # residuals (same size as original data)
	# 	self.sigma2         = sigma2           # variance
	# 	self.z              = z                # test statistic
	# 	self.df             = df               # degrees of freedom
	# 	self.fwhm           = fwhm             # smoothness
	# 	self.resels         = resels           # resel counts
	# 	self.roi            = roi              # region of interest

	# def __eq__(self, other):
	# 	eq = True
	# 	for k,v in self.__dict__.items():
	# 		if not k.startswith('_'):
	# 			v1 = getattr(other, k)
	# 			if isinstance(v, (str,int,float,tuple,list)):
	# 				eq = v==v1
	# 			elif isinstance(v, np.ndarray):
	# 				eq = np.all( np.isclose(v, v1, rtol=1e-5, atol=1e-9, equal_nan=True ) )
	# 			elif v is None:
	# 				eq = v1 is None
	# 			else:
	# 				raise ValueError( f'Unable to hash type: {type(v)}' )
	# 			if not eq:
	# 				break
	# 	return eq
	
	
	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_header( self._class_str )
		dp.add( 'testname' )
		dp.add( 'STAT' )
		if self.isanova:
			dp.add( 'name' )
			dp.add( 'ss' , array2shortstr )
			dp.add( 'ms' , array2shortstr )
		dp.add( 'z', fmt=array2shortstr )
		if self.isregress:
			dp.add('r', fmt=array2shortstr )
		dp.add( 'df', fmt=dflist2str )
		dp.add_header( 'Smoothness estimates:' )
		dp.add( 'fwhm', fmt='%.3f' )
		dp.add( 'lkc', fmt='%.3f' )
		dp.add( 'resels', fmt=resels2str )
		return dp.asstr()

	
	@property
	def STAT(self):
		return self.teststat.STAT
	@property
	def contrast(self):
		return self.design.contrasts[ self.teststat.ind ]
	@property
	def df(self):
		return self.teststat.df
	# @property
	# def effect_name(self):
	# 	return self.design.contrasts[ self.teststat.ind ].name
	@property
	def ms(self):
		return self.teststat.ms if self.isanova else None
	@property
	def name(self):
		return self.contrast.name
	@property
	def name_s(self):
		return self.contrast.name_s
	@property
	def name_short(self):
		return self.contrast.name_s
	@property
	def residuals(self):
		return self.fit.e
	@property
	def ss(self):
		return self.teststat.ss if self.isanova else None
	@property
	def testname(self):
		return self.design.testname
	@property
	def z(self):
		return self.teststat.z


	# smoothness parameters:
	@property
	def fwhm(self):
		return self.sm.fwhm
	@property
	def lkc(self):
		return self.sm.lkc
	@property
	def resels(self):
		return self.sm.resels


	# @property
	# def R(self):
	#     return self.residuals
	# @property
	# def nNodes(self):
	# 	return self.Q
	@property
	def Q(self):
		return self.z.size
	@property
	def Qmasked(self):
		return self.z.size if (self.roi is None) else self.z.count()
	@property
	def lkc(self):
		from ... geom.smoothness import fwhm2lkc
		return fwhm2lkc( self.fwhm, self.Q )
	# @property
	# def fwhm(self):
	# 	return self.fit.fwhm
	# @property
	# def resels(self):
	# 	return self.fit.resels
	
	
	def _repr_corrcoeff(self):
		return '(1x%d) correlation coefficient field' %self.Q
	def _repr_teststat(self):
		return '(1x%d) test stat field' %self.Q
	def _repr_teststat_short(self):
		return '(1x%d) array' %self.Q
	def _repr_summ(self):  # for F lists
		return '{:<5} z = {:<18} df = {}\n'.format(self.name_s,  self._repr_teststat_short(), dflist2str(self.df))


	# def _build_spmi(self, results, alpha, dirn=0, df_adjusted=None):
	# 	from . _spm1di import SPM1Di
	# 	spmi             = SPM1Di( self, results.method, alpha, results.zc, results.p, df_adjusted, dirn )
	#
	# 	spmi             = deepcopy( self )
	# 	spmi.__class__   = SPM1Di
	# 	spmi.df_adjusted = df_adjusted
	# 	spmi.method      = results.method
	# 	spmi.alpha       = alpha
	# 	spmi.zc          = results.zc
	# 	spmi.p_set       = results.p_set
	# 	spmi.p_max       = results.p_max
	# 	spmi.clusters    = results.clusters
	# 	if self.STAT=='T':
	# 		spmi.dirn     = dirn
	# 		# spmi.dirn   = parser.kwargs['dirn']
	# 	if results.method=='perm':
	# 		spmi.nperm    = results.nperm
	# 		spmi.permuter = results.permuter
	# 	return spmi


	# def _build_spmi(self, results, df_adjusted=None):
	# 	from . _spm1di import SPM1Di
	# 	# spmi             = deepcopy( self )
	# 	# spmi.__class__   = SPM0Di
	# 	spmi             = SPM1Di(self, results, df_adjusted)
	# 	# if results.method=='perm':
	# 	# 	spmi.nperm    = results.nperm
	# 	# 	spmi.permuter = results.permuter
	# 	return spmi

	# def _build_spmi(self, results, alpha, dirn=0, df_adjusted=None):
	# 	from . _spm1di import SPM1Di
	# 	spmi             = deepcopy( self )
	# 	spmi.__class__   = SPM1Di
	# 	spmi.df_adjusted = df_adjusted
	# 	spmi.method      = results.method
	# 	spmi.alpha       = alpha
	# 	spmi.zc          = results.zc
	# 	spmi.p_set       = results.p_set
	# 	spmi.p_max       = results.p_max
	# 	spmi.clusters    = results.clusters
	# 	if self.STAT=='T':
	# 		spmi.dirn     = dirn
	# 		# spmi.dirn   = parser.kwargs['dirn']
	# 	if results.method=='perm':
	# 		spmi.nperm    = results.nperm
	# 		spmi.permuter = results.permuter
	# 	return spmi

	
	# def _estimate_smoothness(self):
	# 	from ... geom import estimate_fwhm, resel_counts
	# 	self.fwhm   = estimate_fwhm( self.residuals, roi=self.roi )
	# 	self.resels = resel_counts(self.residuals, self.fwhm, element_based=False, roi=self.roi)
		

	def _estimate_smoothness(self):
		from ... geom.smoothness import SmoothnessEstimates
		self.sm     = SmoothnessEstimates( self.residuals, method='rft1d', roi=None )
	
	
	def inference(self, alpha, method='rft', **kwargs):
		# from . _argparsers import InferenceArgumentParser1D
		# parser   = InferenceArgumentParser1D(self.STAT, self.testname, method)
		# kwargs   = parser.parse( alpha, **kwargs )
		
		if method == 'rft':
			iresults = prob.rft(self.STAT, self.z, self.df, self.fwhm, self.resels, alpha=alpha, **kwargs)
			# results = self.inference_rft(alpha, **kwargs)
			
			# spmi = self.inference_rft(alpha, **parser.kwargs)
		elif method == 'perm':
			# print( len(self._args) )
			# nperm = kwargs['nperm']
			# results = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, dirn=dirn)
			iresults = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, dim=1, **kwargs)
			
			# return self._build_spmi(results, alpha, dirn=dirn)
			#
			# spmi = self.inference_perm(alpha, **parser.kwargs)
		
		elif method == 'fdr':
			iresults = prob.fdr(self.STAT, self.z, self.df, alpha=alpha, **kwargs)
		
		else:
			raise ValueError( f'Unknown inference method: {method}. Must be one of: ["rft", "perm", "fdr"]' )
		
		# spmi       = self._build_spmi(alpha, zstar, clusters, p_set, two_tailed)    #assemble SPMi object
		# return spmi
		
		dfa = self.df
		# dirn = kwargs['dirn'] if 'dirn' in kwargs else None
		
		
		# spmi = self._build_spmi(results, df_adjusted=dfa)
		
		# from . _spm1di import SPM1Di
		# spmi = SPM1Di(self, iresults, dfa)
		
		
		from . _spm1di import SPM1Di
		from copy import deepcopy
		
		spmi = deepcopy( self )
		spmi.__class__ = SPM1Di
		spmi._set_inference_results( iresults, dfa )
		
		# spmi._iargs   = (alpha,)
		# spmi._ikwargs = dict(method=method)
		# spmi._ikwargs.update( **kwargs )
		
		
		return spmi
		
		
	def normality_test(self, alpha=0.05):
		from .. normality.k2 import residuals
		return residuals( self.residuals ).inference( alpha )
		
			
		


	def plot(self, **kwdargs):
		from ... plot import plot_spm
		return plot_spm(self, **kwdargs)
		
	def plot_design(self, **kwdargs):
		from ... plot import plot_spm_design
		plot_spm_design(self, **kwdargs)
		
	def toarray(self):
		return self.z.copy()







# class SPM1D(_SPMParent):
# 	dim                     = 1
#
# 	def __init__(self, results, design, fit, contrast, roi=None):
# 		self._args          = None            # arguments for spm1d.stats function
# 		self._kwargs        = None            # keyword arguments for spm1d.stats function
# 		# self.testname       = None            # hypothesis test name (set using set_testname method)
# 		self.design         = design
# 		self.contrast       = contrast
# 		self.fit            = fit
# 		self.results        = results
# 		self.roi            = roi
# 		self.sm             = None  # smoothness estimates
# 		# self.fwhm           = None
# 		# self.resels         = None
# 		self._estimate_smoothness()
#
#
# 	# def __init__(self, STAT, z, df, beta=None, residuals=None, sigma2=None, X=None, fwhm=None, resels=None, roi=None):
# 	# 	self.STAT           = STAT             # test statistic ("T" or "F")
# 	# 	self.testname       = None             # hypothesis test name (set using set_testname method)
# 	# 	self.X              = X                # design matrix
# 	# 	self.beta           = beta             # fitted parameters
# 	# 	self.residuals      = residuals        # residuals (same size as original data)
# 	# 	self.sigma2         = sigma2           # variance
# 	# 	self.z              = z                # test statistic
# 	# 	self.df             = df               # degrees of freedom
# 	# 	self.fwhm           = fwhm             # smoothness
# 	# 	self.resels         = resels           # resel counts
# 	# 	self.roi            = roi              # region of interest
#
# 	# def __eq__(self, other):
# 	# 	eq = True
# 	# 	for k,v in self.__dict__.items():
# 	# 		if not k.startswith('_'):
# 	# 			v1 = getattr(other, k)
# 	# 			if isinstance(v, (str,int,float,tuple,list)):
# 	# 				eq = v==v1
# 	# 			elif isinstance(v, np.ndarray):
# 	# 				eq = np.all( np.isclose(v, v1, rtol=1e-5, atol=1e-9, equal_nan=True ) )
# 	# 			elif v is None:
# 	# 				eq = v1 is None
# 	# 			else:
# 	# 				raise ValueError( f'Unable to hash type: {type(v)}' )
# 	# 			if not eq:
# 	# 				break
# 	# 	return eq
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
# 		dp.add_header( 'Smoothness estimates:' )
# 		dp.add( 'fwhm', fmt='%.3f' )
# 		dp.add( 'lkc', fmt='%.3f' )
# 		dp.add( 'resels', fmt=resels2str )
# 		return dp.asstr()
#
#
# 	@property
# 	def STAT(self):
# 		return self.results.STAT
# 	@property
# 	def df(self):
# 		return self.results.df
# 	@property
# 	def ms(self):
# 		return self.results.ms if self.isanova else None
# 	@property
# 	def name(self):
# 		return self.contrast.name
# 	@property
# 	def name_s(self):
# 		return self.contrast.name_s
# 	@property
# 	def name_short(self):
# 		return self.contrast.name_s
# 	@property
# 	def residuals(self):
# 		return self.fit.e
# 	@property
# 	def ss(self):
# 		return self.results.ss if self.isanova else None
# 	@property
# 	def testname(self):
# 		return self.design.testname
# 	@property
# 	def z(self):
# 		return self.results.z
#
#
# 	# smoothness parameters:
# 	@property
# 	def fwhm(self):
# 		return self.sm.fwhm
# 	@property
# 	def lkc(self):
# 		return self.sm.lkc
# 	@property
# 	def resels(self):
# 		return self.sm.resels
#
#
# 	# @property
# 	# def R(self):
# 	#     return self.residuals
# 	# @property
# 	# def nNodes(self):
# 	# 	return self.Q
# 	@property
# 	def Q(self):
# 		return self.z.size
# 	@property
# 	def Qmasked(self):
# 		return self.z.size if (self.roi is None) else self.z.count()
# 	@property
# 	def lkc(self):
# 		from ... geom.smoothness import fwhm2lkc
# 		return fwhm2lkc( self.fwhm, self.Q )
# 	# @property
# 	# def fwhm(self):
# 	# 	return self.fit.fwhm
# 	# @property
# 	# def resels(self):
# 	# 	return self.fit.resels
#
#
# 	def _repr_corrcoeff(self):
# 		return '(1x%d) correlation coefficient field' %self.Q
# 	def _repr_teststat(self):
# 		return '(1x%d) test stat field' %self.Q
# 	def _repr_teststat_short(self):
# 		return '(1x%d) array' %self.Q
# 	def _repr_summ(self):  # for F lists
# 		return '{:<5} z = {:<18} df = {}\n'.format(self.effect_label_s,  self._repr_teststat_short(), dflist2str(self.df))
#
#
# 	# def _build_spmi(self, results, alpha, dirn=0, df_adjusted=None):
# 	# 	from . _spm1di import SPM1Di
# 	# 	spmi             = SPM1Di( self, results.method, alpha, results.zc, results.p, df_adjusted, dirn )
# 	#
# 	# 	spmi             = deepcopy( self )
# 	# 	spmi.__class__   = SPM1Di
# 	# 	spmi.df_adjusted = df_adjusted
# 	# 	spmi.method      = results.method
# 	# 	spmi.alpha       = alpha
# 	# 	spmi.zc          = results.zc
# 	# 	spmi.p_set       = results.p_set
# 	# 	spmi.p_max       = results.p_max
# 	# 	spmi.clusters    = results.clusters
# 	# 	if self.STAT=='T':
# 	# 		spmi.dirn     = dirn
# 	# 		# spmi.dirn   = parser.kwargs['dirn']
# 	# 	if results.method=='perm':
# 	# 		spmi.nperm    = results.nperm
# 	# 		spmi.permuter = results.permuter
# 	# 	return spmi
#
#
# 	# def _build_spmi(self, results, df_adjusted=None):
# 	# 	from . _spm1di import SPM1Di
# 	# 	# spmi             = deepcopy( self )
# 	# 	# spmi.__class__   = SPM0Di
# 	# 	spmi             = SPM1Di(self, results, df_adjusted)
# 	# 	# if results.method=='perm':
# 	# 	# 	spmi.nperm    = results.nperm
# 	# 	# 	spmi.permuter = results.permuter
# 	# 	return spmi
#
# 	# def _build_spmi(self, results, alpha, dirn=0, df_adjusted=None):
# 	# 	from . _spm1di import SPM1Di
# 	# 	spmi             = deepcopy( self )
# 	# 	spmi.__class__   = SPM1Di
# 	# 	spmi.df_adjusted = df_adjusted
# 	# 	spmi.method      = results.method
# 	# 	spmi.alpha       = alpha
# 	# 	spmi.zc          = results.zc
# 	# 	spmi.p_set       = results.p_set
# 	# 	spmi.p_max       = results.p_max
# 	# 	spmi.clusters    = results.clusters
# 	# 	if self.STAT=='T':
# 	# 		spmi.dirn     = dirn
# 	# 		# spmi.dirn   = parser.kwargs['dirn']
# 	# 	if results.method=='perm':
# 	# 		spmi.nperm    = results.nperm
# 	# 		spmi.permuter = results.permuter
# 	# 	return spmi
#
#
# 	# def _estimate_smoothness(self):
# 	# 	from ... geom import estimate_fwhm, resel_counts
# 	# 	self.fwhm   = estimate_fwhm( self.residuals, roi=self.roi )
# 	# 	self.resels = resel_counts(self.residuals, self.fwhm, element_based=False, roi=self.roi)
#
#
# 	def _estimate_smoothness(self):
# 		from ... geom.smoothness import SmoothnessEstimates
# 		self.sm     = SmoothnessEstimates( self.residuals, method='rft1d', roi=None )
#
#
# 	def inference(self, alpha, method='rft', **kwargs):
# 		# from . _argparsers import InferenceArgumentParser1D
# 		# parser   = InferenceArgumentParser1D(self.STAT, self.testname, method)
# 		# kwargs   = parser.parse( alpha, **kwargs )
#
# 		if method == 'rft':
# 			iresults = prob.rft(self.STAT, self.z, self.df, self.fwhm, self.resels, alpha=alpha, **kwargs)
# 			# results = self.inference_rft(alpha, **kwargs)
#
# 			# spmi = self.inference_rft(alpha, **parser.kwargs)
# 		elif method == 'perm':
# 			# print( len(self._args) )
# 			# nperm = kwargs['nperm']
# 			# results = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, dirn=dirn)
# 			iresults = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, dim=1, **kwargs)
#
# 			# return self._build_spmi(results, alpha, dirn=dirn)
# 			#
# 			# spmi = self.inference_perm(alpha, **parser.kwargs)
#
# 		elif method == 'fdr':
# 			iresults = prob.fdr(self.STAT, self.z, self.df, alpha=alpha, **kwargs)
#
# 		else:
# 			raise ValueError( f'Unknown inference method: {method}. Must be one of: ["rft", "perm", "fdr"]' )
#
# 		# spmi       = self._build_spmi(alpha, zstar, clusters, p_set, two_tailed)    #assemble SPMi object
# 		# return spmi
#
# 		dfa = self.df
# 		# dirn = kwargs['dirn'] if 'dirn' in kwargs else None
#
#
# 		# spmi = self._build_spmi(results, df_adjusted=dfa)
#
# 		from . _spm1di import SPM1Di
# 		spmi = SPM1Di(self, iresults, dfa)
#
#
# 		# spmi._iargs   = (alpha,)
# 		# spmi._ikwargs = dict(method=method)
# 		# spmi._ikwargs.update( **kwargs )
#
#
# 		return( spmi )
#
#
# 	def normality_test(self, alpha=0.05):
# 		from .. normality.k2 import residuals
# 		return residuals( self.residuals ).inference( alpha )
#
#
#
#
#
# 	def plot(self, **kwdargs):
# 		from ... plot import plot_spm
# 		return plot_spm(self, **kwdargs)
#
# 	def plot_design(self, **kwdargs):
# 		from ... plot import plot_spm_design
# 		plot_spm_design(self, **kwdargs)
#
# 	def toarray(self):
# 		return self.z.copy()
#


# class SPM1D(_SPMParent):
#     dim                     = 1
#
#     def __init__(self, STAT, z, df, beta=None, residuals=None, sigma2=None, X=None, fwhm=None, resels=None, roi=None):
#         self.STAT           = STAT             # test statistic ("T" or "F")
#         self.testname       = None             # hypothesis test name (set using set_testname method)
#         self.X              = X                # design matrix
#         self.beta           = beta             # fitted parameters
#         self.residuals      = residuals        # residuals (same size as original data)
#         self.sigma2         = sigma2           # variance
#         self.z              = z                # test statistic
#         self.df             = df               # degrees of freedom
#         self.fwhm           = fwhm             # smoothness
#         self.resels         = resels           # resel counts
#         self.roi            = roi              # region of interest
#
#     # def __eq__(self, other):
#     #     eq = True
#     #     for k,v in self.__dict__.items():
#     #         if not k.startswith('_'):
#     #             v1 = getattr(other, k)
#     #             if isinstance(v, (str,int,float,tuple,list)):
#     #                 eq = v==v1
#     #             elif isinstance(v, np.ndarray):
#     #                 eq = np.all( np.isclose(v, v1, rtol=1e-5, atol=1e-9, equal_nan=True ) )
#     #             elif v is None:
#     #                 eq = v1 is None
#     #             else:
#     #                 raise ValueError( f'Unable to hash type: {type(v)}' )
#     #             if not eq:
#     #                 break
#     #     return eq
#
#
#     def __repr__(self):
#         dp      = DisplayParams( self )
#         dp.add_header( self._class_str )
#         dp.add( 'testname' )
#         dp.add( 'STAT' )
#         if self.isanova:
#             dp.add( 'effect_label' )
#             dp.add( 'ss' , arraytuple2str )
#             dp.add( 'ms' , arraytuple2str )
#         dp.add( 'z', fmt=array2shortstr )
#         if self.isregress:
#             dp.add('r', fmt=array2shortstr )
#         dp.add( 'df', fmt=dflist2str )
#         dp.add_header( 'Smoothness estimates:' )
#         dp.add( 'fwhm', fmt='%.3f' )
#         dp.add( 'lkc', fmt='%.3f' )
#         dp.add( 'resels', fmt=resels2str )
#         return dp.asstr()
#
#
#     @property
#     def R(self):
#         return self.residuals
#     @property
#     def nNodes(self):
#         return self.Q
#     @property
#     def Q(self):
#         return self.z.size
#     @property
#     def Qmasked(self):
#         return self.z.size if (self.roi is None) else self.z.count()
#     @property
#     def lkc(self):
#         from ... geom.smoothness import fwhm2lkc
#         return fwhm2lkc( self.fwhm, self.Q )
#
#
#     def _repr_corrcoeff(self):
#         return '(1x%d) correlation coefficient field' %self.Q
#     def _repr_teststat(self):
#         return '(1x%d) test stat field' %self.Q
#     def _repr_teststat_short(self):
#         return '(1x%d) array' %self.Q
#     def _repr_summ(self):  # for F lists
#         return '{:<5} z = {:<18} df = {}\n'.format(self.effect_label_s,  self._repr_teststat_short(), dflist2str(self.df))
#
#
#     # def _build_spmi(self, results, alpha, dirn=0, df_adjusted=None):
#     #     from . _spm1di import SPM1Di
#     #     spmi             = SPM1Di( self, results.method, alpha, results.zc, results.p, df_adjusted, dirn )
#     #
#     #     spmi             = deepcopy( self )
#     #     spmi.__class__   = SPM1Di
#     #     spmi.df_adjusted = df_adjusted
#     #     spmi.method      = results.method
#     #     spmi.alpha       = alpha
#     #     spmi.zc          = results.zc
#     #     spmi.p_set       = results.p_set
#     #     spmi.p_max       = results.p_max
#     #     spmi.clusters    = results.clusters
#     #     if self.STAT=='T':
#     #         spmi.dirn     = dirn
#     #         # spmi.dirn   = parser.kwargs['dirn']
#     #     if results.method=='perm':
#     #         spmi.nperm    = results.nperm
#     #         spmi.permuter = results.permuter
#     #     return spmi
#
#
#     def _build_spmi(self, results, df_adjusted=None):
#         from . _spm1di import SPM1Di
#         # spmi             = deepcopy( self )
#         # spmi.__class__   = SPM0Di
#         spmi             = SPM1Di(self, results, df_adjusted)
#         # if results.method=='perm':
#         #     spmi.nperm    = results.nperm
#         #     spmi.permuter = results.permuter
#         return spmi
#
#     # def _build_spmi(self, results, alpha, dirn=0, df_adjusted=None):
#     #     from . _spm1di import SPM1Di
#     #     spmi             = deepcopy( self )
#     #     spmi.__class__   = SPM1Di
#     #     spmi.df_adjusted = df_adjusted
#     #     spmi.method      = results.method
#     #     spmi.alpha       = alpha
#     #     spmi.zc          = results.zc
#     #     spmi.p_set       = results.p_set
#     #     spmi.p_max       = results.p_max
#     #     spmi.clusters    = results.clusters
#     #     if self.STAT=='T':
#     #         spmi.dirn     = dirn
#     #         # spmi.dirn   = parser.kwargs['dirn']
#     #     if results.method=='perm':
#     #         spmi.nperm    = results.nperm
#     #         spmi.permuter = results.permuter
#     #     return spmi
#
#
#     def inference(self, alpha, method='rft', **kwargs):
#         # from . _argparsers import InferenceArgumentParser1D
#         # parser   = InferenceArgumentParser1D(self.STAT, self.testname, method)
#         # kwargs   = parser.parse( alpha, **kwargs )
#
#         if method == 'rft':
#             results = prob.rft(self.STAT, self.z, self.df, self.fwhm, self.resels, alpha=alpha, **kwargs)
#             # results = self.inference_rft(alpha, **kwargs)
#
#             # spmi = self.inference_rft(alpha, **parser.kwargs)
#         elif method == 'perm':
#             # print( len(self._args) )
#             # nperm = kwargs['nperm']
#             # results = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, dirn=dirn)
#             results = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, dim=1, **kwargs)
#
#             # return self._build_spmi(results, alpha, dirn=dirn)
#             #
#             # spmi = self.inference_perm(alpha, **parser.kwargs)
#
#         elif method == 'fdr':
#             results = prob.fdr(self.STAT, self.z, self.df, alpha=alpha, **kwargs)
#
#         else:
#             raise ValueError( f'Unknown inference method: {method}. Must be one of: ["rft", "perm", "fdr"]' )
#
#         # spmi       = self._build_spmi(alpha, zstar, clusters, p_set, two_tailed)    #assemble SPMi object
#         # return spmi
#
#         dfa = self.df
#         # dirn = kwargs['dirn'] if 'dirn' in kwargs else None
#
#
#         spmi = self._build_spmi(results, df_adjusted=dfa)
#
#         spmi._iargs   = (alpha,)
#         spmi._ikwargs = dict(method=method)
#         spmi._ikwargs.update( **kwargs )
#
#
#         return( spmi )
#
#
#     def normality_test(self, alpha=0.05):
#         from .. normality.k2 import residuals
#         return residuals( self.residuals ).inference( alpha )
#
#
#
#
#
#     def plot(self, **kwdargs):
#         from ... plot import plot_spm
#         return plot_spm(self, **kwdargs)
#
#     def plot_design(self, **kwdargs):
#         from ... plot import plot_spm_design
#         plot_spm_design(self, **kwdargs)
#
#     def toarray(self):
#         return self.z.copy()





