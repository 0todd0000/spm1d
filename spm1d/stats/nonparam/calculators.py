
from math import log
import numpy as np
from spm1d.stats.anova import designs,models
from spm1d.stats.anova.ui import aov



eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



#---------------------------------------------------------------------------------
#  ONE-SAMPLE TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

class _CalculatorOneSample(object):
	def __init__(self, nResponses, mu=None):
		self.J     = nResponses
		self.mu    = 0 if mu is None else mu
	def get_test_stat(self, y):
		return self.get_test_stat_mu_subtracted( y - self.mu )
	def get_test_stat_mu_subtracted(self, y):
		pass


class CalculatorTtest(_CalculatorOneSample):
	def __init__(self, nResponses, mu=None):
		super(CalculatorTtest, self).__init__(nResponses, mu)
		self.sqrtN       = int(self.J)**0.5
	def get_test_stat_mu_subtracted(self, y):
		return y.mean(axis=0) / (  y.std(axis=0, ddof=1) / self.sqrtN  )


class CalculatorHotellings0D(_CalculatorOneSample):
	def get_test_stat_mu_subtracted(self, y):
		m       = np.matrix( y.mean(axis=0) )       #estimated mean
		W       = np.matrix( np.cov(y.T, ddof=1) )  #estimated covariance
		T2      = self.J * m * np.linalg.inv(W) * m.T
		return float(T2)


# class CalculatorTtest(_CalculatorOneSample):
# 	def __init__(self, nResponses, mu=None):
# 		super(CalculatorTtest, self).__init__(nResponses, mu)
# 		self.sqrtN       = int(self.J)**0.5
# 	def get_test_stat_mu_subtracted(self, y):
# 		return y.mean(axis=0) / (  y.std(axis=0, ddof=1) / self.sqrtN  )




#---------------------------------------------------------------------------------
#  TWO-SAMPLE TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

class _CalculatorTwoSample(object):
	def __init__(self, nA, nB):
		self.nA1         = nA - 1
		self.nB1         = nB - 1
		self.df          = nA + nB - 2
	def get_test_stat(self, yA, yB):
		pass


class CalculatorTtest20D( _CalculatorTwoSample ):
	def __init__(self, nA, nB):
		super(CalculatorTtest20D, self).__init__(nA, nB)
		self.sqrtAB      = (1.0/nA + 1.0/nB)**0.5
	def get_test_stat(self, yA, yB):
		mA,mB  = yA.mean(), yB.mean()
		sA,sB  = yA.std(ddof=1), yB.std(ddof=1)
		s      = (   (  self.nA1*sA*sA + self.nB1*sB*sB  )  /  self.df   )**0.5
		return (mA-mB) / s / self.sqrtAB


class CalculatorHotellings20D( _CalculatorTwoSample ):
	def __init__(self, nA, nB):
		super(CalculatorHotellings20D, self).__init__(nA, nB)
		self.nABAB       = (nA * nB) / float( nA + nB )
	def get_test_stat(self, yA, yB):
		yA,yB     = np.matrix(yA), np.matrix(yB)
		mA,mB     = yA.mean(axis=0), yB.mean(axis=0)
		WA,WB     = np.cov(yA.T), np.cov(yB.T)
		W         = (self.nA1*WA + self.nB1*WB) / self.df
		T2        = self.nABAB  * (mB-mA) * np.linalg.inv(W) * (mB-mA).T
		return float(T2)





#---------------------------------------------------------------------------------
#  REGRESSION TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------



class CalculatorRegress0D(object):
	def __init__(self, x):
		self.x           = np.asarray(x, dtype=float)
		self.J           = self.x.size
		self.df          = self.J - 2     #degrees of freedom
		### design matrix:
		X                = np.ones( (self.J, 2) )
		X[:,0]           = self.x
		self.X           = np.matrix(X)
		self.Xi          = np.linalg.pinv(X)
		self.c           = np.matrix([1,0]).T
		self.cXXc        = float(  self.c.T * np.linalg.inv(self.X.T*self.X) * self.c  )
	
	def get_test_stat(self, y):
		Y      = np.matrix(y).T
		b      = self.Xi * Y            #parameters
		eij    = Y - self.X*b           #residuals
		R      = eij.T*eij              #residual sum of squares
		sigma2 = float(R) / self.df     #variance
		t      = float(self.c.T*b)  /   (sigma2*self.cXXc)**0.5
		return t



