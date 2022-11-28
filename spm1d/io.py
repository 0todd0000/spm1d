

'''
Input/Output module

.. warning:: This module has been deprecated and will be removed in the future.

	All spm1d procedures accept NumPy arrays directly, and NumPy load/save
	functionality has greatly improved in the last few years, so spm1d-specific
	data IO has been made redundant. Consider using the following functions:
	
	* numpy.loadtxt
	* numpy.savetxt
	* numpy.load
	* numpy.save
	* scipy.io.loadmat
	* scipy.io.savemat
'''

# Copyright (C) 2016  Todd Pataky
# updated (2016/10/01) todd



class Deprecated(object):
	def __init__(self, f):
		fnname     = 'spm1d.io.' + f.__name__
		self.msg   = '"%s" has been deprecated.  The "spm1d.io" module will be removed in the future.' %fnname
	def __call__(self, *args):
		raise( DeprecationWarning( self.msg ) )



@Deprecated
def load(*args):
	pass
@Deprecated
def loadmat(*args):
	pass
@Deprecated
def loadspm(*args):
	pass
@Deprecated
def loadtxt(*args):
	pass


@Deprecated
def save(*args):
	pass
@Deprecated
def savemat(*args):
	pass
@Deprecated
def savespm(*args):
	pass
@Deprecated
def savetxt(*args):
	pass


