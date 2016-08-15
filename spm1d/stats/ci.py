
'''
Confidence intervals

If the CI cloud starting from the datum reaches the criterion line, the null hypothesis is rejected.
'''


import numpy as np
import rft1d
from .. plot import plot_ci_0d, plot_ci_multisample_0d, plot_ci, plot_ci_multisample
from _spm import df2str, dflist2str
from t import ttest,ttest2


def _check_args(mu, datum, criterion):
	if (mu is not None) and not isinstance(mu, (int,float)):
		raise ValueError('"mu" must be None or a scalar')
	if not isinstance(datum, str):
		raise ValueError('"datum" must be a string')
	if not isinstance(criterion, str):
		raise ValueError('"criterion" must be a string')
	s0,s1   = datum.lower(), criterion.lower()
	if s0 not in ['difference', 'meana']:
		raise ValueError('"datum" must be one of: "difference", "meanA"')
	if s1 not in ['zero', 'meanb', 'tailsab']:
		raise ValueError('"criterion" must be one of: "zero", "meanB", "tailsAB"')
	if s0 == 'difference' and s1!='zero':
		raise ValueError('If "datum" is "difference", "criterion" must be "zero". Confidence intervals are not defined for a difference datum and a non-zero criterion.')
	if s0 == 'mean' and s1=='zero':
		raise ValueError('If "datum" is "meanA", "criterion" cannot be "zero". Confidence intervals are not defined for a mean datum and a zero criterion.')


def _get_mu(mu, spmi):
	if spmi.dim==0:
		mu     = None if mu is None else float(mu)
	elif spmi.dim==1:
		if mu is None:
			mu = np.zeros(spmi.Q)
		elif isinstance(mu, (int, float)):
			mu = mu * np.ones(spmi.Q)
		elif isinstance(mu, (list, np.ndarray)):
			mu = np.asarray(mu, dtype=float)
	return mu






class _CI0D(object):
	name                  = '0D Confidence Interval'
	dim                   = 0



class _CITwoSample0D(_CI0D):
	def __init__(self, spmi, meanA, meanB, hstar, datum='difference', mu=None):
		### main parameters:
		self.datum            = datum
		self.criterion        = mu if isinstance(mu, str) else 'mu'
		self.meanA            = float(meanA)
		self.meanB            = float(meanB)
		self.meanAB           = self.meanA - self.meanB
		self.mu               = None
		self._datum_value     = None
		self._criterion_value = None
		### probability:
		self.alpha            = spmi.alpha
		self.df               = spmi.df
		self.zstar            = spmi.zstar
		### confidence interval:
		self.istest           = mu is not None
		self.hstar            = hstar
		self.ci               = None
		self.ciA              = None
		self.ciB              = None
		self.h0reject         = spmi.h0reject
		self._set_values(mu)

	def _set_values(self, mu):
		if self.datum == 'difference':
			self._datum_value          = self.meanAB
			self._criterion_value      = mu
			self.mu                    = self._criterion_value
			self.ci                    = self.meanAB - self.hstar, self.meanAB + self.hstar
		elif self.datum == 'meanA':
			self._datum_value          = self.meanA
			if self.criterion == 'meanB':
				self._criterion_value  = self.meanB
				self.mu                = None
				self.ci                = self.meanA - self.hstar, self.meanA + self.hstar
			elif self.criterion == 'tailsAB':
				self._criterion_value  = None
				self.mu                = None
				self.ciA               = self.meanA - 0.5*self.hstar, self.meanA + 0.5*self.hstar
				self.ciB               = self.meanB - 0.5*self.hstar, self.meanB + 0.5*self.hstar
	

	def __repr__(self):
		s            = ''
		s           += '%s (%d%s)\n'                        %(self.name, 100*(1-self.alpha), '%')
		s           += '   kind          :  %s\n'              %self.kind
		s           += '   datum         :  %s  (%.5f)\n'      %(self.datum, self._datum_value)
		if self.criterion == 'tailsAB':
			s       += '   datumB        :  meanB  (%.5f)\n'   %self.meanB
		if self.istest:
			if self.criterion == 'tailsAB':
				s   += '   criterion     :  %s\n'              %self.criterion
			else:
				s   += '   criterion     :  %s  (%.5f)\n'      %(self.criterion, self._criterion_value)
		s           += '   Probability\n'
		s           += '      alpha      :  %.3f\n'         %self.alpha
		s           += '      df         :  %s\n'           %dflist2str(self.df)
		s           += '      zstar      :  %.5f\n'         %self.zstar
		if self.criterion=='tailsAB':
			s       += '   Confidence intervals\n'
			s       += '      hstar      :  %.5f\n'         %self.hstar
			s       += '      ciA        :  (%.5f, %.5f)\n' %self.ciA
			s       += '      ciB        :  (%.5f, %.5f)\n' %self.ciB
			ios      = 'do not overlap' if self.h0reject else 'overlap'
			s       += '      h0reject   :  %s (CIs %s)\n' %(self.h0reject, ios)
		else:
			s       += '   Confidence interval\n'
			s       += '      hstar      :  %.5f\n'         %self.hstar
			s       += '      ci         :  (%.5f, %.5f)\n' %self.ci
			if self.istest:
				ios  = 'outside' if self.h0reject else 'inside'
				s   += '      h0reject   :  %s (%s %s ci)\n' %(self.h0reject, self.criterion, ios)
		return s


	def plot(self, ax=None):
		plot_ci_multisample_0d(self, ax)



