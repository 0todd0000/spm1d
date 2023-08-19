'''
Hotelling's multivariate one- , paired- and two-sample tests

Copyright (C) 2023  Todd Pataky
'''

# 


import numpy as np
from .. _dec import appendargs
from .. _spmcls import SPM0D, SPM1D
from ... geom import estimate_fwhm_mv, resel_counts_mv

eps        = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



def _get_residuals_onesample(Y):
	N = Y.shape[0]
	m = Y.mean(axis=0)
	R = Y - np.array([m]*N)
	return R

def _get_residuals_onesample_0d(Y):
	N = Y.shape[0]
	m = Y.mean(axis=0)
	R = Y - np.array([m]*N)
	return R

def _get_residuals_twosample(YA, YB):
	RA = _get_residuals_onesample(YA)
	RB = _get_residuals_onesample(YB)
	R  = np.vstack( (RA,RB) )
	return R


def _get_residuals_twosample_0d(YA, YB):
	RA = _get_residuals_onesample_0d(YA)
	RB = _get_residuals_onesample_0d(YB)
	R  = np.vstack( (RA,RB) )
	return R



def _T2_onesample_singlenode(y):  #at a single node:
	y        = np.matrix(y)
	n        = y.shape[0]           # nResponses
	m        = y.mean(axis=0)       # mean vector
	W        = np.cov(y.T) + eps    # covariance
	T2       = n * m * np.linalg.inv(W) * m.T
	return float(T2)

def _T2_twosample_singlenode(yA, yB):  #at a single node:
	JA,JB    = yA.shape[0], yB.shape[0]  #nResponses
	yA,yB    = np.matrix(yA), np.matrix(yB)
	mA,mB    = yA.mean(axis=0), yB.mean(axis=0)  #means
	WA,WB    = np.cov(yA.T), np.cov(yB.T)
	W        = ((JA-1)*WA + (JB-1)*WB) / (JA+JB-2) + eps
	T2       = (JA*JB)/float(JA+JB)  * (mB-mA) * np.linalg.inv(W) * (mB-mA).T
	return float(T2)




@appendargs
def hotellings(Y, mu=None, roi=None, _fwhm_method='taylor2008'):
	'''
	One-sample Hotelling's T2 test.
	
	:Parameters:
		- *Y* --- (J x Q x I) numpy array
		- *mu* --- scalar or (Q x I) array (datum)

	
	:Returns:
		- T2 : An **spm1d._spm.SPM_T2** instance
	'''
	
	if Y.ndim==2:
		if mu is not None:
			Y         = Y - mu
		T2            = _T2_onesample_singlenode(Y)
		J,I           = Y.shape
		m,p           = float(J)-1, float(I)
		v1,v2         = p, m
		R      = _get_residuals_onesample_0d(Y)
		spm           =  SPM0D('T2', T2, (v1, v2), beta=None, residuals=R, sigma2=None, X=None)
		# return _spm.SPM0D_T2(T2, (v1, v2))
	else:
		if mu is not None:
			Y         = Y - mu
		nResponses,nNodes,nVectDim  = Y.shape
		T2            = np.array([_T2_onesample_singlenode(Y[:,i,:])   for i in range(nNodes)])
		T2            = T2 if roi is None else np.ma.masked_array(T2, np.logical_not(roi))
		R             = _get_residuals_onesample(Y)
		fwhm          = estimate_fwhm_mv(R, method=_fwhm_method)
		resels = resel_counts_mv(R, fwhm, roi=roi)
		m,p           = float(nResponses)-1, float(nVectDim)
		v1,v2         = p, m
		spm    = SPM1D('T2', T2, (v1,v2), beta=None, residuals=R, sigma2=None, X=None, fwhm=fwhm, resels=resels, roi=roi)
	# spm._set_testname( 'hotellings' )
	# spm._set_data( Y, mu )
	return spm
	



def hotellings_paired(YA, YB, roi=None, _fwhm_method='taylor2008'):
	'''
	Paired Hotelling's T2 test.
	
	:Parameters:
		- *YA* --- (J x Q x I) numpy array
		- *YB* --- (J x Q x I) numpy array

	
	:Returns:
		- T2 : An **spm1d._spm.SPM_T2** instance
		
	:Note:
		- A paired Hotelling's test on (YA,YB) is equivalent to a one-sample Hotelling's test on (YB-YA)
	'''
	
	return hotellings( YB - YA, roi=roi, _fwhm_method=_fwhm_method )



@appendargs
def hotellings2(YA, YB, equal_var=True, roi=None, _fwhm_method='taylor2008'):
	'''
	Two-sample Hotelling's T2 test.
	
	:Parameters:
		- *YA* --- (J x Q x I) numpy array
		- *YB* --- (J x Q x I) numpy array

	
	:Returns:
		- T2 : An **spm1d._spm.SPM_T2** instance
		
	:Note:
		- Non-sphericity correction not implemented. Equal variance must be assumed by setting "equal_var=True".
	'''
	if equal_var is not True:
		raise( UserWarning('Non-sphericity correction not implemented. To continue you must assume equal variance and set "equal_var=True".') )
	if YA.ndim==2:
		T2            = _T2_twosample_singlenode(YA, YB)
		JA,IA         = YA.shape
		JB,IB         = YB.shape
		# v1,v2         = float(IA), float(JA+JB-IA-1)  ###incorrect;  these are F df, not T2 df
		v1,v2         = float(IA), float(JA+JB-2)
		# return _spm.SPM0D_T2(T2, (v1, v2))
		R             = _get_residuals_twosample_0d(YA, YB)
		spm           = SPM0D('T2', T2, (v1, v2), beta=None, residuals=R, sigma2=None, X=None)
	else:
		JA,QA,IA      = YA.shape
		JB,QB,IB      = YB.shape
		T2            = np.array([_T2_twosample_singlenode(YA[:,i,:], YB[:,i,:])   for i in range(QA)])
		T2            = T2 if roi is None else np.ma.masked_array(T2, np.logical_not(roi))
		R             = _get_residuals_twosample(YA, YB)
		fwhm          = estimate_fwhm_mv(R, method=_fwhm_method)
		resels = resel_counts_mv(R, fwhm, roi=roi)
		# v1,v2         = float(IA), float(JA+JB-IA-1)  ###incorrect;  these are F df, not T2 df
		v1,v2         = float(IA), float(JA+JB-2)
		spm    = SPM1D('T2', T2, (v1,v2), beta=None, residuals=R, sigma2=None, X=None, fwhm=fwhm, resels=resels, roi=roi)
	# spm._set_testname( 'hotellings2' )
	# spm._set_data( YA, YB )
	return spm
	

