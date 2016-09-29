
# Copyright (C) 2016  Todd Pataky

import itertools
import numpy as np
from scipy.special import factorial
from . import calculators
from . metrics import metric_dict



#---------------------------------------------------------------------------------
#  0D and 1D PERMUTERS (ABSTRACT CLASSES)
#---------------------------------------------------------------------------------

class _Permuter(object):
	CalculatorClass  = None
	ismultivariate   = False
	def _set_teststat_calculator(self, *args):
		self.calc    = self.CalculatorClass(*args)
	def build_pdf(self, iterations=-1):
		pass
	def get_test_stat(self, labels):
		pass
	def get_test_stat_original(self):
		return self.get_test_stat( self.labels0 )
	def get_z_critical(self, alpha=0.05, two_tailed=False):
		perc     = [100*0.5*alpha, 100*(1-0.5*alpha)]  if two_tailed else 100*(1-alpha)
		# zstar    = np.percentile(self.Z, perc, interpolation='linear', axis=0)
		zstar    = np.percentile(self.Z, perc, interpolation='midpoint', axis=0)
		return zstar
	


class _Permuter0D(_Permuter):
	dim  = 0   #data dimensionality
	minp = 0   #minimum possible p value
	maxp = 1   #maximum possible p value
	
	
	def get_p_value(self, z, zstar, alpha, Z=None):
		two_tailed    = isinstance(zstar, np.ndarray)
		Z             = self.Z if Z is None else Z
		if two_tailed:
			if z > 0:
				p     = 2 * ( self.Z > z ).mean()
			else:
				p     = 2 * ( self.Z < z ).mean()
		else:
			p         = ( self.Z > z ).mean()
		### set miminum and maximum p values:
		self.minp     = 1.0 / self.Z.size
		self.maxp     = 1 - self.minp
		### adjust the p value to alpha if (z > z*) but (p > alpha)
		zc0,zc1       = zstar if two_tailed else (-np.inf, zstar)
		if (z > zc1) and (p > alpha):
			p         = alpha
		elif (z < zc0) and (p > alpha):
			p         = alpha
		### substitute with min/max p value if applicable:
		p             = min( max(p, self.minp), self.maxp )
		return p



class _Permuter1D(_Permuter):
	dim    = 1      #data dimensionality
	roi    = None   #region of interest
	_roin  = None   #boolean opposite of roi
	hasroi = False  #flag
	
	def _set_roi(self, roi):
		if roi is not None:
			self.roi    = np.asarray(roi, dtype=bool)
			self._roin  = np.logical_not( self.roi )
			self.hasroi = True
			roi         = np.asarray( [self.roi]*self.J, dtype=bool )
			if self.ismultivariate:
				roi     = np.dstack( [roi]*self.I )
			self.Y      = np.ma.masked_array( self.Y, np.logical_not(roi) )
	
	def build_secondary_pdf(self, zstar, circular=False):
		self.Z2          = [self.metric.get_max_metric(z, zstar, circular)   for z in self.ZZ]
	def get_clusters(self, z, zstar, two_tailed=False):
		return self.metric.get_all_clusters(z, zstar, self.Z2, two_tailed)
	def get_test_stat_original(self):
		z = self.get_test_stat( self.labels0 )
		if self.hasroi:
			z = np.ma.masked_array( z, self._roin )
		return z
	def set_metric(self, metric_name):
		self.metric     = metric_dict[metric_name]







#---------------------------------------------------------------------------------
#  ONE-SAMPLE PERMUTERS
#---------------------------------------------------------------------------------

class _PermuterOneSample(object):
	def build_pdf(self, iterations=-1):
		Z              = []
		if iterations==-1:
			LABELS     = itertools.product((0,1), repeat=self.N)
			Z          = [self.get_test_stat(labels)  for labels in LABELS]
		else:
			for i in range(iterations):
				labels = np.random.binomial(1, 0.5, self.N)
				Z.append( self.get_test_stat(labels) )
		self.Z         = np.asarray(Z)
		if self.dim==1:
			self.ZZ    = self.Z
			self.Z     = self.Z.max(axis=1)

	def _get_signs(self, labels):
		return -2*np.array(labels) + 1
	def get_signs(self, labels):
		return self._get_signs(labels)
	def get_test_stat(self, labels):
		signs          = self.get_signs(labels)
		y              = signs * (self.Y - self.mu)
		return self.calc.get_test_stat_mu_subtracted(y)
	def _set_stat_calculator(self):
		self.calc       = self.CalculatorClass(self.J, self.mu)