class CIOneSample0D(_CI0D):
	kind                  = 'One sample'
	datum                 = 'mean'
	criterion             = 'mu'
	
	def __init__(self, spmi, mean, hstar, mu=None):
		### main parameters:
		self.mean         = float(mean)
		self.mu           = mu
		### probability:
		self.alpha        = spmi.alpha
		self.df           = spmi.df
		self.zstar        = spmi.zstar
		### confidence interval:
		self.hstar        = hstar
		self.ci           = mean - hstar, mean + hstar
		self.h0reject     = spmi.h0reject


	def __repr__(self):
		s        = ''
		s       += '%s (%d%s)\n'                         %(self.name, 100*(1-self.alpha), '%')
		s       += '   kind          :  %s\n'            %self.kind
		s       += '   datum         :  %s  (%.5f)\n'    %(self.datum, self.mean)
		if self.mu is not None:
			s   += '   criterion     :  %s  (%.5f)\n'    %(self.criterion, self.mu)
		s       += '   Probability\n'
		s       += '      alpha      :  %.3f\n'          %self.alpha
		s       += '      df         :  %s\n'            %dflist2str(self.df)
		s       += '      zstar      :  %.5f\n'          %self.zstar
		s       += '   Confidence interval\n'
		s       += '      hstar      :  %.5f\n'          %self.hstar
		s       += '      ci         :  (%.5f, %.5f)\n'  %self.ci
		if self.mu is not None:
			ios  = 'outside' if self.h0reject else 'inside'
			s   += '      mu         :  %.5f\n'          %self.mu
			s   += '      h0reject   :  %s (mu %s ci)\n' %(self.h0reject, ios)
		return s
		
	def plot(self, ax=None):
		plot_ci_0d(self, ax)








class CIPairedSample0D(_CITwoSample0D):
	kind                  = 'Paired sample'
class CITwoSample0D(_CITwoSample0D):
	kind                  = 'Two sample'






















class _CI1D(object):
	name                  = '1D Confidence Interval'
	dim                   = 1



