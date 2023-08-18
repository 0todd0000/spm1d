'''
One- and two sample tests.
'''

# Copyright (C) 2023  Todd Pataky



# import numpy as np
# from .. _spmcls import SPM0D

# from . factors import Factor
# from . contrasts import Contrast

# from .. _la import rank
# from ... util import array2shortstr, dflist2str, df2str, DisplayParams
# eps = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors




from . _dec import appendSPMargs






def _assemble_spm_objects(design, model, fit, teststat, roi=None):
	if fit.dvdim==0:
		# from .. _spmcls import SPM0D
		from spm1d.stats._spmcls import SPM0D
		# spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
		spm = SPM0D(design, model, fit, teststat)
	else:
		# from .. _spmcls import SPM1D
		from spm1d.stats._spmcls import SPM1D
		spm = SPM1D(design, model, fit, teststat)
		# spm = [SPM1D(design, model, fit, s, roi)  for s in teststats]
	# if len(spm)==1:
	# 	spm = spm[0]
	# else:
	# 	from .. _spmcls import SPMFList
	# 	spm = SPMFList( spm )
	return spm
	



def glm(y, X, c, QQ=None):
	from . core.models import GeneralLinearModel
	model     = GeneralLinearModel()
	model.set_design_matrix( X )
	# model.set_variance_model( QQ )
	fit       = model.fit( y )
	# t         = fit.calculate_t_stat( c, gg=gg, _Xeff=_Xeff, ind=i )
	teststat  = fit.calculate_t_stat( c )
	# teststats = [   for i,c in enumerate(C)]
	return model, fit, teststat
	# print(t)

	



	

@appendSPMargs
def ttest(y, mu=0, roi=None):
	from . core.designs import TTEST
	design    = TTEST(y, mu)
	model,fit,teststat = glm(y, design.X, design.contrasts[0].C)
	return _assemble_spm_objects(design, model, fit, teststat)
	# return model,fit,teststat
	
	
	

ttest2 = None
ttest_paired = None
regress = None




