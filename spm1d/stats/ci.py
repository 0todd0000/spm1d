
'''
Confidence intervals
'''
import numpy as np
import rft1d
from .. plot import plot_ci, plot_ci_multi
from _spm import df2str, dflist2str




class ConfidenceInterval(object):
	'''
	Confidence Interval 
	
	If the CI cloud starting from the datum reaches the criterion line, the null hypothesis is rejected.
	'''
	def __init__(self, datum, alpha, fwhm, resels, zstar, hstar, criterion=None, design=None, datumstr=None, criterionstr=None, df=(1,1)):
		self.Q            = datum.size
		self.df           = tuple(df)
		self.datum        = datum
		self.alpha        = alpha
		self.fwhm         = fwhm
		self.resels       = resels
		self.zstar        = zstar
		self.hstar        = hstar
		self.criterion    = criterion
		self.design       = design
		self.datumstr     = datumstr
		self.criterionstr = criterionstr

	def __repr__(self):
		s        = ''
		s       += 'Confidence Interval (%d%s)\n' %(100*(1-self.alpha), '%')
		s       += '   alpha      :  %.3f\n'       %self.alpha
		s       += '   df         :  %s\n'         %dflist2str(self.df)
		s       += '   fwhm       :  %.5f\n'       %self.fwhm
		s       += '   resels     :  (%d, %.5f)\n' %tuple(self.resels)
		s       += '   zstar      :  %.5f\n'       %self.zstar
		s       += '   datum      :  %s\n'         %self.datumstr
		s       += '   criterion  :  %s\n'         %self.criterionstr
		return s

	def plot(self, ax=None, x=None, linecolor='k', facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
		plot_ci(self, ax, x, linecolor, facecolor, edgecolor, alpha, autoset_ylim)



class ConfidenceIntervalMulti(ConfidenceInterval):
	def __init__(self, datumlist, alpha, fwhm, resels, zstar, hstar, design=None, datumstr=None, criterionstr=None, df=(1,1)):
		super(ConfidenceIntervalMulti, self).__init__(datumlist[0], alpha, fwhm, resels, zstar, hstar, None, design, datumstr, criterionstr, df)
		self.other     = datumlist[1]
		
	def plot(self, ax=None, x=None, linecolors=('k','r'), facecolors=('0.8','r'), edgecolors=('0.8','r'), alphas=0.5, autoset_ylim=True):
		plot_ci_multi(self, ax, x, linecolors, facecolors, edgecolors, alphas, autoset_ylim)





def _check_datum_criterion_strings(datum, criterion):
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





def ci_onesample(y, alpha=0.05):
	J,Q        = y.shape
	m,s        = y.mean(axis=0), y.std(axis=0, ddof=1)
	residuals  = y - m
	fwhm       = rft1d.geom.estimate_fwhm(residuals)
	resels     = rft1d.geom.resel_counts(residuals, fwhm, element_based=False)
	zstar      = rft1d.t.isf_resels(0.5*alpha, J-1, resels, withBonf=True, nNodes=Q)
	hstar      = zstar * s / J**0.5
	return ConfidenceInterval(m, alpha, fwhm, resels, zstar, hstar, design='OneSample', datumstr='mean', criterionstr='zero', df=(1,J-1))


def ci_pairedsample(yA, yB, alpha=0.05, datum='difference', criterion='zero'):
	_check_datum_criterion_strings(datum, criterion)
	ci              = ci_onesample( yA - yB , alpha )
	ci.design       = 'PairedSample'
	ci.datumstr     = datum
	ci.criterionstr = criterion
	if datum != 'difference':
		if criterion=='meanB':
			ci.datum     = yA.mean(axis=0)
			ci.criterion = yB.mean(axis=0)
		else:
			dlist        = [yA.mean(axis=0), yB.mean(axis=0)]
			ci           = ConfidenceIntervalMulti(dlist, alpha, ci.fwhm, ci.resels, ci.zstar, 0.5*ci.hstar, design=ci.design, datumstr=datum, criterionstr=criterion, df=ci.df)
	return ci




def ci_twosample(yA, yB, alpha=0.05, equal_var=True, datum='difference', criterion='zero'):
	_check_datum_criterion_strings(datum, criterion)
	if not equal_var:
		raise NotImplementedError('Two-sample confidence interval calculations are currently only implemented for assumed equal variance. Set "equal_var=True" to force equal variance assumption.')
	JA,Q       = yA.shape
	JB         = yB.shape[0]
	df         = float(JA + JB - 2)
	### compute means and standard deviations:
	mA,mB      = yA.mean(axis=0), yB.mean(axis=0)
	d          = mA - mB  #mean difference
	sA,sB      = yA.std(axis=0, ddof=1), yB.std(axis=0, ddof=1)
	sPooled    = (   (  (JA-1)*sA*sA + (JB-1)*sB*sB  )  /  df   )**0.5
	### assemble residuals and estimate smoothness:
	rA,rB      = yA - mA, yB - mB
	residuals  = np.vstack([rA, rB]) 
	fwhm       = rft1d.geom.estimate_fwhm(residuals)
	resels     = rft1d.geom.resel_counts(residuals, fwhm, element_based=False)
	zstar      = rft1d.t.isf_resels(0.5*alpha, df, resels, withBonf=True, nNodes=Q)
	hstar      = zstar * sPooled * (1./JA + 1./JB)**0.5
	### check the CI type:
	if datum == 'difference':
		ci     = ConfidenceInterval(d, alpha, fwhm, resels, zstar, hstar, design='TwoSample', datumstr=datum, criterionstr=criterion, df=(1,df))
	else:
		if criterion=='meanB':
			ci     = ConfidenceInterval(mA, alpha, fwhm, resels, zstar, hstar, criterion=mB, design='TwoSample', datumstr=datum, criterionstr=criterion, df=(1,df))
		else:
			ci     = ConfidenceIntervalMulti([mA, mB], alpha, fwhm, resels, zstar, 0.5*hstar, design='TwoSample', datumstr=datum, criterionstr=criterion, df=(1,df))
	return ci
	



