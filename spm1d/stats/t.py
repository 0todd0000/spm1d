

import numpy as np
from matplotlib import pyplot, cm as colormaps
import _datachecks, _reml, _spm
import rft1d


rank   = np.linalg.matrix_rank
eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors




def glm(Y, X, c, Q=None):
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
	Y      = np.matrix(Y)
	X      = np.matrix(X)
	c      = np.matrix(c).T
	### solve the GLM:
	b      = np.linalg.pinv(X)*Y    #parameters
	eij    = Y - X*b                #residuals
	R      = eij.T*eij              #residuals: sum of squares
	df     = Y.shape[0] - rank(X)   #degrees of freedom
	sigma2 = np.diag(R)/df          #variance
	### compute t statistic
	t      = np.array(c.T*b).flatten()  /   (np.sqrt(sigma2*float(c.T*(np.linalg.inv(X.T*X))*c)) + eps)
	### estimate df due to non-sphericity:
	if Q!=None:
		df = _reml.estimate_df_T(Y, X, eij, Q)
	eij    = np.asarray(eij)
	if Y.shape[1] > 1:
		### estimate field smoothness and geometry:
		fwhm   = rft1d.geom.estimate_fwhm(eij)
		resels = rft1d.geom.resel_counts(eij, fwhm, element_based=False)
		t      = _spm.SPM_T(t, (1,df), fwhm, resels, np.asarray(X), np.asarray(b), eij)
	else:
		t      = _spm.SPM0D_T(t, (1,df))
	return t





def regress(Y, x):
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
	Y              = _datachecks.asmatrix(Y)
	_datachecks.check('regress', Y, x)
	J              = Y.shape[0]
	X              = np.ones((J,2))
	X[:,0]         = x
	c              = [1,0]
	spmt           = glm(Y, X, c)
	spmt.r         = spmt.z / (  (J - 2 + spmt.z**2)**0.5)  #t = r * ((J-2)/(1-r*r) )**0.5
	spmt.isregress = True
	return spmt






def ttest(Y, y0=None):
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
	Y       = _datachecks.asmatrix(Y)
	_datachecks.check('ttest', Y, y0)
	J       = Y.shape[0]
	Ytemp   = Y.copy()
	if y0!=None:
		Ytemp -= y0
	X       = np.ones((J,1))
	c       = (1)
	### compute SPM{t}:
	return glm(Ytemp, X, c)



def ttest_paired(YA, YB):
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
	YA,YB    = _datachecks.asmatrix(YA), _datachecks.asmatrix(YB)
	_datachecks.check('ttest_paired', YA, YB)
	return ttest(YA-YB)



def ttest2(YA, YB, equal_var=False):
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
	YA,YB    = _datachecks.asmatrix(YA), _datachecks.asmatrix(YB)
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
	return glm(Y, X, c, Q)