class _PermuterOneSample0D(_PermuterOneSample, _Permuter0D):
	def __init__(self, y, mu=None):
		self.Y          = y                         #original responses
		self.J          = y.shape[0]                #number of responses
		self.N          = y.size                    #total number of permutable elements
		self.Z          = None                      #test statistic distribution
		self.mu         = 0 if mu is None else mu   #datum
		self.labels0    = np.array( [0]*self.N )    #original labels
		self.nPermTotal = 2**self.N                 #total possible permutations
		self.calc       = None                      #test statistic calculator (set by subclasses)
		self._set_stat_calculator()



class _PermuterOneSample1D(_PermuterOneSample, _Permuter1D):
	def __init__(self, y, mu=None, roi=None):
		self.Y          = y                         #original responses
		self.J          = y.shape[0]                #number of responses
		self.Q          = y.shape[1]                #number of continuum nodes
		self.I          = 1 if y.ndim==2 else y.shape[2]  #number of vector components
		self.N          = self.J * self.I           #total number of permutable elements
		self.ZZ         = None                      #all permuted test statistic fields
		self.Z          = None                      #primary PDF:    test statistic field maxima distribution
		self.Z2         = None                      #secondary PDF:  cluster metric distribution
		self.mu         = 0 if mu is None else mu   #datum
		self.roi        = None                      #region(s) of interest
		self.labels0    = np.array( [0]*self.N )    #original labels
		self.nPermTotal = 2**self.N                 #total possible permutations
		self.calc       = None                      #test statistic calculator (set by subclasses)
		self._set_stat_calculator()
		self._set_roi(roi)





class PermuterHotellings0D(_PermuterOneSample0D):
	ismultivariate  = True
	CalculatorClass = calculators.CalculatorHotellings0D
	def get_signs(self, labels):
		return self._get_signs(labels).reshape( self.Y.shape )
class PermuterHotellings1D(_PermuterOneSample1D):
	ismultivariate  = True
	CalculatorClass = calculators.CalculatorHotellings1D
	def get_signs(self, labels):
		signs           = self._get_signs(labels).reshape( (self.J, self.I) )
		return np.array([signs]*self.Q).swapaxes(0, 1)
class PermuterTtest0D(_PermuterOneSample0D):
	CalculatorClass    = calculators.CalculatorTtest
class PermuterTtest1D(_PermuterOneSample1D):
	CalculatorClass    = calculators.CalculatorTtest
	def get_signs(self, labels):
		return np.array(  [self._get_signs(labels)] * self.Q ).T
















#---------------------------------------------------------------------------------
#  REGRESSION PERMUTERS
#---------------------------------------------------------------------------------

class _PermuterRegress(object):
	def __init__(self, y, x):
		self.Y             = y
		self.x             = x
		self.J             = x.size
		self.labels0       = np.arange( self.J )  #original labels
		self.nPermTotal    = int( factorial( self.J ) )
		self.calc          = None
		self.Z             = None  #PDF
		self._set_stat_calculator()


	def _set_stat_calculator(self):
		self.calc          = self.CalculatorClass(self.x)

	def build_pdf(self, iterations=-1):
		if iterations==-1:
			LABELS       = itertools.permutations( range(self.J) )
			Z            = [self.get_test_stat(ind)  for ind in LABELS]
		else:
			Z            = []
			for i in range(iterations):
				ind      = np.random.permutation( self.J )
				Z.append(  self.get_test_stat(ind)  )
		self.Z           = np.array(Z)
		if self.dim==1:
			self.ZZ    = self.Z
			self.Z     = self.Z.max(axis=1)

	def get_test_stat(self, ind):
		return self.calc.get_test_stat( self.Y[ list(ind) ] )


class _PermuterRegress1D(_PermuterRegress, _Permuter1D):
	def __init__(self, y, x, roi=None):
		self.Y             = y
		self.x             = x
		self.J             = x.size
		self.I             = y.shape[2] if self.ismultivariate else 1   #number of vector components
		self.labels0       = np.arange( self.J )  #original labels
		self.nPermTotal    = int( factorial( self.J ) )
		self.calc          = None
		self.ZZ            = None                      #all permuted test statistic fields
		self.Z             = None                      #primary PDF:    test statistic field maxima distribution
		self.Z2            = None                      #secondary PDF:  cluster metric distribution
		self.roi           = roi                       #region(s) of interest
		self._set_stat_calculator()
		self._set_roi(roi)




class PermuterCCA0D(_PermuterRegress, _Permuter0D):
	ismultivariate         = True
	CalculatorClass        = calculators.CalculatorCCA0D
