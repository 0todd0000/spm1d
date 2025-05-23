'''
CANONICAL CORRELATION ANALYSIS
'''

# Copyright (C) 2025  Todd Pataky


from math import sqrt,log
import numpy as np
from . import _mvbase, _spm



##########################################
#    CANONICAL CORRELATION ANALYSIS
##########################################





def cca_single_node(y, x):
    N          = y.shape[0]
    X          = x[:,np.newaxis] if x.ndim==1 else x
    Y          = y[:,np.newaxis] if y.ndim==1 else y
    Z          = np.ones((N,1))
    Rz         = np.eye(N) - Z @ np.linalg.inv(Z.T@Z) @ Z.T
    XStar      = Rz @ X
    YStar      = Rz @ Y
    p,r        = 1.0, 1.0   #nContrasts, nNuisanceFactors
    m          = N - p - r
    H          = YStar.T @ XStar  @  np.linalg.inv( XStar.T @ XStar  )  @ XStar.T @ YStar / p
    W          = YStar.T  @ (np.eye(nResponses)  -  XStar@np.linalg.inv(XStar.T@XStar)@XStar.T) @ YStar  / m
    #estimate maximum canonical correlation:
    F          = np.linalg.inv(W) @ H
    ff         = np.linalg.eigvals(  F  )
    fmax       = float( np.real(ff.max()) )
    r2max      = fmax * p  / (m + fmax*p)
    rmax       = sqrt(r2max)
    ### compute test statistic:
    p,m        = float(N), float(y.shape[1])
    x2         = -(p-1-0.5*(m+2)) * log(  (1-rmax**2) )
    return x2


# def cca(y, x):
# 	X2         = np.array([cca_single_node(y[:,q,:], x)   for q in range(y.shape[1])])
# 	R          = _mvbase._get_residuals_regression(y, x)
# 	fwhm       = _mvbase._fwhm(R)
# 	resels     = _mvbase._resel_counts(R, fwhm)
# 	df         = 1, y.shape[2]
# 	return _spm.SPM_X2(X2, df, fwhm, resels, None, None, R)
# 	
	

def _cca_single_node_efficient(y, x, Rz, XXXiX):
	N          = y.shape[0]
	Y          = np.asarray(y)
	YStar      = Rz @ Y
	p,r        = 1.0, 1.0   #nContrasts, nNuisanceFactors
	m          = N - p - r
	H          = YStar.T @ XXXiX @ YStar / p
	W          = YStar.T  @ (np.eye(N)  -  XXXiX) @ YStar  / m
	#estimate maximum canonical correlation:
	F          = np.linalg.inv(W) @ H
	ff         = np.linalg.eigvals(  F  )
	fmax       = float( np.real(ff.max()) )
	r2max      = fmax * p  / (m + fmax*p)
	rmax       = sqrt(r2max)
	### compute test statistic:
	m          = y.shape[1]
	x2         = -(N-1-0.5*(m+2)) * log(  (1-rmax**2) )
	# df         = m
	return x2


def cca(Y, x, roi=None):
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
	X          = np.asarray([x]).T
	Z          = np.ones((N,1))
	Rz         = np.eye(N) - Z @ np.linalg.inv(Z.T@Z) @ Z.T
	XStar      = Rz @ X
	XXXiX      = XStar  @  np.linalg.inv( XStar.T @ XStar  )  @ XStar.T
	if Y.ndim==2:
		X2         = _cca_single_node_efficient(Y, x, Rz, XXXiX)
		df         = 1, Y.shape[1]
		return _spm.SPM0D_X2(X2, df)
	else:
		X2         = np.array([_cca_single_node_efficient(Y[:,q,:], x, Rz, XXXiX)   for q in range(Y.shape[1])])
		X2         = X2 if roi is None else np.ma.masked_array(X2, np.logical_not(roi))
		R          = _mvbase._get_residuals_regression(Y, x)
		fwhm       = _mvbase._fwhm(R)
		resels     = _mvbase._resel_counts(R, fwhm, roi=roi)
		df         = 1, Y.shape[2]
		return _spm.SPM_X2(X2, df, fwhm, resels, None, None, R, roi=roi)



