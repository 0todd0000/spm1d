

'''
Utility module

This module contains a variety of convenience functions, including:

- get_dataset
- interp
- p_corrected_bonf
- p_critical_bonf
- smooth
'''

# Copyright (C) 2022  Todd Pataky
# updated (2022/02/06) todd



from math import sqrt,log
import numpy as np
from . stats._spm import plist2string as p2s
# from scipy.ndimage.filters import gaussian_filter1d
from scipy.ndimage import gaussian_filter1d






def plist2stringlist(pList):
	s  = p2s(pList).split(', ')
	for i,ss in enumerate(s):
		if ss.startswith('<'):
			s[i]  = 'p' + ss
		else:
			s[i]  = 'p=' + ss
	return s



def get_dataset(*args):
	'''
	.. warning:: Deprecated
		
		**get_dataset** is deprecated and will be removed from future versions of **spm1d**.  Please access datasets using the "spm1d.data" interface.
	'''
	raise( IOError('"get_dataset" is deprecated.  Please access datasets using "spm1d.data".') )



def interp(y, Q=101):
	'''
	Simple linear interpolation to *n* values.
	
	:Parameters:
	
	- *y* --- a 1D array or list of J separate 1D arrays
	- *Q* --- number of nodes in the interpolated continuum
	
	:Returns:
	
	- Q-component 1D array or a (J x Q) array
	
	:Example:
	
	>>> y0 = np.random.rand(51)
	>>> y1 = np.random.rand(87)
	>>> y2 = np.random.rand(68)
	>>> Y  = [y0, y1, y2]
	
	>>> Y  = spm1d.util.interp(Y, Q=101)
	'''
	y          = np.asarray(y)
	if (y.ndim==2) or (not np.isscalar(y[0])):
		return np.asarray( [interp(yy, Q)   for yy in y] )
	else:
		x0     = range(y.size)
		x1     = np.linspace(0, y.size, Q)
		return np.interp(x1, x0, y, left=None, right=None)






def p_corrected_bonf(p, n):
	'''
	Bonferroni-corrected *p* value.
	
	.. warning:: This correction assumes independence amongst multiple tests.
	
	:Parameters:
	
	- *p* --- probability value computed from one of multiple tests
	- *n* --- number of tests
	
	:Returns:
	
	- Bonferroni-corrected *p* value.
	
	:Example:
	
	>>> p = spm1d.util.p_corrected_bonf(0.03, 8)    # yields p = 0.216
	'''
	if p<=0:
		return 0
	elif p>=1:
		return 1
	else:
		pBonf  = 1 - (1.0-p)**n
		pBonf  = max(0, min(1, pBonf))
		return pBonf



def p_critical_bonf(alpha, n):
	'''
	Bonferroni-corrected critical Type I error rate.
	
	.. warning:: This crticial threshold assumes independence amongst multiple tests.
	
	:Parameters:
	
	- *alpha* --- original Type I error rate (usually 0.05)
	- *n* --- number of tests
	
	:Returns:
	
	- Bonferroni-corrected critical *p* value; retains *alpha* across all tests.
	
	:Example:
	
	>>> p = spm1d.util.p_critical_bonf(0.05, 20)    # yields p = 0.00256
	'''
	if alpha<=0:
		return 0
	elif alpha>=1:
		return 1
	else:
		return 1 - (1.0-alpha)**(1.0/n)




def smooth(Y, fwhm=5.0):
	'''
	Smooth a set of 1D continua.
	This method uses **scipy.ndimage.filters.gaussian_filter1d** but uses the *fwhm*
	instead of the standard deviation.
	
	:Parameters:
	
	- *Y* --- a (J x Q) numpy array
	- *fwhm* ---  Full-width at half-maximum of a Gaussian kernel used for smoothing.
	
	:Returns:
	
	- (J x Q) numpy array
	
	:Example:
	
	>>> Y0  = np.random.rand(5, 101)
	>>> Y   = spm1d.util.smooth(Y0, fwhm=10.0)
	
	.. note:: A Gaussian kernel's *fwhm* is related to its standard deviation (*sd*) as follows:
	
	>>> fwhm = sd * sqrt(8*log(2))
	'''
	sd    = fwhm / sqrt(8*log(2))
	return gaussian_filter1d(Y, sd, mode='wrap')