class PermuterCCA1D(_PermuterRegress1D):
	ismultivariate = True
	CalculatorClass        = calculators.CalculatorCCA1D
class PermuterRegress0D(_PermuterRegress, _Permuter0D):
	CalculatorClass        = calculators.CalculatorRegress0D
class PermuterRegress1D(_PermuterRegress1D):
	CalculatorClass        = calculators.CalculatorRegress1D




#---------------------------------------------------------------------------------
#  TWO-SAMPLE PERMUTERS
#---------------------------------------------------------------------------------

class _PermuterTwoSample(object):
	def __init__(self, yA, yB):
		yA,yB               = np.asarray(yA, dtype=float), np.asarray(yB, dtype=float)
		self.Y              = self._stack(yA, yB)
		self.JA             = yA.shape[0]
		self.JB             = yB.shape[0]
		self.J              = self.JA + self.JB
		self.labels0        = np.array( [0]*self.JA + [1]*self.JB )  #original labels
		self.labelsZeros    = np.array( [0]*self.J )  #empty labels
		if factorial(self.J)==np.inf:
			self.nPermTotal = -1
		else:
			self.nPermTotal = int(factorial(self.J) / ( factorial(self.JA)*factorial(self.JB) ))
		self.calc           = None
		self.Z              = None
		self._set_stat_calculator()

	def _set_stat_calculator(self):
		self.calc           = self.CalculatorClass(self.JA, self.JB)

	def _stack(self, yA, yB):
		return np.hstack( [yA, yB] ) if yA.ndim==1 else np.vstack( [yA, yB] )

	def build_pdf(self, iterations=-1):
		if iterations==-1:
			ONES            = itertools.combinations(range(self.J), self.JA)
			Z               = [self.get_test_stat_ones(ones)  for ones in ONES]
		else:
			Z               = []
			for i in range(iterations):
				ones        = np.random.permutation(self.J)[:self.JA]
				Z.append(  self.get_test_stat_ones(ones)  )
		self.Z              = np.asarray(Z)
		if self.dim==1:
			self.ZZ         = self.Z
			self.Z          = self.Z.max(axis=1)

	def get_test_stat(self, labels):
		yA,yB               = self.Y[labels==0], self.Y[labels==1]
		return self.calc.get_test_stat(yA, yB)

	def get_test_stat_ones(self, ones):
		labels              = self.labelsZeros.copy()
		labels[list(ones)]  = 1
		return self.get_test_stat(labels)


class _PermuterTwoSample1D(_PermuterTwoSample, _Permuter1D):
	def __init__(self, yA, yB, roi=None):
		super(_PermuterTwoSample1D, self).__init__(yA, yB)
		self.roi            = None
		self.I              = yA.shape[2] if self.ismultivariate else 1   #number of vector components
		self._set_roi(roi)

class PermuterHotellings20D(_PermuterTwoSample, _Permuter0D):
	ismultivariate    = True
	CalculatorClass   = calculators.CalculatorHotellings20D
class PermuterHotellings21D(_PermuterTwoSample1D):
	ismultivariate    = True
	CalculatorClass   = calculators.CalculatorHotellings21D
class PermuterTtest20D(_PermuterTwoSample, _Permuter0D):
	CalculatorClass   = calculators.CalculatorTtest2
class PermuterTtest21D(_PermuterTwoSample1D):
	CalculatorClass   = calculators.CalculatorTtest2




#---------------------------------------------------------------------------------
#  ANOVA PERMUTERS
#---------------------------------------------------------------------------------

class _PermuterANOVA(object):
	def __init__(self, y, *args):
		self.Y          = y                         #original responses
		self.J          = y.shape[0]                #number of responses
		self.Z          = None                      #test statistic distribution
		self.labels0    = np.arange( self.J )       #original labels
		self.nPermTotal = factorial( self.J )
		self.nPermTotal = -1 if self.nPermTotal==np.inf else int(self.nPermTotal)
		self.calc       = None
		self._set_teststat_calculator(*args)

	def build_pdf(self, iterations=-1):
		if iterations==-1:
			LABELS       = itertools.permutations( range(self.J) )
			Z            = [self.get_test_stat(ind)  for ind in LABELS]
		else:
			Z            = []
			for i in range(iterations):
				ind      = np.random.permutation( self.J )
				Z.append(  self.get_test_stat(ind)  )
		self.Z           = np.array(Z)
		if self.dim==1:
			self.ZZ    = self.Z
			self.Z     = self.Z.max(axis=-1)

	def get_design_label(self):
		return self.calc.design.get_design_label()
	def get_effect_labels(self):
		return self.calc.design.get_effect_labels()
	def get_test_stat(self, ind):
		return self.calc.get_test_stat( self.Y[ list(ind) ] )


