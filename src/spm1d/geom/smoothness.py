
'''
1D field smoothness estimates including FWHM and Lipschitz–Killing curvature (LKC)

References:

Barnes GR, Ridgway GR, Flandin G, Woolrich M, Friston K (2013). Set-level threshold-free tests on the intrinsic volumes of SPMs. NeuroImage 68:133-40.
https://doi.org/10.1016/j.neuroimage.2012.11.046

Taylor JE, Worsley KJ (2017). Detecting sparse signals in random fields, with an application to brain mapping. Journal of the American Statistical Association 102(479):913-28.
https://doi.org/10.1198/016214507000000815

'''

from math import log
import numpy as np
from . label import bwlabel
from .. util import array2shortstr, resels2str, DisplayParams
eps = np.finfo(float).eps
_4log2 = 4 * log(2)




class SmoothnessEstimates(object):
	def __init__(self, e, method='rft1d', roi=None):
		self.method   = method
		self.e        = e
		self.fwhm     = None
		self.lkc      = None
		self.resels   = None
		self._estimate(roi)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_header( self.__class__.__name__ )
		dp.add( 'J' )
		dp.add( 'Q' )
		dp.add( 'e', array2shortstr )
		dp.add( 'fwhm', fmt='%.3f' )
		dp.add( 'lkc', fmt='%.3f' )
		dp.add( 'resels', fmt=resels2str )
		return dp.asstr()
	
	def _estimate(self, roi):
		self.fwhm   = estimate_fwhm(self.e, method=self.method, roi=roi)
		self.lkc    = fwhm2lkc(self.fwhm, self.Q)
		self.resels = resel_counts(self.e, self.fwhm, roi=roi)

	@property
	def J(self):
		return self.e.shape[0]
	
	@property
	def Q(self):
		return self.e.shape[1]

	def set_roi(self, roi):
		self._estimate( roi )



# CONVERSION FUNCTIONS

def fwhm2lkc(fwhm, Q):
	resels = (Q - 1) / fwhm     # use (Q-1) for point-based sampling;  use (Q) for element-based sampling
	return resels2lkc( resels )

def lkc2resels(lkc, d=1):  # Barnes 2013, Eqn.9 (in text after equation)
	return _4log2 **(-d/2) * lkc

def lkc2fwhm(lkc, Q):
	resels = lkc2resels(lkc)
	return (Q - 1) / resels    # use (Q-1) for point-based sampling;  use (Q) for element-based sampling

def resels2lkc(resels, d=1):
	return resels / ( _4log2 **(-d/2) )



# SMOOTHNESS ESTIMATION FUNCTIONS


def _estimate_fwhm_rft1d(r, roi=None):
	'''
	(Modified from rft1d.geom)
	'''
	ssq    = (r**2).sum(axis=0)
	dy,dx  = np.gradient(r)       # gradient estimation (Method 2 from rft1d.geom)
	v      = (dx**2).sum(axis=0)
	# normalize:
	v     /= (ssq + eps)
	# ignore zero-variance nodes:
	i      = np.isnan(v)
	v      = v[np.logical_not(i)]
	# global FWHM estimate:
	rpn    = np.sqrt( v / _4log2 )  # resels per node
	fwhm   = 1 / rpn.mean()
	return fwhm
	

def _estimate_lkc_barnes2013(r):
	'''
	Lipschitz–Killing curvature, Barnes et al. (2013) Eqn.9
	
	Same resutls as Taylor & Worsley 2007; this is implemented just as a check
	
	Note: for the 1D case the LKC estimation procedure is more clearly explained in Taylor & Worsley (2007).
	The "standardized" residuals in Barnes et al. (2013, Eqn.4) create some confusion
	'''
	def _standardized_residuals(e):  # Barnes 2013, eqn.4
		# N  = e.shape[0]
		ss = (e**2).sum(axis=0) 
		# r  = (N-1)**0.5  * e / (ss ** 0.5)  # this yields incorrect results so the (N-1) standardization factor is removed
		r  = e / (ss ** 0.5)
		return r
	r     = _standardized_residuals( r ) # eqn.4
	dR    = np.diff(r, axis=1)           # eqn.7
	vol   = (dR**2).sum(axis=0)**0.5     # eqn.8
	lkc   = vol.sum()                    # eqn.9
	return lkc
	

