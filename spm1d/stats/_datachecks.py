'''
Data checking tools.

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)
'''

# Copyright (C) 2016  Todd Pataky



import warnings
import numpy as np



def asmatrix(Y, dtype=None):
	Y = np.asarray(Y, dtype=dtype)
	return np.matrix(Y).T if Y.ndim==1 else np.matrix(Y)




class SPM1DError(ValueError):
	pass

class DataChecker(object):
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



class DataCheckerANOVA1List(DataChecker):
	def __init__(self, YY):
		self.YY   = YY
	def check(self):
		if len(self.YY)==1:
			raise( ValueError('There must be at least two levels in one-way ANOVA.') )
		elif len(self.YY)==2:
			warnings.warn('\nWARNING:  A one-way ANOVA with two levels is equivalent to a two-sample t test. The F statistic is equal to the square of the t statistic.\n', UserWarning, stacklevel=2)
		[self.check_array(Y)  for Y in self.YY]
		[self.check_2d(Y) for Y in self.YY]
		[self.check_size(Y) for Y in self.YY]
		[self.check_zero_variance(Y) for Y in self.YY]
		nGroups  = len(self.YY)
		for i in range(1, nGroups):
			self.check_equal_Q(self.YY[0], self.YY[i])
			
class DataCheckerANOVA1(DataChecker):
	def __init__(self, Y, A):
		self.Y   = Y
		self.A   = A
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


class DataCheckerANOVA2(DataChecker):
	def __init__(self, Y, A, B):
		self.Y   = Y
		self.A   = A
		self.B   = B
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



class DataCheckerRegress(DataChecker):
	def __init__(self, Y, x):
		self.Y    = Y
		self.x    = x
	def check(self):
		self.check_array(self.Y)
		self.check_2d(self.Y)
		self.check_1d(self.x, 2)
		self.check_size(self.Y)
		self.check_zero_variance(self.Y)
		self.check_equal_J(self.Y, self.x)
		

class DataCheckerTtest(DataChecker):
	def __init__(self, Y, y0):
		self.Y    = Y
		self.y0   = y0
	def check(self):
		self.check_array(self.Y)
		self.check_2d(self.Y)
		self.check_size(self.Y)
		self.check_zero_variance(self.Y)

class DataCheckerTtest2(DataChecker):
	def __init__(self, YA, YB):
		self.YA   = YA
		self.YB   = YB
	def check(self):
		YY        = self.YA, self.YB
		[self.check_array(Y)  for Y in YY]
		[self.check_2d(Y) for Y in YY]
		[self.check_size(Y) for Y in YY]
		self.check_equal_Q(self.YA, self.YB)
		[self.check_zero_variance(Y) for Y in YY]

class DataCheckerTtestPaired(DataCheckerTtest2):
	def check(self):
		DataCheckerTtest2.check(self)
		self.check_equal_J(self.YA, self.YB)





def check(testname, *args):
	if testname == 'anova1list':
		YY       = args[0]
		checker  = DataCheckerANOVA1List(YY)
	if testname == 'anova1':
		Y,A      = args
		checker  = DataCheckerANOVA1(Y, A)
	if testname == 'anova2':
		Y,A,B    = args
		checker  = DataCheckerANOVA2(Y, A, B)
	if testname == 'ttest':
		Y,y0     = args
		checker  = DataCheckerTtest(Y, y0)
	elif testname == 'ttest_paired':
		YA,YB    = args
		checker  = DataCheckerTtestPaired(YA, YB)
	elif testname == 'ttest2':
		YA,YB    = args
		checker  = DataCheckerTtest2(YA, YB)
	elif testname == 'regress':
		Y,x      = args
		checker  = DataCheckerRegress(Y, x)
	checker.check()



