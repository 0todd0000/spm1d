
'''
Confidence intervals

If the CI cloud starting from the datum reaches the criterion line, the null hypothesis is rejected.
'''


import numpy as np
import rft1d
from .. plot import plot_ci, plot_ci_multi
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



# class ConfidenceInterval(object):
# 	'''
# 	Confidence Interval
#
# 	If the CI cloud starting from the datum reaches the criterion line, the null hypothesis is rejected.
# 	'''
# 	def __init__(self, datum, alpha, fwhm, resels, zstar, hstar, criterion=None, design=None, datumstr=None, criterionstr=None, df=(1,1)):
# 		self.Q            = datum.size
# 		self.df           = tuple(df)
# 		self.datum        = datum
# 		self.alpha        = alpha
# 		self.fwhm         = fwhm
# 		self.resels       = resels
# 		self.zstar        = zstar
# 		self.hstar        = hstar
# 		self.criterion    = criterion
# 		self.design       = design
# 		self.datumstr     = datumstr
# 		self.criterionstr = criterionstr
#
# 	def __repr__(self):
# 		s        = ''
# 		s       += 'Confidence Interval (%d%s)\n' %(100*(1-self.alpha), '%')
# 		s       += '   alpha      :  %.3f\n'       %self.alpha
# 		s       += '   df         :  %s\n'         %dflist2str(self.df)
# 		s       += '   fwhm       :  %.5f\n'       %self.fwhm
# 		s       += '   resels     :  (%d, %.5f)\n' %tuple(self.resels)
# 		s       += '   zstar      :  %.5f\n'       %self.zstar
# 		s       += '   datum      :  %s\n'         %self.datumstr
# 		s       += '   criterion  :  %s\n'         %self.criterionstr
# 		return s
#
# 	def plot(self, ax=None, x=None, linecolor='k', facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
# 		plot_ci(self, ax, x, linecolor, facecolor, edgecolor, alpha, autoset_ylim)


