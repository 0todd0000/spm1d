

'''
Input/Output module

This module contains functions for loading and saving data, including
SPMs.

.. warning:: most functions in **spm1d.io** are deprecated.

	Please use the following well-supported functions:
	
	* numpy.loadtxt
	* numpy.savetxt
	* numpy.load
	* numpy.save
	* scipy.io.loadmat
	* scipy.io.savemat
'''

# Copyright (C) 2016  Todd Pataky
# io.py version: 0.3.2 (2016/01/03)



import numpy as np
from scipy.io import loadmat as scipy_loadmat
from scipy.io import savemat as scipy_savemat
from stats import _spm



def _check4pytables():
	try:
		import tables
	except ImportError:
		raise(ImportError('You must install pytables to use spm1d.io.load'))
	



def load(fname):
	'''
	WARNING:  "spm1d.io.load" is deprecated and will be removed from future versions of spm1d. 
	'''
	_check4pytables()
	import tables
	fid  = tables.openFile(fname, mode='r')
	Y    = fid.getNode('/Y').read()
	fid.close()
	return Y


def loadmat(fname):
	'''
	WARNING:  "spm1d.io.loadmat" is deprecated.  Use "scipy.io.loadmat" instead. 
	'''
	raise DeprecationWarning('"spm1d.io.loadmat" is deprecated.  Use "scipy.io.loadmat" instead')


def loadspm(fname):
	'''
	Load an SPM object from disk.
	The SPM file should have been saved in zipped NumPy (NPZ) format using **spm1d.io.savespm**.
	
	:Parameters:
	
	fname : a string specifying the file name
	
	:Returns:
	
	An **spm1d** SPM object.
	'''
	Z           = np.load(fname)
	keys        = Z.keys()
	STAT        = str( Z['STAT'] )
	X           = Z['X']
	beta        = Z['beta']
	residuals   = Z['residuals']
	z           = Z['z']
	df          = tuple( Z['df'] )
	fwhm        = float( Z['fwhm'] )
	resels      = tuple( Z['resels'] )
	if 'alpha' in keys:
		alpha   = float( Z['alpha'] )
		zstar   = float( Z['zstar'] )
		p       = tuple( Z['p'] )
		nClusters = int( Z['nClusters'] )
		L       = Z['L']
		two_tailed = bool( Z['two_tailed'] )
	if (STAT=='F') and ('alpha' in keys):
		pass
	elif STAT=='F':
		spm     = _spm.SPM_F(z, df, fwhm, resels, X, beta, residuals)
		if 'alpha' in keys:
			spm = _spm.SPMi_F(spm, alpha, zstar, nClusters, L, p, two_tailed)
	elif STAT=='T':
		spm     = _spm.SPM_T(z, df, fwhm, resels, X, beta, residuals)
		if 'alpha' in keys:
			spm = _spm.SPMi_T(spm, alpha, zstar, nClusters, L, p, two_tailed)
	return spm


def loadtxt(fname):
	'''
	WARNING:  "spm1d.io.loadtxt" is deprecated.  Use "numpy.loadtxt" instead. 
	'''
	raise DeprecationWarning('"spm1d.io.loadtxt" is deprecated.  Use "numpy.loadtxt" instead.')
	return np.loadtxt(fname, delimiter='\t')


def save(fname, Y):
	'''
	WARNING:  "spm1d.io.save" is deprecated and will be removed from future versions of spm1d.
	'''
	_check4pytables()
	import tables
	### create file (existing file will be overwritten)
	fid          = tables.openFile(fname, mode='w')
	try:
		### write data:
		atom     = tables.FloatAtom()
		filter0  = tables.Filters(complevel=5,complib='zlib')
		CA       = fid.createCArray(fid.root, 'Y', atom, Y.shape, filters=filter0)
		CA[:]    = Y
		fid.close()
	except IOError:
		fid.close()
		raise IOError('Error saving file.')


def savemat(fname, Y):
	'''
	WARNING:  "spm1d.io.savemat" is deprecated.  Use "scipy.io.savemat" instead. 
	'''
	raise DeprecationWarning('"spm1d.io.savemat" is deprecated.  Use "scipy.io.savemat" instead.')



def savespm(fname, spm):
	'''
	Save an SPM object in zipped NumPy (NPZ) format. Once saved an SPM can be re-loaded using **spm1d.io.loadspm**
	
	:Parameters:
	
	fname : a string specifying the file name (with extension .npz)
	
	spm   : an SPM object, as returned from a statistical test in **spm1d.stats**
	'''
	if not isinstance(spm, (_spm._SPM, _spm._SPMinference)):
		raise IOError('Must submit an SPM or SPMi object to spm1d.io.save_spm')
	fields      = ['STAT', 'Q', 'X', 'z', 'df', 'fwhm', 'resels', 'beta', 'residuals']
	if isinstance(spm, _spm._SPMinference):
		fields += ['alpha', 'zstar', 'p', 'nClusters', 'L', 'two_tailed']
	values      = [eval('spm.%s' %field)  for field in fields]
	np.savez(fname, **dict(zip(fields,values)) )


def savetxt(fname, Y):
	'''
	WARNING:  "spm1d.io.savetxt" is deprecated.  Use "numpy.savetxt" instead. 
	'''
	raise DeprecationWarning('"spm1d.io.savetxt" is deprecated.  Use "numpy.savetxt" instead.')