class _PermuterANOVA0D(_PermuterANOVA, _Permuter0D):
	pass
class _PermuterANOVA1D(_PermuterANOVA, _Permuter1D):
	def __init__(self, y, roi=None, *args):
		super(_PermuterANOVA1D, self).__init__(y, *args)
		self.ZZ         = None                      #all permuted test statistic fields
		self.Z2         = None                      #secondary PDF:  cluster metric distribution
		self._set_roi(roi)

	def get_test_stat(self, ind):
		z               = super(_PermuterANOVA1D, self).get_test_stat(ind)
		if self.hasroi:
			z[ self._roin ] = 0
		return z











class _PermuterANOVA0DmultiF(_PermuterANOVA0D):
	def get_p_value_list(self, zz, zzstar, alpha):
		return [self.get_p_value(z, zstar, alpha, Z=Z)  for z,zstar,Z in zip(zz,zzstar,self.Z.T)]
	def get_z_critical_list(self, alpha=0.05, two_tailed=False):
		return self.get_z_critical(alpha)

class _PermuterANOVA1DmultiF(_PermuterANOVA1D):
	def build_secondary_pdfs(self, zstarlist, circular=False):
		Z2   = []
		for i,zstar in enumerate(zstarlist):
			Z    = self.ZZ[:,i,:]   #all test statistic fields for one ANOVA term
			z2   = [self.metric.get_max_metric(z, zstar, circular)  for z in Z]
			Z2.append(z2)
		self.Z2  = np.array(Z2)

	def get_test_stat(self, ind):
		zz       = self.calc.get_test_stat( self.Y[ list(ind) ] )
		if self.hasroi:
			for z in zz:
				z[ self._roin ] = 0
		return zz
		
	def get_test_stat_original(self):
		z = self.get_test_stat( self.labels0 )
		if self.hasroi:
			for i,zz in enumerate(z):
				zz = np.ma.masked_array( zz, self._roin )
				z[i] = zz
		return z

	def get_z_critical_list(self, alpha=0.05):
		return self.get_z_critical(alpha)





class PermuterANOVA10D(_PermuterANOVA0D):
	def _set_teststat_calculator(self, *args):
		self.calc  = calculators.CalculatorANOVA1( args[0] )
class PermuterANOVA1rm0D(_PermuterANOVA0D):
	CalculatorClass    = calculators.CalculatorANOVA1rm
class PermuterANOVA11D(_PermuterANOVA1D):
	def _set_teststat_calculator(self, *args):
		self.calc  = calculators.CalculatorANOVA1( args[0] )
class PermuterANOVA1rm1D(_PermuterANOVA1D):
	CalculatorClass    = calculators.CalculatorANOVA1rm



class PermuterANOVA20D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2
class PermuterANOVA2nested0D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2nested
class PermuterANOVA2onerm0D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2onerm
class PermuterANOVA2rm0D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2rm



class PermuterANOVA21D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2
class PermuterANOVA2nested1D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2nested
class PermuterANOVA2onerm1D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2onerm
class PermuterANOVA2rm1D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA2rm



class PermuterANOVA30D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3
class PermuterANOVA3nested0D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3nested
class PermuterANOVA3onerm0D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3onerm
class PermuterANOVA3tworm0D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3tworm
class PermuterANOVA3rm0D(_PermuterANOVA0DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3rm



class PermuterANOVA31D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3
class PermuterANOVA3nested1D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3nested
class PermuterANOVA3onerm1D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3onerm
class PermuterANOVA3tworm1D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3tworm
class PermuterANOVA3rm1D(_PermuterANOVA1DmultiF):
	CalculatorClass    = calculators.CalculatorANOVA3rm




#---------------------------------------------------------------------------------
#  MANOVA PERMUTERS
#---------------------------------------------------------------------------------

class _PermuterMANOVA(_PermuterANOVA):
	ismultivariate = True
	def __init__(self, y, A):
		self.A         = A
		self.I         = y.shape[ self.dim + 1 ]
		super(_PermuterMANOVA, self).__init__(y, A)
	def _set_teststat_calculator(self, *args):
		self.calc      = self.CalculatorClass( self.A, self.I )

class PermuterMANOVA10D(_PermuterMANOVA, _Permuter0D):
	CalculatorClass    = calculators.CalculatorMANOVA10D
class PermuterMANOVA11D(_PermuterANOVA1D, _PermuterMANOVA):
	CalculatorClass    = calculators.CalculatorMANOVA11D


