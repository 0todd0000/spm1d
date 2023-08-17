
# Copyright (C) 2023  Todd Pataky



import numpy as np
from . fit import GLMFit
from ... util import array2shortstr, arraylist2str, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams









class GeneralLinearModel(object):
	def __init__(self):
		self.QQ   = None   # (co-)variance model
		self.X    = None   # design matrix

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'X' , array2shortstr )
		# dp.add( 'QQ' , arraylist2str, 'covariance component models' )
		return dp.asstr()
	
	@property
	def J(self):
		return None if (self.X is None) else self.X.shape[0]

	def fit(self, y):
		# y0     = y.copy()
		y      = np.asarray(y, dtype=float)
		y      = y if (y.ndim==2) else np.array([y]).T
		Xi     = np.linalg.pinv( self.X )
		b      = Xi @ y
		e      = y - self.X @ b
		return GLMFit(self, y, b, e)

	def set_design_matrix(self, X):
		self.X       = X
	# def set_variance_model(self, QQ):
	# 	self.QQ      = QQ