# import numpy as np
# from . _dec import appendSPMargs
# from . import _datachecks
# from . _cov import CovarianceModel
# from . _la import rank
# eps = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors
#
#
# def __tstat_cov_model(Y, X, Xi, c, b, s2, Q):
# 	'''
# 	t statistic calculation given a covariance model (Q)
#
# 	Covariance components (V) and their hyperparameters (h)
# 	are estimated using REML. See spm1d.stats._cov.py for
# 	more details
# 	'''
# 	from . _cov import reml, traceRV
# 	ndim        = Y.ndim
# 	if ndim == 1:
# 		Y       = np.array([Y]).T
# 	n,s         = Y.shape
# 	trRV        = n - rank(X)
# 	q           = np.diag(np.sqrt( trRV / s2 )).T if (ndim==2) else np.array( [np.sqrt( trRV / s2 )] )
# 	Ym          = Y @ q
# 	if ndim == 1:
# 		Ym      = np.array([Ym]).T
# 	YY          = Ym @ Ym.T / s
# 	V,h         = reml(YY, X, Q)
# 	V           = V * (n / np.trace(V))
# 	trRV,trRVRV = traceRV(V, X)
# 	df          = trRV**2 / trRVRV  # effective degrees of freedom
# 	t           = (c @ b)  /   ( np.sqrt( s2 * (c @ Xi @ V @ Xi.T @ c)  + eps ) )
# 	return t, df
#
#
# def _tstat_cov_model(Y, X, Xi, c, b, s2, Q, roi=None):
# 	if roi is None:
# 		t,df      = __tstat_cov_model(Y, X, Xi, c, b, s2, Q)
# 	else:
# 		_Y,_b,_s2 = Y[:,roi], b[:,roi], s2[roi]
# 		_t,df     = __tstat_cov_model(_Y, X, Xi, c, _b, _s2, Q)
# 		t         = np.nan * np.ones(Y.shape[1])
# 		t[roi]    = _t
# 	return t, df
#
#
# def glm(Y, X, c, Q=None, roi=None):
# 	'''
# 	General linear model (for t contrasts).
#
# 	:Parameters:
#
# 	- *Y* --- (J x Q) numpy array (dependent variable)
# 	- *X* --- (J x B) design matrix  (J responses, B parameters)
# 	- *c* --- B-component contrast vector (list or array)
# 	- *Q* --- list of (J,J) covariance components (optional)
# 	- *roi* --- (Q,) boolean numpy array (optional)
#
# 	:Returns:
#
# 	- An **spm1d._spm.SPM_T** object.
#
# 	:Example:
#
# 	>>> t  = spm1d.stats.glm(Y, X, (-1,1))
# 	>>> ti = t.inference(alpha=0.05, two_tailed=True)
# 	>>> ti.plot()
# 	'''
#
# 	Xi     = np.linalg.pinv(X)
# 	b      = Xi @ Y    # parameters
# 	eij    = Y - X @ b                # residuals
# 	ss     = (eij ** 2).sum(axis=0)   # sum-of-squared residuals
# 	df     = Y.shape[0] - rank(X)     # degrees of freedom
# 	s2     = ss / df                  # variance
#
# 	if Q is None:  # covariance not modeled
# 		t      = (c @ b)  /   ( np.sqrt( s2 * (c @ np.linalg.inv(X.T @ X) @ c) ) + eps )
# 	else:
# 		t,df   = _tstat_cov_model(Y, X, Xi, c, b, s2, Q, roi=roi)
#
# 	if Y.ndim == 1:
# 		from . _spmcls import SPM0D
# 		spm  = SPM0D('T', t, (1,df), beta=b, residuals=eij, sigma2=s2, X=X)
# 	else:
# 		from . _spmcls import SPM1D
# 		from .. geom import estimate_fwhm, resel_counts
# 		fwhm   = estimate_fwhm(eij)
# 		resels = resel_counts(eij, fwhm, element_based=False, roi=roi)
# 		if roi is not None:
# 			t  = np.ma.masked_array(t, np.logical_not(roi))
# 		spm      = SPM1D('T', t, (1,df), beta=b, residuals=eij, sigma2=s2, X=X, fwhm=fwhm, resels=resels, roi=roi)
# 	return spm
#
#
#
# @appendSPMargs
# def regress(Y, x, roi=None):
# 	'''
# 	Simple linear regression.
#
# 	:Parameters:
#
# 	- *Y* --- (J x Q) numpy array (dependent variable)
# 	- *x* --- J-component list or array (independent variable)
#
# 	:Returns:
#
# 	- An **spm1d._spm.SPM_T** object.
#
# 	:Example:
#
# 	>>> Y  = np.random.rand(10, 101)
# 	>>> Y  = spm1d.util.smooth(Y, fwhm=10)
# 	>>> x  = np.random.rand(10)
# 	>>> t  = spm1d.stats.regress(Y, x)
# 	>>> ti = t.inference(alpha=0.05)
# 	>>> ti.plot()
#
# 	:Notes:
# 		- the correlation coefficient is retrievable as "t.r" where "t" is the output from **spm1d.stats.regress**
# 		- statistical inferences are based on *t*, not on *r*
# 	'''
# 	# Y              = _datachecks.asmatrix(Y, dtype=float)
# 	# _datachecks.check('regress', Y, x)
# 	J              = Y.shape[0]
# 	X              = np.ones((J,2))
# 	X[:,0]         = x
# 	c              = [1,0]
# 	spm            = glm(Y, X, c, roi=roi)
# 	spm.r          = spm.z / (  (J - 2 + spm.z**2)**0.5)   # t = r * ((J-2)/(1-r*r) )**0.5
# 	return spm
#
#
#
#
#
#
#
#
# @appendSPMargs
# def ttest(Y, mu=None, roi=None):
# 	'''
# 	One-sample t test.
#
# 	:Parameters:
#
# 	- *Y* --- (J x Q) data array  (J responses, Q nodes)
# 	- *mu* --- optional Q-component datum array (default is the null continuum)
#
# 	:Returns:
#
# 	- An **spm1d._spm.SPM_T** object.
#
# 	:Example:
#
# 	>>> Y  = np.random.randn(8, 101)
# 	>>> Y  = spm1d.util.smooth(Y, fwhm=15)
# 	>>> t  = spm1d.stats.ttest(Y)
# 	>>> ti = t.inference(alpha=0.05, two_tailed=True)
# 	>>> ti.plot()
# 	'''
# 	Y       = np.asarray( Y, dtype=float )
# 	# _datachecks.check('ttest', Y, y0)
# 	J       = Y.shape[0]
# 	Ytemp   = Y.copy()
# 	if mu is not None:
# 		Ytemp -= mu
# 	X       = np.ones((J,1))
# 	c       = (1,)
# 	### compute SPM{t}:
# 	spm = glm(Ytemp, X, c, roi=roi)
# 	return spm
#
#
#
#
#
# def ttest_paired(YA, YB, roi=None):
# 	'''
# 	Paired t test.
#
# 	:Parameters:
#
# 	- *YA* --- (J x Q) data array  (J responses, Q nodes)
# 	- *YB* --- (J x Q) data array  (J responses, Q nodes)
#
# 	:Returns:
#
# 	- An **spm1d._spm.SPM_T** object.
#
# 	:Example:
#
# 	>>> YA,YB  = np.random.randn(8, 101), np.random.randn(8, 101)
# 	>>> YA,YB  = spm1d.util.smooth(Y, fwhm=10), spm1d.util.smooth(Y, fwhm=10)
#
# 	>>> t      = spm1d.stats.ttest_paired(YA, YB)
# 	>>> ti = t.inference(alpha=0.05)
# 	>>> ti.plot()
# 	'''
# 	# YA,YB    = _datachecks.asmatrix(YA, dtype=float), _datachecks.asmatrix(YB, dtype=float)
# 	# _datachecks.check('ttest_paired', YA, YB)
# 	spm      = ttest(YA-YB, roi=roi)
# 	spm._set_testname( 'ttest_paired' )
# 	# spm._set_data( _yA, _yB )  # don't set the data!!!!  Allow ttest to set the data (set using the "appendSPMargs" decorator)
# 	return spm
#
#
#
#
#
# # def ttest2(YA, YB, equal_var=None, roi=None):
# @appendSPMargs
# def ttest2(YA, YB, equal_var=None, var_model=1, roi=None):
# 	'''
# 	Two-sample t test.
#
# 	:Parameters:
#
# 	- *YA* --- (J x Q) data array  (J responses, Q nodes)
# 	- *YB* --- (J x Q) data array  (J responses, Q nodes)
# 	- *equal_var* --- (deprecated) If *True*, equal group variance will be assumed
# 	- *var_model* --- Variance model (see below)
#
# 	Variance/covariance modeling:
# 	- Models the variance / covariance amongst observations (NOT across domain nodes)
# 	- The previous "equal_var" keyword argument is deprecated
#
# 	:Returns:
#
# 	- An **spm1d._spm.SPM_T** object.
#
# 	:Example:
#
# 	>>> YA,YB  = np.random.randn(8, 101), np.random.randn(8, 101)
# 	>>> YA,YB  = spm1d.util.smooth(Y, fwhm=10), spm1d.util.smooth(Y, fwhm=10)
#
# 	>>> t  = spm1d.stats.ttest2(YA, YB)
# 	>>> ti = t.inference(alpha=0.05)
# 	>>> ti.plot()
# 	'''
# 	### check data:
# 	# YA,YB    = _datachecks.asmatrix(YA, dtype=float), _datachecks.asmatrix(YB, dtype=float)
# 	# _datachecks.check('ttest2', YA, YB)
# 	### assemble data
# 	JA,JB    = YA.shape[0], YB.shape[0]
# 	# Y        = np.vstack(  (YA, YB)  )
# 	Y        = np.hstack(  (YA, YB)  ) if (YA.ndim==1) else np.vstack(  (YA, YB)  )
# 	### specify design and contrast:
# 	X        = np.zeros( (JA+JB, 2) )
# 	X[:JA,0] = 1
# 	X[JA:,1] = 1
# 	c        = (1, -1)
# 	### compute SPM{t}:
#
# 	model    = CovarianceModel(X)
# 	if equal_var:
# 		model.add_constant_var()
# 	else:
# 		model.add_group_vars()
# 		# model.add_autocorr()
# 	Q        = model.get_model()
#
# 	spm = glm(Y, X, c, Q=Q, roi=roi)
# 	return spm

