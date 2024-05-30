'''
One- and two sample tests.
'''

# Copyright (C) 2016  Todd Pataky





import numpy as np
from matplotlib import pyplot, cm as colormaps
from . import _datachecks, _reml, _spm
from .. import rft1d


rank   = np.linalg.matrix_rank
eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors




def glm(Y, X, c, Q=None, roi=None):
    '''
    General linear model (for t contrasts).

    :Parameters:

    - *Y* --- (J x Q) numpy array (dependent variable)
    - *X* --- (J x B) design matrix  (J responses, B parameters)
    - *c* --- B-component contrast vector (list or array)
    - *Q* --- non-sphericity specifiers (not currently supported for **glm**)

    .. note:: Non-sphericity estimates are not supported for **spm1d.stats.glm**

    :Returns:

    - An **spm1d._spm.SPM_T** object.

    :Example:

    >>> t  = spm1d.stats.glm(Y, X, (-1,1))
    >>> ti = t.inference(alpha=0.05, two_tailed=True)
    >>> ti.plot()
    '''
    ### assemble data:
    Y      = np.asarray(Y)
    X      = np.asarray(X)
    c      = np.asarray([c]).T
    ### solve the GLM:
    b      = np.linalg.pinv(X) @ Y  #parameters
    eij    = Y - X@b                #residuals
    df     = Y.shape[0] - rank(X)   #degrees of freedom
    # # previous sigma2 calculation (slow when Q get large: about 5 ms for Q=1000 and about 900 ms for Q=10000! )
    # R      = eij.T@eij              #residuals: sum of squares
    # sigma2 = np.diag(R)/df          #variance
    # new sigam2 calculation (using Einstein summation trick)
    diagR  = np.einsum('ij,ji->i', eij.T, eij)  # residual sum of squares (eigensum trick)
    sigma2 = diagR / df          #variance
    ### compute t statistic
    cXXc   = c.T @ np.linalg.inv(X.T@X) @ c
    cXXc   = float(cXXc[0,0]) if isinstance(cXXc, np.ndarray) else float(cXXc)
    t      = np.array(c.T@b).flatten()  /   (np.sqrt(sigma2*cXXc + eps))
    ### estimate df due to non-sphericity:
    if Q is not None:
        df = _reml.estimate_df_T(Y, X, eij, Q)
    eij    = np.asarray(eij)
    if Y.shape[1] > 1:
        ### estimate field smoothness:
        fwhm   = rft1d.geom.estimate_fwhm(eij)
        ### compute resel counts:
        if roi is None:
            resels = rft1d.geom.resel_counts(eij, fwhm, element_based=False)
        else:
            B      = np.any( np.isnan(eij), axis=0)  #node is true if NaN
            B      = np.logical_and(np.logical_not(B), roi)  #node is true if in ROI and also not NaN
            mask   = np.logical_not(B)  #true for masked-out regions
            resels = rft1d.geom.resel_counts(mask, fwhm, element_based=False)
            t      = np.ma.masked_array(t, np.logical_not(roi))
        ### assemble SPM{t} object
        s      = np.asarray(sigma2).flatten()
        t      = _spm.SPM_T(t, (1,df), fwhm, resels, np.asarray(X), np.asarray(b), eij, sigma2=s, roi=roi)
    else:
        b,r    = np.asarray(b).flatten(), eij.flatten()
        s2     = float(sigma2[0]) if isinstance(sigma2, np.ndarray) else float(sigma2)
        t      = _spm.SPM0D_T(t, (1,df), beta=b, residuals=r, sigma2=s2)
    return t





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
	Y              = _datachecks.asarray(Y, dtype=float)
	_datachecks.check('regress', Y, x)
	J              = Y.shape[0]
	X              = np.ones((J,2))
	X[:,0]         = x
	c              = [1,0]
	spmt           = glm(Y, X, c, roi=roi)
	spmt.r         = spmt.z / (  (J - 2 + spmt.z**2)**0.5)  #t = r * ((J-2)/(1-r*r) )**0.5
	spmt.isregress = True
	return spmt






def ttest(Y, y0=None, roi=None):
	'''
	One-sample t test.
	
	:Parameters:
	
	- *Y* --- (J x Q) data array  (J responses, Q nodes)
	- *y0* --- optional Q-component datum array (default is the null continuum)
	
	:Returns:
	
	- An **spm1d._spm.SPM_T** object.
	
	:Example:
	
	>>> Y  = np.random.randn(8, 101)
	>>> Y  = spm1d.util.smooth(Y, fwhm=15)
	>>> t  = spm1d.stats.ttest(Y)
	>>> ti = t.inference(alpha=0.05, two_tailed=True)
	>>> ti.plot()
	'''
	Y       = _datachecks.asarray(Y, dtype=float)
	_datachecks.check('ttest', Y, y0)
	J       = Y.shape[0]
	Ytemp   = Y.copy()
	if y0 is not None:
		Ytemp -= y0
	X       = np.ones((J,1))
	c       = (1)
	### compute SPM{t}:
	return glm(Ytemp, X, c, roi=roi)



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
	YA,YB    = _datachecks.asarray(YA, dtype=float), _datachecks.asarray(YB, dtype=float)
	_datachecks.check('ttest_paired', YA, YB)
	return ttest(YA-YB, roi=roi)



def ttest2(YA, YB, equal_var=False, roi=None):
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
	YA,YB    = _datachecks.asarray(YA, dtype=float), _datachecks.asarray(YB, dtype=float)
	_datachecks.check('ttest2', YA, YB)
	### assemble data
	JA,JB    = YA.shape[0], YB.shape[0]
	Y        = np.vstack(  (YA, YB)  )
	### specify design and contrast:
	X        = np.zeros( (JA+JB, 2) )
	X[:JA,0] = 1
	X[JA:,1] = 1
	c        = (1, -1)
	### non-sphericity:
	Q        = None
	if not equal_var:
		J           = JA + JB
		q0,q1       = np.eye(JA), np.eye(JB)
		Q0,Q1       = np.matrix(np.zeros((J,J))), np.matrix(np.zeros((J,J)))
		Q0[:JA,:JA] = q0
		Q1[JA:,JA:] = q1
		Q           = [Q0, Q1]
	### compute SPM{t}:
	return glm(Y, X, c, Q, roi=roi)




