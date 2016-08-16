
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



class _CI(object):
	### summary variables:
	name             = None    #confidence interval name ("0D CI" or "1D CI")
	dim              = None    #data dimensionality (0 or 1)
	kind             = None    #type of confidence interval (one-, paried- or two-sample)
	### means, datum and criteria:
	criterion_type   = None    #criterion type (string)
	criterion_value  = None    #float or 1D array
	criterion        = None    #tuple: (criterion_type, criterion_value)
	datum_type       = None    #datum type (string)
	datum_value      = None    #float or 1D array
	datum            = None    #tuple: (datum_type, datum_value)
	nMeans           = None    #number of means (1 or 2)
	mu               = None    #datum  (if applicable)
	### probability:
	alpha            = None    #Type I error rate
	df               = None    #degrees of freedom
	zstar            = None    #critical test statistic value
	### confidence interval:
	hstar            = None    #CI height
	h0reject         = None    #null hypothesis rejection decision
	### booleans:
	ismultimean      = None    #is a multi-mean CI
	isscalarmu       = None    #is mu a scalar
	istest           = None    #is a hypothesis test
	

	# def __repr__(self):
	# 	s        = ''
	# 	s       += '%s (%d%s)\n'                         %(self.name, 100*(1-self.alpha), '%')
	# 	s       += '   kind          :  %s\n'            %self.kind
	# 	s       += '   datum         :  (1x%d) field\n'  %self.Q
	# 	if self.mu is not None:
	# 		if self.isscalarmu:
	# 			s   += '   criterion     :  %s  (%.5f)\n'    %(self.criterion, self.mu)
	# 		else:
	# 			s   += '   criterion     :  %s  [(1x%d) field]\n'    %(self.criterion, self.Q)
	# 	s       += '   Probability\n'
	# 	s       += '      alpha      :  %.3f\n'          %self.alpha
	# 	s       += '      df         :  %s\n'            %dflist2str(self.df)
	# 	s       += '      fwhm       :  %.5f\n'          %self.fwhm
	# 	s       += '      resels     :  (%.5f, %.5f)\n'  %self.resels
	# 	s       += '      zstar      :  %.5f\n'          %self.zstar
	# 	s       += '   Confidence interval\n'
	# 	s       += '      hstar      :  (1x%d) field\n'  %self.Q
	# 	s       += '      ci         :  (2x%d) field\n'  %self.Q
	# 	if self.mu is not None:
	# 		ios  = 'outside' if self.h0reject else 'not outside'
	# 		if self.isscalarmu:
	# 			s   += '      mu         :  %.5f\n'          %self.mu
	# 		else:
	# 			s   += '      mu         :  (1x%d) field\n'  %self.Q
	# 		s   += '      h0reject   :  %s (mu %s ci)\n' %(self.h0reject, ios)
	# 	return s


	def __repr__(self):
		### build repr string:
		s            = ''
		s           += '%s (%s)\n'                             %(self.name, self.get_percent(asstr=True))
		s           += '   kind          :  %s\n'              %self.kind
		s           += '   datum         :  %s  %s\n'          %(self.datum_type, self.get_datum_value(asstr=True, with_brackets=True))
		if self.criterion_type == 'tailsAB':
			s       += '   datumB        :  meanB  (%.5f)\n'   %self.meanB
		if self.istest:
			if self.criterion_type == 'tailsAB':
				s   += '   criterion     :  %s\n'              %self.criterion_type
			else:
				s   += '   criterion     :  %s  %s\n'          %(self.criterion_type, self.get_criterion_value(asstr=True, with_brackets=True))
		s           += '   Probability\n'
		s           += '      alpha      :  %.3f\n'            %self.alpha
		s           += '      df         :  %s\n'              %dflist2str(self.df)
		s           += '      zstar      :  %.5f\n'            %self.zstar
		if self.criterion_type =='tailsAB':
			s       += '   Confidence intervals\n'
			s       += '      hstar      :  %.5f\n'            %self.hstar
			s       += '      ciA        :  (%.5f, %.5f)\n'    %self.ciA
			s       += '      ciB        :  (%.5f, %.5f)\n'    %self.ciB
			s       += '      h0reject   :  %s (CIs %s)\n'     %(self.h0reject, self.get_h0rejection_decision_reason())
		else:
			s       += '   Confidence interval\n'
			s       += '      hstar      :  %s\n'              %self.get_hstar(asstr=True)
			s       += '      ci         :  %s\n'              %self.get_ci(asstr=True)
			if self.istest:
				ios  = 'outside' if self.h0reject else 'inside'
				s   += '      h0reject   :  %s (%s %s ci)\n' %(self.h0reject, self.criterion_type, ios)
		return s
	
	def _assemble_datum_criterion_pairs(self):
		self.datum       = self.datum_type, self.datum_value
		self.criterion   = self.criterion_type, self.criterion_value
	
	def _get_value(self, x, asstr=False, with_brackets=False):
		if asstr:
			if (self.dim==0) or (np.size(x)==1):
				x  = '(%.5f)'%x if with_brackets else '%.5f'%x
			else:
				x  = self.get_field_str(1, with_brackets)
		return x

	def get_ci(self, asstr=False, with_brackets=False):
		x      = self.ci
		if asstr:
			if self.dim==0:
				x  = '(%.5f, %.5f)' %x
			else:
				x  = self.get_field_str(2, with_brackets)
		return x
	
	def get_criterion_value(self, asstr=False, with_brackets=False):
		return self._get_value(self.criterion_value, asstr, with_brackets)

	def get_datum_value(self, asstr=False, with_brackets=False):
		return self._get_value(self.datum_value, asstr, with_brackets)

	def get_h0rejection_decision_reason(self):
		return 'do not overlap' if self.h0reject else 'overlap'
	
	def get_hstar(self, asstr=False, with_brackets=False):
		return self._get_value(self.hstar, asstr, with_brackets)

	def get_percent(self, asstr=False):
		x       = 100 * (1-self.alpha)
		if asstr:
			x   = '%.1f%s' %(x, '%')
		return x