class _CI(object):
	'''
	Parent class for Confidence Interval objects
	'''
	alpha     = None
	spmi      = None
	mean      = None
	thresh    = None
	hstar     = None
	datum     = None
	criterion = None

	def __repr__(self):
		s        = ''
		s       += 'Confidence Interval (%d%s)\n' %(100*(1-self.alpha), '%')
		s       += '   alpha      :  %.3f\n'       %self.alpha
		s       += '   df         :  %s\n'         %dflist2str(self.spmi.df)
		s       += '   fwhm       :  %.5f\n'       %self.spmi.fwhm
		s       += '   resels     :  (%d, %.5f)\n' %self.spmi.resels
		s       += '   zstar      :  %.5f\n'       %self.spmi.zstar
		s       += '   mean       :  (1x%d) datum field\n' %self.spmi.Q
		s       += '   hstar      :  (1x%d) critical height field\n' %self.spmi.Q
		s       += '   thresh     :  (1x%d) critical threshold field\n' %self.spmi.Q
		s       += '   datum      :  %s\n'         %self.datum
		s       += '   criterion  :  %s\n'         %self.criterion
		return s

	def plot(self, ax=None, x=None, linecolor='k', facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
		plot_ci(self, ax, x, linecolor, facecolor, edgecolor, alpha, autoset_ylim)



class ConfidenceInterval(_CI):
	def __init__(self, spmi, mean, hstar, thresh, datum, criterion):
		self.alpha        = spmi.alpha
		self.spmi         = spmi
		self.mean         = mean
		self.hstar        = hstar
		self.thresh       = thresh
		self.datum        = datum
		self.criterion    = criterion

	def plot(self, ax=None, x=None, linecolor='k', facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
		plot_ci(self, ax, x, linecolor, facecolor, edgecolor, alpha, autoset_ylim)



# class ConfidenceIntervalTailCriterion(ConfidenceInterval):
# 	def __init__(self, spmi, mA, mB, criterion, hstar, datumstr, criterionstr):
# 		super(ConfidenceIntervalMulti, self).__init__(spmi, datumlist[0], None, hstar, datumstr, criterionstr)
# 		self.other     = datumlist[1]
#
# 	def plot(self, ax=None, x=None, linecolors=('k','r'), facecolors=('0.8','r'), edgecolors=('0.8','r'), alphas=0.5, autoset_ylim=True):
# 		plot_ci_multi(self, ax, x, linecolors, facecolors, edgecolors, alphas, autoset_ylim)

class ConfidenceIntervalMultiMean(ConfidenceInterval):
	def __init__(self, spmi, meanA, meanB, hstar, datum, criterion):
		self.alpha        = spmi.alpha
		self.spmi         = spmi
		self.meanA        = meanA
		self.meanB        = meanB
		self.hstar        = hstar
		self.datum        = datum
		self.criterion    = criterion
	
	def __repr__(self):
		s        = ''
		s       += 'Multi-Mean Confidence Interval (%d%s)\n' %(100*(1-self.alpha), '%')
		s       += '   alpha      :  %.3f\n'       %self.alpha
		s       += '   df         :  %s\n'         %dflist2str(self.spmi.df)
		s       += '   fwhm       :  %.5f\n'       %self.spmi.fwhm
		s       += '   resels     :  (%d, %.5f)\n' %self.spmi.resels
		s       += '   zstar      :  %.5f\n'       %self.spmi.zstar
		s       += '   meanA      :  (1x%d) datum A field\n' %self.spmi.Q
		s       += '   meanB      :  (1x%d) datum B field\n' %self.spmi.Q
		s       += '   hstar      :  (1x%d) critical height field\n' %self.spmi.Q
		s       += '   datum      :  %s\n'         %self.datum
		s       += '   criterion  :  %s\n'         %self.criterion
		return s

	def plot(self, ax=None, x=None, linecolors=('k','r'), facecolors=('0.8','r'), edgecolors=('0.8','r'), alphas=0.5, autoset_ylim=True):
		plot_ci_multi(self, ax, x, linecolors, facecolors, edgecolors, alphas, autoset_ylim)









# class CI0DOneSample(object):
# 	kind                  = 'One sample'
# 	datum                 = 'mean'
# 	criterion             = 'mu'
#
# 	def __init__(self, spmi, mean, hstar, mu=None):
# 		### main parameters:
# 		self.mean         = float(mean)
# 		self.mu           = mu
# 		### probability:
# 		self.alpha        = spmi.alpha
# 		self.df           = spmi.df
# 		self.zstar        = spmi.zstar
# 		### confidence interval:
# 		self.hstar        = hstar
# 		self.ci           = mean - hstar, mean + hstar
# 		self.h0reject     = spmi.h0reject
#
#
# 	def __repr__(self):
# 		s        = ''
# 		s       += '0D Confidence Interval (%d%s)\n'    %(100*(1-self.alpha), '%')
# 		s       += '   kind       :  %s\n'              %self.kind
# 		s       += '   datum      :  %s  (%.5f)\n'      %(self.datum, self.mean)
# 		if self.mu is not None:
# 			s   += '   criterion  :  %s  (%.5f)\n'      %(self.criterion, self.mu)
# 		s       += '   Probability\n'
# 		s       += '      alpha      :  %.3f\n'         %self.alpha
# 		s       += '      df         :  %s\n'           %dflist2str(self.df)
# 		s       += '      zstar      :  %.5f\n'         %self.zstar
# 		s       += '   Confidence interval\n'
# 		s       += '      hstar      :  %.5f\n'         %self.hstar
# 		s       += '      ci         :  (%.5f, %.5f)\n' %self.ci
# 		if self.mu is not None:
# 			s   += '      h0reject   :  %s\n'           %self.h0reject
# 		return s


class CI0DPairedSample(object):
	kind                  = 'Paired sample'
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
		s       += '0D Confidence Interval (%d%s)\n'    %(100*(1-self.alpha), '%')
		s       += '   kind       :  %s\n'              %self.kind
		s       += '   datum      :  %s  (%.5f)\n'      %(self.datum, self.mean)
		if self.mu is not None:
			s   += '   criterion  :  %s  (%.5f)\n'      %(self.criterion, self.mu)
		s       += '   Probability\n'
		s       += '      alpha      :  %.3f\n'         %self.alpha
		s       += '      df         :  %s\n'           %dflist2str(self.df)
		s       += '      zstar      :  %.5f\n'         %self.zstar
		s       += '   Confidence interval\n'
		s       += '      hstar      :  %.5f\n'         %self.hstar
		s       += '      ci         :  (%.5f, %.5f)\n' %self.ci
		if self.mu is not None:
			s   += '      h0reject   :  %s\n'           %self.h0reject
		return s


def ci_onesample(y, alpha=0.05, mu=None):
	spmi    = ttest(y, mu).inference(alpha, two_tailed=True)
	# mu      = _get_mu(mu, spmi)
	mean    = spmi.beta.flatten()  #sample mean
	mean    = mean if (mu is None) else (mean + mu)
	s       = spmi.sigma2**0.5     #sample standard deviation
	hstar   = spmi.zstar * s / y.shape[0]**0.5
	# thresh  = mu
	CIclass = ConfidenceInterval if spmi.dim==1 else CI0DOneSample
	return CIclass(spmi, mean, hstar, mu=mu)



def ci_pairedsample(yA, yB, alpha=0.05, mu=None, datum='difference', criterion='zero'):
	_check_args(mu, datum, criterion)
	ci              = ci_onesample(yA-yB, alpha, mu=mu)
	ci.datum        = datum
	ci.criterion    = criterion
	if datum != 'difference':
		mA,mB       = yA.mean(axis=0), yB.mean(axis=0)
		if criterion=='meanB':
			ci.mean      = mA
			ci.thresh    = mB
			d            = mA - mB
			ci.ci        = tuple([x+mA-d  for x in ci.ci])
		else:
			ci      = ConfidenceIntervalMultiMean(ci.spmi, mA, mB, 0.5*ci.hstar, datum, criterion)
	return ci



def ci_twosample(yA, yB, alpha=0.05, equal_var=True, datum='difference', criterion='zero'):
	_check_args(datum, criterion)
	if not equal_var:
		raise NotImplementedError('Two-sample confidence interval calculations are currently only implemented for assumed equal variance. Set "equal_var=True" to force equal variance assumption.')
	JA,JB      = yA.shape[0], yB.shape[0]
	spmi       = ttest2(yA, yB, equal_var=True).inference(alpha, two_tailed=True)
	mA,mB  = spmi.beta            #sample means
	s      = spmi.sigma2**0.5     #sample standard deviation
	hstar  = spmi.zstar * s * (1./JA + 1./JB)**0.5
	# else:
	# 	mA,mB  = yA.mean(), yB.mean()
		
	### check the CI type:
	if datum == 'difference':
		# ci     = ConfidenceInterval(d, alpha, fwhm, resels, zstar, hstar, design='TwoSample', datumstr=datum, criterionstr=criterion, df=(1,df))
		thresh = np.zeros(spmi.Q)
		ci     = ConfidenceInterval(spmi, mA-mB, hstar, thresh, 'mean', 'zero')
	else:
		if criterion=='meanB':
			ci = ConfidenceInterval(spmi, mA, hstar, mB, 'meanA', 'meanB')
		else:
			ci = ConfidenceIntervalMultiMean(spmi, mA, mB, 0.5*hstar, 'meanA', 'tailsAB')
	return ci
	




