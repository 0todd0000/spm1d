
# Copyright (C) 2016  Todd Pataky

from math import sqrt,log
import numpy as np
from scipy import ndimage
from . import _spm
from .. import rft1d

eps        = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors








def _fwhm(R):
	nComp  = R.shape[2]
	W      = [rft1d.geom.estimate_fwhm(R[:,:,i])  for i in range(nComp)]
	return np.mean(W)

	
def _get_residuals_onesample(Y):
	N = Y.shape[0]
	m = Y.mean(axis=0)
	R = Y - np.array([m]*N)
	return R

def _get_residuals_twosample(YA, YB):
	RA = _get_residuals_onesample(YA)
	RB = _get_residuals_onesample(YB)
	return np.vstack((RA,RB))

def _get_residuals_regression(y, x):
	J,Q,I      = y.shape  #nResponses, nNodes, nComponents
	Z          = np.matrix(np.ones(J)).T
	X          = np.hstack([np.matrix(x.T).T, Z])
	Xi         = np.linalg.pinv(X)
	R          = np.zeros(y.shape)
	for i in range(Q):
		for ii in range(I):
			yy     = np.matrix(y[:,i,ii]).T
			b      = Xi*yy
			eij    = yy - X*b
			R[:,i,ii] = np.asarray(eij).flatten()
	return R

def _get_residuals_manova1(Y, GROUP):
	u  = np.unique(GROUP)
	R  = []
	for uu in u:
		R.append(   _get_residuals_onesample(Y[GROUP==uu])   )
	return np.vstack(R)


def _normalize_residuals(R):
	nCurves,nNodes,nVectDim = R.shape
	for i in range(nCurves):
		mag       = np.sqrt(  (R[i,:,:]**2).sum(axis=0)  )   #normalize vector at this time node
		R[i,:,:] /= mag
		mag       = np.sqrt(  (R[i,:,:]**2).sum(axis=1)  )   #normalize the time series energy
		R[i,:,:] /= np.vstack([mag]*nVectDim).T
	return R


def _resel_counts(R, W, roi=None):
	### construct binary search volume:
	B            = np.any(np.any(np.abs(R)>0, axis=0), axis=1)  #False indicates no observations at that node
	if roi is not None:
		B      = np.logical_and(B, roi)  #node is true if in ROI and also not NaN
	### summarize search area geometry:
	mNodes       = B.sum()
	mClusters    = ndimage.label(B)[1]
	### define resel counts:
	rCounts      = []
	rCounts.append(  mClusters  )
	rCounts.append( (mNodes-mClusters)/float(W) )   #number of non-zero nodes, normalized by FWHM
	return rCounts
	







