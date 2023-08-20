'''
Argument checks for user-facing functions.  

NOTE!  In spm1d v0.5 argument checking is performed by 
the "checkargs" decorator in _dec.py

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)
'''

# Copyright (C) 2023  Todd Pataky



import warnings
import numpy as np



class SPM1DError(ValueError):
	pass

class Checker(object):
	def check(self):
		pass
	
	def check_1d(self, x, argnum):
		ndim      = np.ndim(x)
		if ndim!=1:
			msg   = '\n\nArgument number %d must be a 1D array or list. \n\n' %argnum
			raise SPM1DError(msg)

	def check_2d(self, Y):
		pass
		# ndim      = np.ndim(Y)
		# if ndim!=2:
		# 	msg   = '\n\n%d-D array detected. spm1d only accepts 2D arrays. \n\n' %np.ndim(Y)
		# 	raise SPM1DError(msg)
	
	def check_array(self, Y):
		if not isinstance(Y, np.ndarray):
			msg   = 'Object of type %s detected. Must submit a numpy array.' %type(Y)
			raise SPM1DError(msg)
	
	def check_equal_J(self, Y0, Y1):
		J0,J1     = Y0.shape[0], Y1.shape[0]
		if J0!=J1:
			msg   = 'Unequal number of responses in (J x Q) arrays (J1=%d, J2=%d). J1 must equal J2.' %(J0,J1)
			raise SPM1DError(msg)

	def check_equal_Q(self, Y0, Y1):
		if (Y0.ndim > 1) and (Y1.ndim > 1):
			Q0,Q1     = Y0.shape[1], Y1.shape[1]
			if Q0!=Q1:
				msg   = 'Unequal number of nodes in (J x Q) arrays (Q1=%d, Q2=%d). Q1 must equal Q2.' %(Q0,Q1)
				raise SPM1DError(msg)
	
	def check_equal_JQ(self, Y0, Y1):
		self.check_equal_J(Y0, Y1)
		self.check_equal_Q(Y0, Y1)

	def check_size(self, Y):
		pass
		# if Y.shape[1] < 11:
		# 	msg   = '(J x Q) array with Q=%d detected. Q must be at least 11.' %Y.shape[1]
		# 	raise SPM1DError(msg)
			
	
	def check_zero_variance(self, Y, only_warning=False):
		a         = Y.var(axis=0)==0
		if np.any(a):
			ind   = np.argwhere( a ).flatten().tolist()
			msg   = '\n\nZero variance detected at the following nodes:\n\n %s \n' %ind.__repr__()
			if only_warning:
				warnings.warn(msg)
			else:
				raise SPM1DError(msg)



class CheckerANOVA1(Checker):
	def __init__(self, Y, A, roi=None):
		self.Y    = Y
		self.A    = A
		self.roi  = roi
	def check(self):
		[self.check_array(x)  for x in [self.Y,self.A]]
		self.check_2d(self.Y)
		self.check_1d(self.A, 2)
		if np.unique(self.A).size == 1:
			raise( ValueError('There must be at least two factor levels in a one-way ANOVA (only one found).') )
		elif np.unique(self.A).size == 2:
			warnings.warn('\nWARNING:  A one-way ANOVA with two levels is equivalent to a two-sample t test. The F statistic is equal to the square of the t statistic.\n', UserWarning, stacklevel=2)
		self.check_size(self.Y)
		self.check_equal_J(self.Y, self.A)
		self.check_zero_variance(self.Y)


class CheckerANOVA2(Checker):
	def __init__(self, Y, A, B, roi=None):
		self.Y   = Y
		self.A   = A
		self.B   = B
		self.roi  = roi
	def check(self):
		YAB      = self.Y, self.A, self.B
		[self.check_array(x)  for x in YAB]
		self.check_2d(self.Y)
		self.check_1d(self.A, 2)
		self.check_1d(self.B, 3)
		self.check_size(self.Y)
		self.check_equal_J(self.Y, self.A)
		self.check_equal_J(self.Y, self.B)
		self.check_zero_variance(self.Y)



class CheckerREGRESS(Checker):
	def __init__(self, Y, x, roi=None):
		self.Y    = Y
		self.x    = x
		self.roi  = roi
	def check(self):
		self.check_array(self.Y)
		self.check_2d(self.Y)
		self.check_1d(self.x, 2)
		self.check_size(self.Y)
		self.check_zero_variance(self.Y)
		self.check_equal_J(self.Y, self.x)
		

class CheckerTTEST(Checker):
	def __init__(self, Y, y0, roi=None):
		self.Y    = Y
		self.y0   = y0
		self.roi  = roi
	def check(self):
		self.check_array(self.Y)
		self.check_2d(self.Y)
		self.check_size(self.Y)
		self.check_zero_variance(self.Y)

class CheckerTTEST2(Checker):
	def __init__(self, YA, YB, roi=None):
		self.YA   = YA
		self.YB   = YB
		self.roi  = roi
	def check(self):
		YY        = self.YA, self.YB
		[self.check_array(Y)  for Y in YY]
		[self.check_2d(Y) for Y in YY]
		[self.check_size(Y) for Y in YY]
		self.check_equal_Q(self.YA, self.YB)
		[self.check_zero_variance(Y) for Y in YY]

class CheckerTTEST_PAIRED(CheckerTTEST2):
	def check(self):
		super().check()
		self.check_equal_J(self.YA, self.YB)
