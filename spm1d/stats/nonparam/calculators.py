
# Copyright (C) 2025  Todd Pataky

from math import log
import numpy as np
from .. anova import designs,models
from .. anova.ui import aov



eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



#---------------------------------------------------------------------------------
#  ONE-SAMPLE TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

# class _CalculatorOneSample(object):
#     def __init__(self, nResponses, mu=None):
#         self.J     = nResponses
#         self.mu    = 0 if mu is None else mu
#
#
#     # def teststat(self, y):
#     #     return self.teststat_mu_subtracted( y - self.mu )
#     # def teststat_mu_subtracted(self, y):
#     #     pass


class CalculatorTtest(object):
    def __init__(self, nResponses, mu=None):
        # super(CalculatorTtest, self).__init__(nResponses, mu)
        self.J      = nResponses
        self.mu     = 0 if mu is None else mu
        self.sqrtN  = int(self.J)**0.5
    
    def teststat(self, y, signs):
        y = (np.asarray(signs) * (y - self.mu).T).T
        t = y.mean(axis=0) / (  y.std(axis=0, ddof=1) / self.sqrtN  )
        return t
    
    
    # def teststat_mu_subtracted(self, y):
    #     return y.mean(axis=0) / (  y.std(axis=0, ddof=1) / self.sqrtN  )


# class CalculatorHotellings0D(_CalculatorOneSample):
#     def teststat_mu_subtracted(self, y):
#         m       = y.mean(axis=0)       # estimated mean
#         W       = np.cov(y.T, ddof=1)  # estimated covariance
#         T2      = self.J * m @ np.linalg.inv(W) @ m.T
#         return float(T2)
#
# class CalculatorHotellings1D(_CalculatorOneSample):
#     def _T2_onesample_singlenode(self, y):
#         if np.ma.is_masked(y):
#             T2   = 0
#         else:
#             n    = y.shape[0]      #nResponses
#             m    = y.mean(axis=0)  #mean vector
#             W    = np.cov(y.T) + eps  #covariance
#             T2   = n * m @ np.linalg.inv(W) @ m.T
#         return float(T2)
#
#     def teststat_mu_subtracted(self, y):
#         T2      = [self._T2_onesample_singlenode( y[:,i,:] )   for i in range(y.shape[1])]
#         return np.asarray(T2)





#---------------------------------------------------------------------------------
#  TWO-SAMPLE TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

class _CalculatorTwoSample(object):
    def __init__(self, n0, n1):
        self.n0m1        = n0 - 1
        self.n1m1        = n1 - 1
        self.df          = n0 + n1 - 2
    def teststat(self, y0, y1):
        pass


class CalculatorTtest2( _CalculatorTwoSample ):
    def __init__(self, n0, n1):
        super().__init__(n0, n1)
        self.sqrt01      = (1.0/n0 + 1.0/n1)**0.5

    def teststat(self, y, A):
        A      = np.asarray(A)
        y0,y1  = y[A==0], y[A==1]
        n0,n1  = y0.shape[0], y1.shape[0]
        m0,m1  = y0.mean(axis=0), y1.mean(axis=0)
        s0,s1  = y0.std(ddof=1, axis=0), y1.std(ddof=1, axis=0)
        n      = y.shape[0]
        sp     = (   (  self.n0m1*s0*s0 + self.n1m1*s1*s1  )  /  self.df   )**0.5
        t      = (m0-m1) / sp / self.sqrt01
        return t


# class CalculatorHotellings20D( _CalculatorTwoSample ):
#     def __init__(self, nA, nB):
#         super(CalculatorHotellings20D, self).__init__(nA, nB)
#         self.nABAB       = (nA * nB) / float( nA + nB )
#     def teststat(self, yA, yB):
#         mA,mB     = yA.mean(axis=0), yB.mean(axis=0)
#         WA,WB     = np.cov(yA.T), np.cov(yB.T)
#         W         = (self.nA1*WA + self.nB1*WB) / self.df + eps
#         T2        = self.nABAB  * (mB-mA) @ np.linalg.inv(W) @ (mB-mA).T
#         return float(T2)
#
# class CalculatorHotellings21D( _CalculatorTwoSample ):
#     def __init__(self, nA, nB):
#         super(CalculatorHotellings21D, self).__init__(nA, nB)
#         self.nABAB       = (nA * nB) / float( nA + nB )
#
#     def _T2_twosample_singlenode(self, yA, yB):  #at a single node:
#         if np.ma.is_masked(yA):
#             T2   = 0
#         else:
#             mA,mB    = yA.mean(axis=0), yB.mean(axis=0)  #means
#             WA,WB    = np.cov(yA.T), np.cov(yB.T)
#             W        = (self.nA1*WA + self.nB1*WB) / self.df + eps
#             T2       = self.nABAB  * (mB-mA) @ np.linalg.inv(W) @ (mB-mA).T
#         return float(T2)
#
#     def teststat(self, yA, yB):
#         T2      = [self._T2_twosample_singlenode( yA[:,i,:], yB[:,i,:] )   for i in range(yA.shape[1])]
#         return np.asarray(T2)