class CalculatorCCA0D(object):
	def __init__(self, x):
		self.x           = np.asarray(x, dtype=float)
		self.J           = x.size
		self.X           = np.matrix(x).T
		Z                = np.matrix( np.ones(self.J) ).T
		self.Rz          = np.eye(self.J) - Z * np.linalg.inv(Z.T*Z) * Z.T
		XStar            = self.Rz * self.X
		self.XXXiX       = XStar  *  np.linalg.inv( XStar.T * XStar  )  * XStar.T
		self.p           = 1.0   #nContrasts
		self.r           = 1.0   #nNuisanceFactors
		self.m           = self.J - self.p - self.r

	def get_test_stat(self, y):
		### estimate maximum canonical correlation:
		Y          = np.matrix(y)
		YStar      = self.Rz * Y
		H          = YStar.T * self.XXXiX * YStar / self.p
		W          = YStar.T  * (np.eye(self.J)  -  self.XXXiX) * YStar  / self.m
		F          = np.linalg.inv(W) * H
		ff         = np.linalg.eigvals( F )
		fmax       = float( np.real(ff.max()) )
		r2max      = fmax * self.p  / (self.m + fmax*self.p)
		rmax       = r2max**0.5
		### compute test statistic:
		m          = y.shape[1]  # df = m  (nComponents)
		x2         = -(self.J - 1 - 0.5*(m+2) )  *  log( (1-rmax**2) )
		return x2









#---------------------------------------------------------------------------------
#  ANOVA TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

class _CalculatorANOVAsingleF(object):
	def get_test_stat(self, y):
		model   = models.LinearModel(y, self.design.X)
		model.fit()
		F       = aov(model, self.design.contrasts, self.design.f_terms)[0]
		return F.z

class _CalculatorANOVAmultiF(object):
	def get_test_stat(self, y):
		model   = models.LinearModel(y, self.design.X)
		model.fit()
		FF      = aov(model, self.design.contrasts, self.design.f_terms)
		return [F.z for F in FF]



class CalculatorANOVA1(_CalculatorANOVAsingleF):
	def __init__(self, A):
		self.design      = designs.ANOVA1(A)
class CalculatorANOVA1rm(_CalculatorANOVAsingleF):
	def __init__(self, A, SUBJ):
		self.design      = designs.ANOVA1rm(A, SUBJ)



class CalculatorANOVA2(_CalculatorANOVAmultiF):
	def __init__(self, A, B):
		self.design      = designs.ANOVA2(A, B)
class CalculatorANOVA2nested(_CalculatorANOVAmultiF):
	def __init__(self, A, B):
		self.design      = designs.ANOVA2nested(A, B)
class CalculatorANOVA2onerm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, SUBJ):
		self.design      = designs.ANOVA2onerm(A, B, SUBJ)
class CalculatorANOVA2rm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, SUBJ):
		self.design      = designs.ANOVA2rm(A, B, SUBJ)



class CalculatorANOVA3(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C):
		self.design      = designs.ANOVA3(A, B, C)
class CalculatorANOVA3nested(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C):
		self.design      = designs.ANOVA3nested(A, B, C)
class CalculatorANOVA3onerm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C, SUBJ):
		self.design      = designs.ANOVA3onerm(A, B, C, SUBJ)
class CalculatorANOVA3tworm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C, SUBJ):
		self.design      = designs.ANOVA3tworm(A, B, C, SUBJ)
class CalculatorANOVA3rm(_CalculatorANOVAmultiF):
	def __init__(self, A, B, C, SUBJ):
		self.design      = designs.ANOVA3rm(A, B, C, SUBJ)




# class CalculatorOneSampleT(CalculatorTtest):
# 	def get_test_stat(self, y):
# 		return (y-self.mu).mean(axis=0) / (  y.std(ddof=1, axis=0)/self.sqrtN  )
#
#
#
#
# class CalculatorTwoSampleT(object):
# 	def __init__(self, nResponsesA, nResponsesB):
# 		self.JA          = int(nResponsesA)
# 		self.JB          = int(nResponsesB)
# 		self.J           = self.JA + self.JB
# 		self.df          = self.J - 2
# 		self.X           = None
# 		self.Xi          = None
# 		self.c           = None
# 		self._build_design_matrix()
#
# 	def _build_design_matrix(self):
# 		X             = np.zeros( (self.J, 2) )
# 		X[:self.JA,0] = 1
# 		X[self.JA:,1] = 1
# 		self.X        = np.matrix(X)
# 		self.Xi       = np.linalg.pinv(X)
# 		self.c        = np.matrix((1, -1)).T
# 		self.cXXc     = float(self.c.T*(np.linalg.inv(self.X.T*self.X))*self.c) + eps
#
# 	def get_test_stat(self, yA, yB):
# 		Y        = np.matrix(np.vstack([yA, yB]))
# 		b        = self.Xi*Y
# 		eij      = Y - self.X*b           #residuals
# 		R        = eij.T*eij              #residual sum of squares
# 		sigma2   = np.diag(R)/self.df     #variance
# 		t        = np.array(self.c.T*b).flatten()  /   np.sqrt(sigma2*self.cXXc)
# 		return t