class _CITwoSample1D(_CI1D):
	def __init__(self, spmi, meanA, meanB, hstar, datum='difference', mu=None):
		### main parameters:
		self.Q                = meanA.size
		self.datum            = datum
		self.criterion        = mu if isinstance(mu, str) else 'mu'
		self.meanA            = meanA
		self.meanB            = meanB
		self.meanAB           = self.meanA - self.meanB
		self.mu               = None
		self._datum_value     = None
		self._criterion_value = None
		### probability:
		self.alpha            = spmi.alpha
		self.df               = spmi.df
		self.fwhm             = spmi.fwhm
		self.resels           = spmi.resels
		self.zstar            = spmi.zstar
		### confidence interval:
		self.istest           = mu is not None
		self.hstar            = hstar
		self.ci               = None
		self.ciA              = None
		self.ciB              = None
		self.h0reject         = spmi.h0reject
		self._set_values(mu)

	def _set_values(self, mu):
		if self.datum == 'difference':
			self._datum_value          = self.meanAB
			self._criterion_value      = mu
			self.mu                    = self._criterion_value
			self.ci                    = np.array([self.meanAB - self.hstar, self.meanAB + self.hstar])
		elif self.datum == 'meanA':
			self._datum_value          = self.meanA
			if self.criterion == 'meanB':
				self._criterion_value  = self.meanB
				self.mu                = None
				self.ci                = np.array([self.meanA - self.hstar, self.meanA + self.hstar])
			elif self.criterion == 'tailsAB':
				self._criterion_value  = None
				self.mu                = None
				self.ciA               = np.array([self.meanA - 0.5*self.hstar, self.meanA + 0.5*self.hstar])
				self.ciB               = np.array([self.meanB - 0.5*self.hstar, self.meanB + 0.5*self.hstar])
	

	def __repr__(self):
		fieldstr     = '(1x%d) field' %self.Q
		fieldstr_ci  = '(2x%d) field' %self.Q
		s            = ''
		s           += '%s (%d%s)\n'                        %(self.name, 100*(1-self.alpha), '%')
		s           += '   kind          :  %s\n'           %self.kind
		
		if self.criterion == 'tailsAB':
			s       += '   datumA        :  meanA [%s]\n'   %fieldstr
			s       += '   datumB        :  meanB [%s]\n'   %fieldstr
		else:
			s       += '   datum         :  %s [%s]\n'      %(self.datum, fieldstr)
		if self.istest:
			if self.criterion == 'tailsAB':
				s   += '   criterion     :  %s\n'           %self.criterion
			else:
				s   += '   criterion     :  %s  [%s]\n'     %(self.criterion, fieldstr)
		s           += '   Probability\n'
		s           += '      alpha      :  %.3f\n'         %self.alpha
		s           += '      df         :  %s\n'           %dflist2str(self.df)
		s           += '      fwhm       :  %.5f\n'         %self.fwhm
		s           += '      resels     :  (%.5f, %.5f)\n' %self.resels
		s           += '      zstar      :  %.5f\n'         %self.zstar
		if self.criterion=='tailsAB':
			s       += '   Confidence intervals\n'
			s       += '      hstar      :  %s\n'           %fieldstr
			s       += '      ciA        :  %s\n'           %fieldstr_ci
			s       += '      ciB        :  %s\n'           %fieldstr_ci
			ios      = 'diverge' if self.h0reject else 'do not diverge'
			s       += '      h0reject   :  %s (CIs %s)\n' %(self.h0reject, ios)
		else:
			s       += '   Confidence interval\n'
			s       += '      hstar      :  %s\n'           %fieldstr
			s       += '      ci         :  %s\n'           %fieldstr_ci
			if self.istest:
				ios  = 'outside' if self.h0reject else 'inside'
				s   += '      h0reject   :  %s (%s %s ci)\n' %(self.h0reject, self.criterion, ios)
		return s


	def plot(self, ax=None):
		plot_ci_multisample(self, ax=None, x=None, linecolors=('k','b'), facecolors=('0.8','b'), edgecolors=('0.4','b'), alphas=(0.5,0.5), autoset_ylim=True)