def _estimate_lkc_taylor2007(e):
	'''
	Lipschitz–Killing curvature, Taylor & Worsley (2007) Eqn.6
	'''
	u   = e / (e**2).sum(axis=0)**0.5            # eqn.5
	d   = np.diff(u, axis=1)
	lkc = (  (d**2).sum(axis=0)**0.5  ).sum()    # eqn.6
	return lkc


def _estimate_lkc_mv_taylor2008(e):
	'''
	Lipschitz–Killing curvature, Taylor & Worsley (2008) Eqn.18
	
	Thank you to Fabian Telschow for helpful advice re: LKC estimates for multivariate residuals
	'''
	def _norm(a):
		return (a**2).sum(axis=0)**0.5
	n        = e.shape[2]  # number of vector components
	lkc      = 0
	for i in range(n):
		u    = e[:,:,i] / _norm( e[:,:,i] )      # normalized residuals
		lkc += _norm( np.diff(u, axis=1) ).sum() # component's contribution to LKC
	lkc     /= n
	return lkc



def estimate_fwhm(r, method='rft1d', roi=None):
	'''
	Estimate FWHM (smoothness) from univariate residuals
	
	r : (J,Q) array of residuals
		J  = number of observations
		Q  = number of field nodes
	
	method : "rft1d" (default), "barnes2013" or "taylor2007"
	'''
	
	if method=='rft1d':
		fwhm = _estimate_fwhm_rft1d(r, roi=roi)
	elif method == 'barnes2013':
		lkc  = _estimate_lkc_barnes2013(r)
		fwhm = lkc2fwhm( lkc, r.shape[1] )
	elif method == 'taylor2007':
		lkc  = _estimate_lkc_taylor2007(r)
		fwhm = lkc2fwhm( lkc, r.shape[1] )
	else:
		raise ValueError( f'Unknown method: "{method}". "method" must be one of: ["rft1d", "barnes2013", "taylor2007"]')
	return fwhm


def estimate_fwhm_mv(r, method='taylor2008'):
	'''
	Estimate FWHM (smoothness) from multivariate residuals
	
	r : (J,Q,I) array of residuals;
		J  = number of observations
		Q  = number of field nodes
		I  = number of vector components
	
	method : "taylor2008" (default), "spm1d-v04" (old method for legacy purposes only)
	'''
	if method == 'taylor2008':
		lkc  = _estimate_lkc_mv_taylor2008(r)
		fwhm = lkc2fwhm( lkc, r.shape[1] )
	elif method == 'spm1d-v04':  # this method was implemented in spm1d-v0.4.x but the Taylor 2008 method is better
		fwhm   = np.mean(   [estimate_fwhm(r[:,:,i], method='rft1d')  for i in range(r.shape[2])]   ) 
	else:
		raise ValueError( f'Unknown method: "{method}". "method" must be one of: ["taylor2008", "spm1d-v04"]')
	return fwhm
	



def _resel_counts(R, fwhm=1, element_based=False):
	'''
	(Modified from rft1d.geom.resel_counts)
	Resel counts for continuous, unbroken fields
	'''
	if R.ndim==2:
		b     = np.any( np.logical_not(np.isnan(R)), axis=0)
	else:
		b     = np.asarray(np.logical_not(R), dtype=bool)
	### Summarize search area geometry:
	nNodes    = b.sum()
	nClusters = bwlabel(b)[1]
	if element_based:
		resels    = nClusters,  float(nNodes)/fwhm
	else:
		resels    = nClusters,  float(nNodes-nClusters)/fwhm
	return resels


def resel_counts(r, fwhm=1, element_based=False, roi=None):
	'''
	Resel counts for continuous, broken or unbroken fields
	'''
	# define binary search area (False = masked):
	if roi is None: # continious, unbroken case
		resels = _resel_counts(r, fwhm, element_based)
	else:
		b      = np.any( np.isnan(r), axis=0)            # node is True if nan
		b      = np.logical_and(np.logical_not(b), roi)  # node is True if (in roi) and (not nan)
		mask   = np.logical_not(b)                       # True for masked-out regions
		resels = resel_counts(mask, fwhm, element_based)
	return resels
	
	
	
def resel_counts_mv(r, fwhm=1, element_based=False, roi=None):
	b            = np.any(np.any(np.abs(r)>0, axis=0), axis=1)  # False indicates no observations at that node
	if roi is not None:
		b      = np.logical_and(b, roi)  #node is true if in ROI and also not NaN
	mask       = np.logical_not(b)                       # True for masked-out regions
	resels     = resel_counts(mask, fwhm, element_based)
	return resels

	
	