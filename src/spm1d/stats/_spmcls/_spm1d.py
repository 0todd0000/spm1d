
'''
SPM1D class definition
'''

# Copyright (C) 2023  Todd Pataky

import numpy as np
from . _spm import _SPM
from ... util import array2shortstr, arraytuple2str, dflist2str, resels2str, DisplayParams




class SPM1D(_SPM):
	dim                     = 1


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

	
	
	def _estimate_smoothness(self):
		from ... geom.smoothness import SmoothnessEstimates
		self.sm     = SmoothnessEstimates( self.residuals, method='rft1d', roi=None )


	# repr private methods:
	def _repr_corrcoeff(self):
		return '(1x%d) correlation coefficient field' %self.Q
	def _repr_summ(self):  # for F lists
		return '{:<5} z = {:<18} df = {}\n'.format(self.name_s,  self._repr_teststat_short(), dflist2str(self.df))
	def _repr_teststat(self):
		return '(1x%d) test stat field' %self.Q
	def _repr_teststat_short(self):
		return '(1x%d) array' %self.Q
	
	
	

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
	# def nNodes(self):
	# 	return self.Q
	@property
	def Q(self):
		return self.z.size
	@property
	def Qmasked(self):
		return self.z.size if (self.roi is None) else self.z.count()
	
	



	
	
	def inference(self, alpha, method='rft', **kwargs):
		# from . _argparsers import InferenceArgumentParser1D
		# parser   = InferenceArgumentParser1D(self.STAT, self.testname, method)
		# kwargs   = parser.parse( alpha, **kwargs )
		
		from ... import prob
		
		if (self.STAT=='T') and ('dirn' not in kwargs):
			kwargs.update( {'dirn':0} )
		
		
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
		
		dfa  = self.df
		
		return self._iresults2spmi(iresults, dfa, alpha, method, kwargs)


		
	def plot(self, **kwdargs):
		from ... plot import plot_spm
		return plot_spm(self, **kwdargs)
		
	def plot_design(self, **kwdargs):
		from ... plot import plot_spm_design
		plot_spm_design(self, **kwdargs)
		
	def toarray(self):
		return self.z.copy()





