'''
Canonical correlation analysis

Copyright (C) 2023  Todd Pataky
'''



from math import sqrt,log
import numpy as np
from .. _dec import appendargs
from .. _spmcls import SPM0D, SPM1D
from ... geom import estimate_fwhm_mv, resel_counts_mv


##########################################
#    CANONICAL CORRELATION ANALYSIS
##########################################


# def max_effect_direction_singlenode(y, x):
# 	nObserv    = y.shape[0]
# 	nCompon    = y.shape[1]
# 	x,Y        = np.matrix(x.T).T, np.matrix(y)
# 
# 	Z          = np.matrix(np.ones(nObserv)).T
# 	Rz         = np.eye(nObserv) - Z*np.linalg.inv(Z.T*Z)*Z.T
# 	xStar      = Rz * x
# 	YStar      = Rz * Y
# 
# 	p          = x.shape[1] #nContrasts
# 	m          = nObserv - p
# 	H          = YStar.T * xStar  *  np.linalg.inv( xStar.T * xStar  )  * xStar.T * YStar / p
# 	W          = YStar.T  * (np.eye(nObserv)  -  xStar*np.linalg.inv(xStar.T*xStar)*xStar.T) * YStar  / m
# 
# 	F          = np.linalg.inv(W)*H
# 	# ff         = np.linalg.eigvals(  F  )
# 	vals,vecs  = np.linalg.eig(F)
# 	ind        = np.argmax(vals)
# 	r          = vecs[:,ind]
# 	return r


	

def cca_single_node(y, x):
	N          = y.shape[0]
	X,Y        = np.matrix(x.T).T, np.matrix(y)
	Z          = np.matrix(np.ones(N)).T
	Rz         = np.eye(N) - Z*np.linalg.inv(Z.T*Z)*Z.T
	XStar      = Rz * X
	YStar      = Rz * Y
	p,r        = 1.0, 1.0   #nContrasts, nNuisanceFactors
	m          = N - p - r
	XsYs       = (XStar*np.linalg.inv(XStar.T*XStar)*XStar.T) * YStar
	res        = YStar  - XsYs  # residuals  (same as fitting separate linear regressions to each component)
	# H          = YStar.T * XStar  *  np.linalg.inv( XStar.T * XStar  )  * XStar.T * YStar / p
	H          = YStar.T * XsYs / p
	W          = YStar.T  * (np.eye(N)  -  XStar*np.linalg.inv(XStar.T*XStar)*XStar.T) * YStar  / m
	#estimate maximum canonical correlation:
	F          = np.linalg.inv(W)*H
	ff         = np.linalg.eigvals(  F  )
	fmax       = float( np.real(ff.max()) )
	r2max      = fmax * p  / (m + fmax*p)
	rmax       = sqrt(r2max)
	### compute test statistic:
	m          = y.shape[1]
	x2         = -(N-1-0.5*(m+2)) * log(  (1-rmax**2) )
	# df         = m
	return x2,res




def _cca_single_node_efficient(y, x, Rz, XXXiX):
	N          = y.shape[0]
	Y          = np.matrix(y)
	YStar      = Rz * Y
	p,r        = 1.0, 1.0   #nContrasts, nNuisanceFactors
	m          = N - p - r
	res        = YStar - XXXiX * YStar  # residuals (same as fitting separate linear regressions to each component)
	H          = YStar.T * XXXiX * YStar / p
	W          = YStar.T  * (np.eye(N)  -  XXXiX) * YStar  / m
	#estimate maximum canonical correlation:
	F          = np.linalg.inv(W)*H
	ff         = np.linalg.eigvals(  F  )
	fmax       = float( np.real(ff.max()) )
	r2max      = fmax * p  / (m + fmax*p)
	rmax       = sqrt(r2max)
	### compute test statistic:
	m          = y.shape[1]
	x2         = -(N-1-0.5*(m+2)) * log(  (1-rmax**2) )
	# df         = m
	return x2,res

def _cca_efficient(y, x, Rz, XXXiX):
	r    = np.empty_like(y)
	x2   = []
	for q in range(y.shape[1]):
		xx2,rr = _cca_single_node_efficient(y[:,q,:], x, Rz, XXXiX)
		r[:,q] = rr
		x2.append(xx2)
	return np.asarray(x2), r
	
	


@appendargs
def cca(Y, x, roi=None, _fwhm_method='taylor2008'):
	'''
	Canonical correlation analysis (CCA).
	
	:Parameters:
		- *Y* --- A list or tuple of (J x Q) numpy arrays
		- *x* --- (J x 1) list or array (independent variable)

	
	:Returns:
		- X2 : An **spm1d._spm.SPM_X2** instance
	
	:Note:
		-  Currently only a univariate 0D independent variable (x) is supported.
	'''
	N          = Y.shape[0]
	X          = np.matrix(x.T).T
	Z          = np.matrix(np.ones(N)).T
	Rz         = np.eye(N) - Z*np.linalg.inv(Z.T*Z)*Z.T
	XStar      = Rz * X
	XXXiX      = XStar  *  np.linalg.inv( XStar.T * XStar  )  * XStar.T
	if Y.ndim==2:
		X2,R       = _cca_single_node_efficient(Y, x, Rz, XXXiX)
		df         = 1, Y.shape[1]
		spm = SPM0D('X2', X2, df, beta=None, residuals=R, sigma2=None, X=X)
	else:
		X2,R   = _cca_efficient(Y, x, Rz, XXXiX)
		X2     = X2 if roi is None else np.ma.masked_array(X2, np.logical_not(roi))
		fwhm   = estimate_fwhm_mv(R, method=_fwhm_method)
		resels = resel_counts_mv(R, fwhm, roi=roi)
		df     = 1, Y.shape[2]
		spm    = SPM1D('X2', X2, df, beta=None, residuals=R, sigma2=None, X=X, fwhm=fwhm, resels=resels, roi=roi)
	return spm



