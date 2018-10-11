
# Copyright (C) 2018  Todd Pataky


import numpy as np
from . import _mvbase, _spm

eps        = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



def _T2_onesample_singlenode(y):  #at a single node:
	y        = np.matrix(y)
	n        = y.shape[0]      #nResponses
	m        = y.mean(axis=0)  #mean vector
	W        = np.cov(y.T) + eps    #covariance
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




def hotellings(Y, mu=None, roi=None):
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
		return _spm.SPM0D_T2(T2, (v1, v2))
	else:
		if mu is not None:
			Y         = Y - mu
		nResponses,nNodes,nVectDim  = Y.shape
		T2            = np.array([_T2_onesample_singlenode(Y[:,i,:])   for i in range(nNodes)])
		T2            = T2 if roi is None else np.ma.masked_array(T2, np.logical_not(roi))
		R             = _mvbase._get_residuals_onesample(Y)
		W             = _mvbase._fwhm(R)
		rCounts       = _mvbase._resel_counts(R, W, roi=roi)
		m,p           = float(nResponses)-1, float(nVectDim)
		v1,v2         = p, m
		return _spm.SPM_T2(T2, (v1, v2), W, rCounts, None, None, R, roi=roi)
	


def hotellings_paired(YA, YB, roi=None):
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
	
	return hotellings( YB - YA, roi=roi )



def hotellings2(YA, YB, equal_var=True, roi=None):
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
		return _spm.SPM0D_T2(T2, (v1, v2))
	else:
		JA,QA,IA      = YA.shape
		JB,QB,IB      = YB.shape
		T2            = np.array([_T2_twosample_singlenode(YA[:,i,:], YB[:,i,:])   for i in range(QA)])
		T2            = T2 if roi is None else np.ma.masked_array(T2, np.logical_not(roi))
		R             = _mvbase._get_residuals_twosample(YA, YB)
		W             = _mvbase._fwhm(R)
		rCounts       = _mvbase._resel_counts(R, W, roi=roi)
		# v1,v2         = float(IA), float(JA+JB-IA-1)  ###incorrect;  these are F df, not T2 df
		v1,v2         = float(IA), float(JA+JB-2)
		return _spm.SPM_T2(T2, (v1, v2), W, rCounts, None, None, R, roi=roi)


