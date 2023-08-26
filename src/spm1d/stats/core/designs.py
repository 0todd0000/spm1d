


import numpy as np
from . contrasts import Contrast
from . factors import Factor
from ... util import array2shortstr, arraytuple2str, dflist2str, objectlist2str, resels2str, DisplayParams



class _Design(object):
	def __init__(self):
		self.X             = None   # design matrix
		self.contrasts     = None   # contrast objects
		self.factors       = None   # list of factor objects
		
	
	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_header( f'Design ({self.__class__.__name__})' )
		dp.add( 'testname' )
		dp.add( 'X' , array2shortstr )
		dp.add( 'contrasts' , objectlist2str )
		return dp.asstr()
	
	def _init_factors(self, *AA):
		self.factors = [Factor(A, name=chr(65+i))   for i,A in enumerate(AA)]


	@property
	def C(self):
		return self.get_contrast_matrices()
	@property
	def J(self):
		return self.X.shape[0]
	@property
	def nfactors(self):
		return len( self.factors )
	@property
	def testname(self):
		return self.__class__.__name__.lower()
		
	def _assemble(self):
		self.X         = self._build_design_matrix()
		self.contrasts = self._build_contrasts()


	def get_contrast_matrices(self):
		return [c.C  for c in self.contrasts]
	
	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
			
		if not np.all(self.X == other.X):
			return False
			
		for c0,c1 in zip(self.contrasts, other.contrasts):
			if c0 != c1:
				return False

		for f0,f1 in zip(self.factors, other.factors):
			if f0 != f1:
				return False

		return True


	def set_factor_names(self, names, names_short=None):
		# self.set_factor_names(names, names_short)
		if names_short is None:
			names_short = [None] * self.nfactors
		for factor,s,ss in zip(self.factors, names, names_short):
			factor.set_name( s, ss )



class REGRESS(_Design):
	def __init__(self, x):
		# self.testname      = 'ttest'
		self.X             = None   # design matrix
		self.contrasts     = None   # contrast objects
		self.factors       = None   # list of factor objects
		
		# # n0,n1              = y0.shape[0], y1.shape[0]
		# A                  = np.array( [0]*n0 + [1]*n1 )
		# self.factors       = [ Factor(A, name='A') ]
		#
		# self.X             = np.zeros((n0+n1,2))
		# self.X[:n0,0]      = 1
		# self.X[n0:,1]      = 1
		# C                  = np.array( [1,-1] )
		# self.contrasts     = [   Contrast( C, factors=self.factors, ind=0 )   ]
		
		n              = x.size
		self.X         = np.ones((n,2))
		self.X[:,0]    = x
		c              = np.array( [1,0] )
		self.contrasts     = [   Contrast( c, factors=self.factors, ind=0 )   ]
		
		



class TTEST(_Design):
	def __init__(self, y, mu=0):
		# self.testname      = 'ttest'
		self.X             = None   # design matrix
		self.contrasts     = None   # contrast objects
		self.factors       = None   # list of factor objects
		
		n                  = y.shape[0]
		A                  = np.ones(n)
		self.factors       = [ Factor(A, name='A') ]
		
		self.X             = np.ones((n,1))
		C                  = np.array( [1,] )
		self.contrasts     = [   Contrast( C, factors=self.factors, ind=0 )   ]
		


class TTEST2(_Design):
	def __init__(self, n0, n1):
		# self.testname      = 'ttest'
		self.X             = None   # design matrix
		self.contrasts     = None   # contrast objects
		self.factors       = None   # list of factor objects
		
		# n0,n1              = y0.shape[0], y1.shape[0]
		A                  = np.array( [0]*n0 + [1]*n1 )
		self.factors       = [ Factor(A, name='A') ]
		
		self.X             = np.zeros((n0+n1,2))
		self.X[:n0,0]      = 1
		self.X[n0:,1]      = 1
		C                  = np.array( [1,-1] )
		self.contrasts     = [   Contrast( C, factors=self.factors, ind=0 )   ]
		


