
'''
SPM module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
'''

# Copyright (C) 2023  Todd Pataky

import warnings
import numpy as np
from ... cfg import SPM1DDeprecationWarning


class _SPM(object):
	dim            = 0
	isinference    = False
	isinlist       = False
	ismultigroup   = False
	testname       = None

	def __eq__(self, other):
		return self.isequal(other, verbose=False)
		# if type(self)!=type(other):
		# 	return False
		# eq = True
		# for k,v in self.__dict__.items():
		# 	# print('\n\n\n\n\n')
		# 	# print(k)
		# 	# print('\n\n\n\n\n')
		# 	if not k.startswith('_'):
		# 		v1 = getattr(other, k)
		# 		if v is None:
		# 			eq = v1 is None
		# 		elif isinstance(v, float) and np.isnan(v):
		# 			eq = np.isnan( v1 )
		# 		elif isinstance(v, tuple) and isinstance(v[0], np.ndarray):
		# 			for vv,vv1 in zip(v,v1):
		# 				eq = np.all( np.isclose(vv, vv1, rtol=1e-5, atol=1e-9, equal_nan=True ) )
		# 				if not eq:
		# 					return False
		# 		elif isinstance(v, np.ndarray):
		# 			eq = np.all( np.isclose(v, v1, rtol=1e-5, atol=1e-9, equal_nan=True ) )
		#
		# 		elif isinstance(v, (str,int,float,tuple,list,dict)):
		# 			eq = v==v1
		# 		else:
		# 			raise ValueError( f'Unable to hash type: {type(v)}' )
		# 		if not eq:
		# 			return False
		# return eq

	@property
	def _class_str(self):
		ss     = 'n' if (self.isinference and not self.isparametric) else ''
		stat   = 't' if (self.STAT=='T') else self.STAT
		s      = f'S{ss}PM{{{stat}}} ({self.dim}D)'
		if self.isinference:
			s += ' inference'
		return s
	
	
	def _reexec(self):
		import spm1d
		fn  = eval(  f'spm1d.stats.{self.testname}'  )
		return fn( *self._args, **self._kwargs )
	
	def _set_data(self, *args, **kwargs):
		self._args   = args
		self._kwargs = kwargs
	
	
	

	
	
	@property
	def isanova(self):
		return self.STAT == 'F'
	# @property
	# def isparametric(self):  # overloaded by inference object (set to False for perm and other nonparametric methods)
	# 	return True
	@property
	def isregress(self):
		return self.testname == 'regress'
	@property
	def ismultigroup(self):
		h = self.testname in ['ttest2', 'anova1']
		if not h:
			h = self.testname.startswith( ('anova2', 'anova3') )
		return h


	def isequal(self, other, verbose=False):
		if type(self)!=type(other):
			return False
		
		for k,v in self.__dict__.items():
			if k.startswith('_'):
				continue
			
			v1 = getattr(other, k)
			
			
			
			if v is None:
				eq = v1 is None
				
			elif isinstance(v, float) and np.isnan(v):
				eq = np.isnan( v1 )

			
			elif (k=='extras') and (self.method=='perm'):
				d,d1 = v.copy(), v1.copy()
				# d.pop('permuter')
				# d1.pop('permuter')
				d.pop('_nprandstate')
				d1.pop('_nprandstate')
				eq = d==d1

			elif (k=='permuter'):
				eq = True
			
			elif isinstance(v, tuple) and isinstance(v[0], np.ndarray):
				for vv,vv1 in zip(v,v1):
					eq = np.all( np.isclose(vv, vv1, rtol=1e-5, atol=1e-9, equal_nan=True ) )
					if not eq:
						break

			elif isinstance(v, np.ndarray):
				eq = np.all( np.isclose(v, v1, rtol=1e-5, atol=1e-9, equal_nan=True ) )
		
			elif isinstance(v, (str,int,float,tuple,list,dict)):
				eq = v==v1
			else:
				raise ValueError( f'Unable to hash type: {type(v)}' )

			if verbose:
				print( f'{k:<14} : equal={eq}'  )

			if not eq:
				return False

		return True



	def normality_test(self, alpha=0.05):
		from .. normality.k2 import residuals
		return residuals( self.residuals ).inference( alpha )