# class CalculatorMANOVA10D( object ):
#     def __init__(self, A, I):
#         ### counts:
#         J           = A.size           #number of responses
#         u           = np.unique(A)
#         nGroups     = u.size
#         self.n1pk   = -((J-1) - 0.5*(I + nGroups))
#         ### design matrix:
#         self.X      = np.zeros((J, nGroups))
#         for i,uu in enumerate(u):
#             self.X[A==uu, i] = 1
#         self.Xi     = np.linalg.pinv( self.X )
#         ### reduced design matrix:
#         self.X0     = np.ones((J,1))
#         self.X0i    = np.linalg.pinv( self.X0 )
#
#     def teststat(self, Y):
#         ### SS for original design:
#         b     = self.Xi @ Y
#         R     = Y - self.X @ b
#         R     = R.T @ R
#         ### SS for reduced design:
#         b0    = self.X0i @ Y
#         R0    = Y - self.X0 @ b0
#         R0    = R0.T @ R0
#         ### Wilk's lambda:
#         lam   = np.linalg.det(R) / (np.linalg.det(R0) + eps)
#         x2    = self.n1pk * log(lam)
#         return x2
#
# class CalculatorMANOVA11D( CalculatorMANOVA10D ):
#     def teststat(self, Y):
#         x2    = [CalculatorMANOVA10D.teststat(self, Y[:,i,:])   for i in range(Y.shape[1])]
#         return np.array(x2)
#






#---------------------------------------------------------------------------------
#  REGRESSION TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------



class CalculatorRegress0D(object):
    def __init__(self, x):
        self.x           = np.asarray(x, dtype=float)
        self.J           = self.x.size
        self.df          = self.J - 2     #degrees of freedom
        ### design matrix:
        self.X           = np.ones( (self.J, 2) )
        self.X[:,0]      = self.x
        self.Xi          = np.linalg.pinv(self.X)
        self.c           = [1,0]
        self.cXXc        = float(  self.c @ np.linalg.inv(self.X.T @ self.X) @ self.c  )

    def teststat(self, y, ind):
        y      = y[ind]
        b      = self.Xi @ y            #parameters
        eij    = y - self.X @ b         #residuals
        R      = eij.T @ eij            #residual sum of squares
        sigma2 = float(R) / self.df     #variance
        t      = float(self.c @ b)  /   (sigma2*self.cXXc)**0.5
        return t

class CalculatorRegress1D(CalculatorRegress0D):
    def teststat(self, y, ind):
        y      = y[ind]
        b      = np.ma.dot(self.Xi, y)        # parameters
        eij    = y - np.ma.dot(self.X, b)     # residuals
        # # previous sigma2 calculation (slow when Q get large: about 5 ms for Q=1000 and about 900 ms for Q=10000! )
        # R      = eij.T@eij              #residuals: sum of squares
        # sigma2 = np.diag(R)/df          #variance
        # new sigma2 calculation (using eigensum trick)
        diagR  = np.einsum('ij,ji->i', eij.T, eij)  # residual sum of squares (eigensum trick)
        sigma2 = diagR / self.df          #variance
        if isinstance(y, np.ma.masked_array):
            sigma2 = np.ma.masked_array(sigma2, y.mask[0])
        t      = np.array(np.ma.dot(self.c, b)).flatten()  /   ((sigma2*self.cXXc)**0.5 + eps)
        return t