class _CI0D(_CI):
	name             = '0D Confidence Interval'
	dim              = 0

class _CI1D(_CI):
	name             = '1D Confidence Interval'
	dim              = 1
	Q                = None    #number of field nodes
	fwhm             = None    #field smoothness
	resels           = None    #resel counts
	
	def get_field_str(self, n=1, with_brackets=False):
		x            = '(%dx%d) field'  %(n, self.Q)
		if with_brackets:
			x        = '[%s]' %x
		return x

class _CIOneSample(_CI):
	kind             = 'One sample'
	nMeans           = 1
	ismultimean      = False
	mean             = None    #primary mean
	ci               = None    #confidence interval
	datum_type       = 'mean'
	criterion_type   = 'mu'
	
	def __init__(self, spmi, mean, hstar, mu=None):
		### main parameters:
		self.mean            = mean if self.dim==1 else float(mean)
		self.mu              = mu
		### probability:
		self.alpha           = spmi.alpha
		self.df              = spmi.df
		self.zstar           = spmi.zstar
		self.h0reject        = spmi.h0reject
		### confidence interval:
		self.hstar           = hstar
		self.ci              = self.mean - hstar, self.mean + hstar
		### organizational attributes (redundant):
		self.isscalarmu      = isinstance(mu, (int,float))
		self.istest          = mu is not None
		self.datum_value     = self.mean
		self.criterion_value = self.mu
		self._assemble_datum_criterion_pairs()
	


class _CIMultiMean(_CI):
	nMeans           = 2
	ismultimean      = True
	meanA            = None    #primary mean
	meanB            = None    #secondary mean
	meanAB           = None    #mean difference (A-B)
	ciA              = None    #primary confidence interval
	ciB              = None    #secondary confidence interval
	
	def __init__(self, spmi, meanA, meanB, hstar, datum='difference', mu=None):
		### main parameters:
		self.meanA           = meanA if self.dim==1 else float(meanA)
		self.meanB           = meanB if self.dim==1 else float(meanB)
		self.meanAB          = self.meanA - self.meanB
		### probability:
		self.alpha           = spmi.alpha
		self.df              = spmi.df
		self.zstar           = spmi.zstar
		self.h0reject        = spmi.h0reject
		### confidence interval:
		self.hstar           = hstar
		### organizational attributes (redundant):
		self.isscalarmu      = isinstance(mu, (int,float))
		self._set_values(datum, mu)
		self._assemble_datum_criterion_pairs()
		
		
	def _set_values(self, datum, mu):
		self.ciA             = self.meanA - hstar, self.meanA + hstar
		
		
		if datum == 'difference':
			self.datum_value           = self.meanAB
			self.criterion_value       = mu
			self.mu                    = self._criterion_value
			self.ci                    = self.meanAB - self.hstar, self.meanAB + self.hstar
			self.istest                = mu is not None
		elif datum == 'meanA':
			self.istest                = True
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


	

