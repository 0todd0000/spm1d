'''
Tests for variance.
'''

# Copyright (C) 2021  Todd Pataky

import numpy as np
from .. import rft1d


def eqvartest(y0, y1, alt="unequal", alpha=None, withBonf=True):
	'''
	F test for equal variance.
	
	This test was reported in Kowalski et al. (2021) and adapted from the
	MATAB script provided as supplementary material with that article.
	
	.. note:: The current implementation of this test does not follow the general spm1d.stats procedures. See details below.

	References:
	
	F-test of equality of variances
	https://en.wikipedia.org/wiki/F-test_of_equality_of_variances
	
	Kowalski, E., Catelli, D. S., & Lamontagne, M. (2021). A waveform test
	for variance inequality, with a comparison of ground reaction force
	during walking in younger vs. older adults. Journal of Biomechanics
	127: 110657.
	https://doi.org/10.1016/j.jbiomech.2021.110657


	:Parameters:
	
	- *y0* --- (J0 x Q) numpy array (dependent variable, one group)
	- *y1* --- (J1 x Q) numpy array (dependent variable, one group)
	- *alt* --- alternative hypothesis: "unequal" (default) or "greater" ( var(y0) > var(y1) )
	- *alpha* --- Type I error rate (set this to "None" to bypass inference and return only the F statistic)
	
	:Returns:
	
	- *f* --- (Q,) array containing the test statistic.
	- *fcrit* --- random field theory-corrrected critical f value (None if alpha=None)
	
	:Example:
	
	>>> f,fcrit  = spm1d.stats.eqvartest(y0, y1, alt="unequal", alpha=0.05, withBonf=True)
	>>> plt.plot(f)
	>>> plt.axhline(fcrit)
	'''
	# check dimensionality:
	if (np.ndim(y0)<2) or (np.ndim(y1)<2):
		raise NotImplementedError( 'Only implemented for 1D data.' )
	# check sample sizes:
	J0,J1         = y0.shape[0], y1.shape[0]
	if (J0!=J1) and (alt.upper()=='UNEQUAL'):
		raise NotImplementedError( 'Unequal alternative implemented only for equal sample sizes. Set alt="greater" to conduct this test.' )
	# calculate f statistic:
	s0,s1         = y0.var(axis=0, ddof=1), y1.var(axis=0, ddof=1)
	if alt.upper() == 'UNEQUAL':
		ss        = np.vstack([s0, s1])
		smax,smin = ss.max(axis=0), ss.min(axis=0)
		f         = smax / smin
	else:
		f         = s0 / s1
	if alpha is None:
		fcrit     = None
	else:
		# conduct inference:
		Q         = y0.shape[1]
		df        = J0-1, J1-1
		r0,r1     = y0 - y0.mean(axis=0), y1 - y1.mean(axis=0)
		r         = np.vstack( [r0,r1] )
		efwhm     = rft1d.geom.estimate_fwhm(r)
		pcrit     = alpha/2 if (alt.upper()=="UNEQUAL") else alpha
		fcrit     = rft1d.f.isf(pcrit, df, Q, efwhm, withBonf=withBonf)
	return f,fcrit