class CIOneSample1D(_CI1D):
	kind                  = 'One sample'
	datum                 = 'mean'
	criterion             = 'mu'
	
	def __init__(self, spmi, mean, hstar, mu=None):
		### main parameters:
		self.Q            = mean.size
		self.mean         = mean
		self.mu           = mu
		self.isscalarmu   = isinstance(mu, (int,float))
		### probability:
		self.alpha        = spmi.alpha
		self.df           = spmi.df
		self.fwhm         = spmi.fwhm
		self.resels           = spmi.resels
		self.zstar        = spmi.zstar
		### confidence interval:
		self.hstar        = hstar
		self.ci           = np.asarray([mean - hstar, mean + hstar])
		self.h0reject     = spmi.h0reject


	def __repr__(self):
		s        = ''
		s       += '%s (%d%s)\n'                         %(self.name, 100*(1-self.alpha), '%')
		s       += '   kind          :  %s\n'            %self.kind
		s       += '   datum         :  (1x%d) field\n'  %self.Q
		if self.mu is not None:
			if self.isscalarmu:
				s   += '   criterion     :  %s  (%.5f)\n'    %(self.criterion, self.mu)
			else:
				s   += '   criterion     :  %s  [(1x%d) field]\n'    %(self.criterion, self.Q)
		s       += '   Probability\n'
		s       += '      alpha      :  %.3f\n'          %self.alpha
		s       += '      df         :  %s\n'            %dflist2str(self.df)
		s       += '      fwhm       :  %.5f\n'          %self.fwhm
		s       += '      resels     :  (%.5f, %.5f)\n'  %self.resels
		s       += '      zstar      :  %.5f\n'          %self.zstar
		s       += '   Confidence interval\n'
		s       += '      hstar      :  (1x%d) field\n'  %self.Q
		s       += '      ci         :  (2x%d) field\n'  %self.Q
		if self.mu is not None:
			ios  = 'outside' if self.h0reject else 'not outside'
			if self.isscalarmu:
				s   += '      mu         :  %.5f\n'          %self.mu
			else:
				s   += '      mu         :  (1x%d) field\n'  %self.Q
			s   += '      h0reject   :  %s (mu %s ci)\n' %(self.h0reject, ios)
		return s
		
	def plot(self, ax=None, x=None, linecolor='k', facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
		plot_ci(self, ax=ax, x=x, linecolor=linecolor, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, autoset_ylim=autoset_ylim)



class CIPairedSample1D(_CITwoSample1D):
	kind                  = 'Paired sample'
class CITwoSample1D(_CITwoSample1D):
	kind                  = 'Two sample'







def ci_onesample(y, alpha=0.05, mu=None):
	spmi    = ttest(y, mu).inference(alpha, two_tailed=True)
	mean    = spmi.beta.flatten()  #sample mean
	mean    = mean if (mu is None) else (mean + mu)
	s       = spmi.sigma2**0.5     #sample standard deviation
	hstar   = spmi.zstar * s / y.shape[0]**0.5
	CIClass = CIOneSample1D if spmi.dim==1 else CIOneSample0D
	return CIClass(spmi, mean, hstar, mu=mu)


def ci_pairedsample(yA, yB, alpha=0.05, datum='difference', mu=None):
	if isinstance(mu, str):
		spmi = ttest(yA-yB, 0).inference(alpha, two_tailed=True)
	else:
		spmi = ttest(yA-yB, mu).inference(alpha, two_tailed=True)
	meanAB   = spmi.beta.flatten()                #mean difference
	mA,mB    = yA.mean(axis=0), yB.mean(axis=0)   #sample means
	s        = spmi.sigma2**0.5                   #sample standard deviation
	hstar    = spmi.zstar * s / yA.shape[0]**0.5  #CI height
	CIClass  = CIPairedSample1D if spmi.dim==1 else CIPairedSample0D
	return CIClass(spmi, mA, mB, hstar, datum, mu)


def ci_twosample(yA, yB, alpha=0.05, equal_var=True, datum='difference', mu=None):
	if equal_var is not True:
		raise NotImplementedError('Two-sample confidence interval calculations are currently implemented only for assumed equal variance. Set "equal_var=True" to force an equal variance assumption.')
	if isinstance(mu, str):
		spmi   = ttest2(yA, yB, equal_var=True).inference(alpha, two_tailed=True)
	else:
		spmi   = ttest2(yA, yB, equal_var=True).inference(alpha, two_tailed=True)
	JA,JB      = yA.shape[0], yB.shape[0]
	mA,mB      = spmi.beta            #sample means
	s          = spmi.sigma2**0.5     #sample standard deviation
	hstar      = spmi.zstar * s * (1./JA + 1./JB)**0.5
	CIClass    = CITwoSample1D if spmi.dim==1 else CITwoSample0D
	return CIClass(spmi, mA, mB, hstar, datum, mu)




