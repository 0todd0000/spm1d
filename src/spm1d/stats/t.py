'''
One- and two sample tests.
'''

# Copyright (C) 2016  Todd Pataky





import numpy as np
from matplotlib import pyplot, cm as colormaps
from . _dec import appendSPMargs
from . import _datachecks, _reml
from .. geom import estimate_fwhm, resel_counts


rank   = np.linalg.matrix_rank
eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



def glm(Y, X, c, Q=None, roi=None):
	'''
	General linear model (for t contrasts).
	
	:Parameters:
	
	- *Y* --- (J x Q) numpy array (dependent variable)
	- *X* --- (J x B) design matrix  (J responses, B parameters)
	- *c* --- B-component contrast vector (list or array)
	
	.. note:: Non-sphericity estimates are not supported for **spm1d.stats.glm**
	
	:Returns:
	
	- An **spm1d._spm.SPM_T** object.
	
	:Example:
	
	>>> t  = spm1d.stats.glm(Y, X, (-1,1))
	>>> ti = t.inference(alpha=0.05, two_tailed=True)
	>>> ti.plot()
	'''
	
	b      = np.linalg.pinv(X) @ Y    # parameters
	eij    = Y - X @ b                # residuals
	ss     = (eij ** 2).sum(axis=0)   # sum-of-squared residuals
	df     = Y.shape[0] - rank(X)     # degrees of freedom
	s2     = ss / df                  # variance
	t      = (c @ b)  /   ( np.sqrt( s2 * (c @ np.linalg.inv(X.T @ X) @ c) ) + eps )

	if Y.ndim == 1:
		from . _spmcls import SPM0D
		spm  = SPM0D('T', t, (1,df), beta=b, residuals=eij, sigma2=s2, X=X)
	else:
		from . _spmcls import SPM1D
		fwhm   = estimate_fwhm(eij)
		resels = resel_counts(eij, fwhm, element_based=False, roi=roi)
		if roi is not None:
			t  = np.ma.masked_array(t, np.logical_not(roi))
		spm      = SPM1D('T', t, (1,df), beta=b, residuals=eij, sigma2=s2, X=X, fwhm=fwhm, resels=resels, roi=roi)
	return spm



@appendSPMargs
def regress(Y, x, roi=None):
	'''
	Simple linear regression.
	
	:Parameters:
	
	- *Y* --- (J x Q) numpy array (dependent variable)
	- *x* --- J-component list or array (independent variable)
	
	:Returns:
	
	- An **spm1d._spm.SPM_T** object.
	
	:Example:
	
	>>> Y  = np.random.rand(10, 101)
	>>> Y  = spm1d.util.smooth(Y, fwhm=10)
	>>> x  = np.random.rand(10)
	>>> t  = spm1d.stats.regress(Y, x)
	>>> ti = t.inference(alpha=0.05)
	>>> ti.plot()
	
	:Notes:
		- the correlation coefficient is retrievable as "t.r" where "t" is the output from **spm1d.stats.regress**
		- statistical inferences are based on *t*, not on *r*
	'''
	# Y              = _datachecks.asmatrix(Y, dtype=float)
	# _datachecks.check('regress', Y, x)
	J              = Y.shape[0]
	X              = np.ones((J,2))
	X[:,0]         = x
	c              = [1,0]
	spm            = glm(Y, X, c, roi=roi)
	spm.r          = spm.z / (  (J - 2 + spm.z**2)**0.5)   # t = r * ((J-2)/(1-r*r) )**0.5
	return spm
	
	
	





@appendSPMargs
def ttest(Y, mu=None, roi=None):
	'''
	One-sample t test.
	
	:Parameters:
	
	- *Y* --- (J x Q) data array  (J responses, Q nodes)
	- *mu* --- optional Q-component datum array (default is the null continuum)
	
	:Returns:
	
	- An **spm1d._spm.SPM_T** object.
	
	:Example:
	
	>>> Y  = np.random.randn(8, 101)
	>>> Y  = spm1d.util.smooth(Y, fwhm=15)
	>>> t  = spm1d.stats.ttest(Y)
	>>> ti = t.inference(alpha=0.05, two_tailed=True)
	>>> ti.plot()
	'''
	Y       = np.asarray( Y, dtype=float )
	# _datachecks.check('ttest', Y, y0)
	J       = Y.shape[0]
	Ytemp   = Y.copy()
	if mu is not None:
		Ytemp -= mu
	X       = np.ones((J,1))
	c       = (1,)
	### compute SPM{t}:
	spm = glm(Ytemp, X, c, roi=roi)
	return spm





def ttest_paired(YA, YB, roi=None):
	'''
	Paired t test.
	
	:Parameters:
	
	- *YA* --- (J x Q) data array  (J responses, Q nodes)
	- *YB* --- (J x Q) data array  (J responses, Q nodes)

	:Returns:
	
	- An **spm1d._spm.SPM_T** object.
	
	:Example:
	
	>>> YA,YB  = np.random.randn(8, 101), np.random.randn(8, 101)
	>>> YA,YB  = spm1d.util.smooth(Y, fwhm=10), spm1d.util.smooth(Y, fwhm=10)
	
	>>> t      = spm1d.stats.ttest_paired(YA, YB)
	>>> ti = t.inference(alpha=0.05)
	>>> ti.plot()
	'''
	# YA,YB    = _datachecks.asmatrix(YA, dtype=float), _datachecks.asmatrix(YB, dtype=float)
	# _datachecks.check('ttest_paired', YA, YB)
	spm      = ttest(YA-YB, roi=roi)
	spm._set_testname( 'ttest_paired' )
	# spm._set_data( _yA, _yB )  # don't set the data!!!!  Allow ttest to set the data (set using the "appendSPMargs" decorator)
	return spm





# def ttest2(YA, YB, equal_var=None, roi=None):
@appendSPMargs
def ttest2(YA, YB, equal_var=None, roi=None):
	'''
	Two-sample t test.
	
	:Parameters:
	
	- *YA* --- (J x Q) data array  (J responses, Q nodes)
	- *YB* --- (J x Q) data array  (J responses, Q nodes)
	- *equal_var* --- If *True*, equal group variance will be assumed
	
	:Returns:
	
	- An **spm1d._spm.SPM_T** object.
	
	:Example:
	
	>>> YA,YB  = np.random.randn(8, 101), np.random.randn(8, 101)
	>>> YA,YB  = spm1d.util.smooth(Y, fwhm=10), spm1d.util.smooth(Y, fwhm=10)
	
	>>> t  = spm1d.stats.ttest2(YA, YB)
	>>> ti = t.inference(alpha=0.05)
	>>> ti.plot()
	'''
	### check data:
	# YA,YB    = _datachecks.asmatrix(YA, dtype=float), _datachecks.asmatrix(YB, dtype=float)
	# _datachecks.check('ttest2', YA, YB)
	### assemble data
	JA,JB    = YA.shape[0], YB.shape[0]
	# Y        = np.vstack(  (YA, YB)  )
	Y        = np.hstack(  (YA, YB)  ) if (YA.ndim==1) else np.vstack(  (YA, YB)  )
	### specify design and contrast:
	X        = np.zeros( (JA+JB, 2) )
	X[:JA,0] = 1
	X[JA:,1] = 1
	c        = (1, -1)
	### compute SPM{t}:
	spm = glm(Y, X, c, Q=None, roi=roi)
	return spm