# class CalculatorCCA0D(object):
#     def __init__(self, x):
#         self.x           = np.asarray(x, dtype=float)
#         self.J           = x.size
#         self.X           = x[:,np.newaxis] if x.ndim==1 else x
#         Z                = np.ones((self.J,1))
#         self.Rz          = np.eye(self.J) - Z @ np.linalg.inv(Z.T@Z) @ Z.T
#         XStar            = self.Rz @ self.X
#         self.XXXiX       = XStar  @  np.linalg.inv( XStar.T @ XStar  )  @ XStar.T
#         self.p           = 1.0   # nContrasts
#         self.r           = 1.0   # nNuisanceFactors
#         self.m           = self.J - self.p - self.r
#
#     def teststat(self, y):
#         if np.ma.is_masked(y):
#             x2     = 0
#         else:
#             ### estimate maximum canonical correlation:
#             YStar      = self.Rz @ y
#             H          = YStar.T @ self.XXXiX @ YStar / self.p
#             W          = YStar.T  @ (np.eye(self.J)  -  self.XXXiX) @ YStar  / self.m
#             F          = np.linalg.inv(W) @ H
#             ff         = np.linalg.eigvals( F )
#             fmax       = float( np.real(ff.max()) )
#             r2max      = fmax * self.p  / (self.m + fmax*self.p)
#             rmax       = r2max**0.5
#             ### compute test statistic:
#             m          = y.shape[1]  # df = m  (nComponents)
#             x2         = -(self.J - 1 - 0.5*(m+2) )  *  log( (1-rmax**2) )
#         return x2
#
#
# class CalculatorCCA1D(CalculatorCCA0D):
#
#     def teststat(self, y):
#         x2         = [super(CalculatorCCA1D, self).teststat(y[:,i,:])   for i in range(y.shape[1])]
#         return np.array(x2)








#---------------------------------------------------------------------------------
#  ANOVA TEST STATISTIC CALCULATORS
#---------------------------------------------------------------------------------

# class _CalculatorANOVAsingleF(object):
#     def teststat(self, y, A):
#         self.design = designs.ANOVA1(A)
#         model       = models.LinearModel(y, self.design.X)
#         model.fit()
#         F           = aov(model, self.design.contrasts, self.design.f_terms)[0]
#         return F.z

class _CalculatorANOVAmultiF(object):
    def teststat(self, y, A, S):
        model   = models.LinearModel(y, self.design.X)
        model.fit()
        FF      = aov(model, self.design.contrasts, self.design.f_terms)
        return [F.z for F in FF]



class CalculatorANOVA1(object):
    def __init__(self, A):
        self.design      = designs.ANOVA1(A)
        
    def teststat(self, y, A):
        self.design = designs.ANOVA1(A)
        model       = models.LinearModel(y, self.design.X)
        model.fit()
        F           = aov(model, self.design.contrasts, self.design.f_terms)[0]
        return F.z
        
class CalculatorANOVA1rm(object):
    def __init__(self, A, S):
        self.design      = designs.ANOVA1rm(A, S)
        
    def teststat(self, y, A, S):
        self.design = designs.ANOVA1rm(A, S)
        model       = models.LinearModel(y, self.design.X)
        model.fit()
        F           = aov(model, self.design.contrasts, self.design.f_terms)[0]
        return F.z

#
# class CalculatorANOVA2(_CalculatorANOVAmultiF):
#     def __init__(self, A, B):
#         self.design      = designs.ANOVA2(A, B)
# class CalculatorANOVA2nested(_CalculatorANOVAmultiF):
#     def __init__(self, A, B):
#         self.design      = designs.ANOVA2nested(A, B)
# class CalculatorANOVA2onerm(_CalculatorANOVAmultiF):
#     def __init__(self, A, B, SUBJ):
#         self.design      = designs.ANOVA2onerm(A, B, SUBJ)
# class CalculatorANOVA2rm(_CalculatorANOVAmultiF):
#     def __init__(self, A, B, SUBJ):
#         self.design      = designs.ANOVA2rm(A, B, SUBJ)
#
#
#
# class CalculatorANOVA3(_CalculatorANOVAmultiF):
#     def __init__(self, A, B, C):
#         self.design      = designs.ANOVA3(A, B, C)
# class CalculatorANOVA3nested(_CalculatorANOVAmultiF):
#     def __init__(self, A, B, C):
#         self.design      = designs.ANOVA3nested(A, B, C)
# class CalculatorANOVA3onerm(_CalculatorANOVAmultiF):
#     def __init__(self, A, B, C, SUBJ):
#         self.design      = designs.ANOVA3onerm(A, B, C, SUBJ)
# class CalculatorANOVA3tworm(_CalculatorANOVAmultiF):
#     def __init__(self, A, B, C, SUBJ):
#         self.design      = designs.ANOVA3tworm(A, B, C, SUBJ)
# class CalculatorANOVA3rm(_CalculatorANOVAmultiF):
#     def __init__(self, A, B, C, SUBJ):
#         self.design      = designs.ANOVA3rm(A, B, C, SUBJ)