class _CIPairedSample(_CIMultiMean):
	kind             = 'Paired sample'
class _CITwoSample(_CIMultiMean):
	kind             = 'Two sample'





class CIOneSample0D(_CI0D, _CIOneSample):
	def plot(self, ax=None):
		plot_ci_0d(self, ax)

class CIOneSample1D(_CI1D, _CIOneSample):
	def __init__(self, spmi, mean, hstar, mu=None):
		super(CIOneSample1D, self).__init__(spmi, mean, hstar, mu)
		self.Q            = mean.size
		self.fwhm         = spmi.fwhm
		self.resels       = spmi.resels
		self.ci           = np.asarray(self.ci)

	def plot(self, ax=None, x=None, linecolor='k', facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
		plot_ci(self, ax=ax, x=x, linecolor=linecolor, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, autoset_ylim=autoset_ylim)


class CIPairedSample0D(_CI0D, _CIPairedSample):
	pass
class CITwoSample0D(_CI0D, _CITwoSample):
	pass








def ci_onesample(y, alpha=0.05, mu=None):
	spmi    = ttest(y, mu).inference(alpha, two_tailed=True)
	mean    = spmi.beta.flatten()  #sample mean
	mean    = mean if (mu is None) else (mean + mu)
	s       = spmi.sigma2**0.5     #sample standard deviation
	hstar   = spmi.zstar * s / y.shape[0]**0.5
	CIClass = CIOneSample1D if spmi.dim==1 else CIOneSample0D
	# CIClass = CIOneSample0D
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
	# CIClass  = CIPairedSample1D if spmi.dim==1 else CIPairedSample0D
	CIClass  = CIPairedSample0D
	return CIClass(spmi, mA, mB, hstar, datum, mu)


def ci_twosample():
	pass



# def ci_twosample(yA, yB, alpha=0.05, equal_var=True, datum='difference', mu=None):
# 	if equal_var is not True:
# 		raise NotImplementedError('Two-sample confidence interval calculations are currently implemented only for assumed equal variance. Set "equal_var=True" to force an equal variance assumption.')
# 	if isinstance(mu, str):
# 		spmi   = ttest2(yA, yB, equal_var=True).inference(alpha, two_tailed=True)
# 	else:
# 		spmi   = ttest2(yA, yB, equal_var=True).inference(alpha, two_tailed=True)
# 	JA,JB      = yA.shape[0], yB.shape[0]
# 	mA,mB      = spmi.beta            #sample means
# 	s          = spmi.sigma2**0.5     #sample standard deviation
# 	hstar      = spmi.zstar * s * (1./JA + 1./JB)**0.5
# 	CIClass    = CITwoSample1D if spmi.dim==1 else CITwoSample0D
# 	return CIClass(spmi, mA, mB, hstar, datum, mu)








#
# class _CITwoSample0D(_CI0D):
# 	def __init__(self, spmi, meanA, meanB, hstar, datum='difference', mu=None):
# 		### main parameters:
# 		self.datum            = datum
# 		self.criterion        = mu if isinstance(mu, str) else 'mu'
# 		self.meanA            = float(meanA)
# 		self.meanB            = float(meanB)
# 		self.meanAB           = self.meanA - self.meanB
# 		self.mu               = None
# 		self._datum_value     = None
# 		self._criterion_value = None
# 		### probability:
# 		self.alpha            = spmi.alpha
# 		self.df               = spmi.df
# 		self.zstar            = spmi.zstar
# 		### confidence interval:
# 		self.istest           = mu is not None
# 		self.hstar            = hstar
# 		self.ci               = None
# 		self.ciA              = None
# 		self.ciB              = None
# 		self.h0reject         = spmi.h0reject
# 		self._set_values(mu)
#
# 	def _set_values(self, mu):
# 		if self.datum == 'difference':
# 			self._datum_value          = self.meanAB
# 			self._criterion_value      = mu
# 			self.mu                    = self._criterion_value
# 			self.ci                    = self.meanAB - self.hstar, self.meanAB + self.hstar
# 		elif self.datum == 'meanA':
# 			self._datum_value          = self.meanA
# 			if self.criterion == 'meanB':
# 				self._criterion_value  = self.meanB
# 				self.mu                = None
# 				self.ci                = self.meanA - self.hstar, self.meanA + self.hstar
# 			elif self.criterion == 'tailsAB':
# 				self._criterion_value  = None
# 				self.mu                = None
# 				self.ciA               = self.meanA - 0.5*self.hstar, self.meanA + 0.5*self.hstar
# 				self.ciB               = self.meanB - 0.5*self.hstar, self.meanB + 0.5*self.hstar
#
#
# 	# def __repr__(self):
# 	# 	s            = ''
# 	# 	s           += '%s (%d%s)\n'                        %(self.name, 100*(1-self.alpha), '%')
# 	# 	s           += '   kind          :  %s\n'              %self.kind
# 	# 	s           += '   datum         :  %s  (%.5f)\n'      %(self.datum, self._datum_value)
# 	# 	if self.criterion == 'tailsAB':
# 	# 		s       += '   datumB        :  meanB  (%.5f)\n'   %self.meanB
# 	# 	if self.istest:
# 	# 		if self.criterion == 'tailsAB':
# 	# 			s   += '   criterion     :  %s\n'              %self.criterion
# 	# 		else:
# 	# 			s   += '   criterion     :  %s  (%.5f)\n'      %(self.criterion, self._criterion_value)
# 	# 	s           += '   Probability\n'
# 	# 	s           += '      alpha      :  %.3f\n'         %self.alpha
# 	# 	s           += '      df         :  %s\n'           %dflist2str(self.df)
# 	# 	s           += '      zstar      :  %.5f\n'         %self.zstar
# 	# 	if self.criterion=='tailsAB':
# 	# 		s       += '   Confidence intervals\n'
# 	# 		s       += '      hstar      :  %.5f\n'         %self.hstar
# 	# 		s       += '      ciA        :  (%.5f, %.5f)\n' %self.ciA
# 	# 		s       += '      ciB        :  (%.5f, %.5f)\n' %self.ciB
# 	# 		ios      = 'do not overlap' if self.h0reject else 'overlap'
# 	# 		s       += '      h0reject   :  %s (CIs %s)\n' %(self.h0reject, ios)
# 	# 	else:
# 	# 		s       += '   Confidence interval\n'
# 	# 		s       += '      hstar      :  %.5f\n'         %self.hstar
# 	# 		s       += '      ci         :  (%.5f, %.5f)\n' %self.ci
# 	# 		if self.istest:
# 	# 			ios  = 'outside' if self.h0reject else 'inside'
# 	# 			s   += '      h0reject   :  %s (%s %s ci)\n' %(self.h0reject, self.criterion, ios)
# 	# 	return s
#
#
# 	def plot(self, ax=None):
# 		plot_ci_multisample_0d(self, ax)









#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# class _CITwoSample1D(_CI1D):
# 	def __init__(self, spmi, meanA, meanB, hstar, datum='difference', mu=None):
# 		### main parameters:
# 		self.Q                = meanA.size
# 		self.datum            = datum
# 		self.criterion        = mu if isinstance(mu, str) else 'mu'
# 		self.meanA            = meanA
# 		self.meanB            = meanB
# 		self.meanAB           = self.meanA - self.meanB
# 		self.mu               = None
# 		self._datum_value     = None
# 		self._criterion_value = None
# 		### probability:
# 		self.alpha            = spmi.alpha
# 		self.df               = spmi.df
# 		self.fwhm             = spmi.fwhm
# 		self.resels           = spmi.resels
# 		self.zstar            = spmi.zstar
# 		### confidence interval:
# 		self.istest           = mu is not None
# 		self.hstar            = hstar
# 		self.ci               = None
# 		self.ciA              = None
# 		self.ciB              = None
# 		self.h0reject         = spmi.h0reject
# 		self._set_values(mu)
#
# 	def _set_values(self, mu):
# 		if self.datum == 'difference':
# 			self._datum_value          = self.meanAB
# 			self._criterion_value      = mu
# 			self.mu                    = self._criterion_value
# 			self.ci                    = np.array([self.meanAB - self.hstar, self.meanAB + self.hstar])
# 		elif self.datum == 'meanA':
# 			self._datum_value          = self.meanA
# 			if self.criterion == 'meanB':
# 				self._criterion_value  = self.meanB
# 				self.mu                = None
# 				self.ci                = np.array([self.meanA - self.hstar, self.meanA + self.hstar])
# 			elif self.criterion == 'tailsAB':
# 				self._criterion_value  = None
# 				self.mu                = None
# 				self.ciA               = np.array([self.meanA - 0.5*self.hstar, self.meanA + 0.5*self.hstar])
# 				self.ciB               = np.array([self.meanB - 0.5*self.hstar, self.meanB + 0.5*self.hstar])
#
#
# 	def __repr__(self):
# 		fieldstr     = '(1x%d) field' %self.Q
# 		fieldstr_ci  = '(2x%d) field' %self.Q
# 		s            = ''
# 		s           += '%s (%d%s)\n'                        %(self.name, 100*(1-self.alpha), '%')
# 		s           += '   kind          :  %s\n'           %self.kind
#
# 		if self.criterion == 'tailsAB':
# 			s       += '   datumA        :  meanA [%s]\n'   %fieldstr
# 			s       += '   datumB        :  meanB [%s]\n'   %fieldstr
# 		else:
# 			s       += '   datum         :  %s [%s]\n'      %(self.datum, fieldstr)
# 		if self.istest:
# 			if self.criterion == 'tailsAB':
# 				s   += '   criterion     :  %s\n'           %self.criterion
# 			else:
# 				s   += '   criterion     :  %s  [%s]\n'     %(self.criterion, fieldstr)
# 		s           += '   Probability\n'
# 		s           += '      alpha      :  %.3f\n'         %self.alpha
# 		s           += '      df         :  %s\n'           %dflist2str(self.df)
# 		s           += '      fwhm       :  %.5f\n'         %self.fwhm
# 		s           += '      resels     :  (%.5f, %.5f)\n' %self.resels
# 		s           += '      zstar      :  %.5f\n'         %self.zstar
# 		if self.criterion=='tailsAB':
# 			s       += '   Confidence intervals\n'
# 			s       += '      hstar      :  %s\n'           %fieldstr
# 			s       += '      ciA        :  %s\n'           %fieldstr_ci
# 			s       += '      ciB        :  %s\n'           %fieldstr_ci
# 			ios      = 'diverge' if self.h0reject else 'do not diverge'
# 			s       += '      h0reject   :  %s (CIs %s)\n' %(self.h0reject, ios)
# 		else:
# 			s       += '   Confidence interval\n'
# 			s       += '      hstar      :  %s\n'           %fieldstr
# 			s       += '      ci         :  %s\n'           %fieldstr_ci
# 			if self.istest:
# 				ios  = 'outside' if self.h0reject else 'inside'
# 				s   += '      h0reject   :  %s (%s %s ci)\n' %(self.h0reject, self.criterion, ios)
# 		return s
#
#
# 	def plot(self, ax=None):
# 		plot_ci_multisample(self, ax=None, x=None, linecolors=('k','b'), facecolors=('0.8','b'), edgecolors=('0.4','b'), alphas=(0.5,0.5), autoset_ylim=True)
#
#

# class CIPairedSample1D(_CITwoSample1D):
# 	kind                  = 'Paired sample'
# class CITwoSample1D(_CITwoSample1D):
# 	kind                  = 'Two sample'
#
#

#

