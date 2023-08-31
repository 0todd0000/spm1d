
# Copyright (C) 2023  Todd Pataky



import numpy as np
# from . fit import GLMFit #, GLMFitANOVA
from ... util import array2shortstr, arraylist2str, arraylist2strnone, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams





class GeneralLinearModel(object):
	
	def __init__(self, X, df0, QQ=None):
		self.QQ   = QQ     # (co-)variance model
		self.X    = X      # design matrix
		self.df0  = df0

	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'X' , array2shortstr )
		dp.add( 'df0' , dflist2str )
		dp.add( 'QQ' , arraylist2strnone )
		return dp.asstr()
	
	@property
	def J(self):
		return None if (self.X is None) else self.X.shape[0]

	@property
	def dfe0(self):
		return self.df0[0][1] if isinstance(self.df0, list) else self.df0[1]

	def fit(self, y):
		from . fit import GLMFit
		y      = np.asarray(y, dtype=float)
		y      = y if (y.ndim==2) else np.array([y]).T
		Xi     = np.linalg.pinv( self.X )
		b      = Xi @ y
		e      = y - self.X @ b
		return GLMFit(self, y, b, e, Xi)

	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
			
		if (self.QQ is not None) and (other.QQ is not None):
			for Q0,Q1 in zip(self.QQ, other.QQ):
				if not np.all(Q0 == Q1):
					return False

		if not np.all(self.X == other.X):
			return False

		return True

	# def set_design_matrix(self, X):
	# 	self.X  = X
	# def set_variance_model(self, QQ):
	# 	self.QQ = QQ

