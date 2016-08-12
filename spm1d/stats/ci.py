
'''
Confidence intervals
'''

import rft1d
from .. plot import plot_ci



class ConfidenceInterval(object):
	def __init__(self, datum, alpha, zstar, hstar, design=None):
		self.Q      = datum.size
		self.datum  = datum
		self.alpha  = alpha
		self.zstar  = zstar
		self.hstar  = hstar
		self.design = design
		
	def plot(self, ax=None, x=None, facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
		plot_ci(self, ax, x, facecolor, edgecolor, alpha, autoset_ylim)


def ci_onesample(y, alpha=0.05):
	# spmi       = spm1d.stats.ttest(y, 0).inference(alpha, two_tailed=True)
	# zstar      = ti.zstar
	J,Q        = y.shape
	m,s        = y.mean(axis=0), y.std(axis=0, ddof=1)
	residuals  = y - m
	fwhm       = rft1d.geom.estimate_fwhm(residuals)
	resels     = rft1d.geom.resel_counts(residuals, fwhm, element_based=False)
	zstar      = rft1d.t.isf_resels(0.5*alpha, J-1, resels, withBonf=True, nNodes=Q)
	hstar      = zstar * s / J**0.5
	return ConfidenceInterval(m, alpha, zstar, hstar, design='OneSample')