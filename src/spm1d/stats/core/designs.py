


import numpy as np
from . contrasts import Contrast
from . factors import Factor
from ... util import array2shortstr, arraytuple2str, dflist2str, objectlist2str, resels2str, DisplayParams



class _Design(object):
	def __init__(self):
		self.X             = None   # design matrix
		self.contrasts     = None   # contrast objects
		self.factors       = None   # list of factor objects
		
	
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
	
	def set_factor_names(self, names, names_short=None):
		# self.set_factor_names(names, names_short)
		if names_short is None:
			names_short = [None] * self.nfactors
		for factor,s,ss in zip(self.factors, names, names_short):
			factor.set_name( s, ss )



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
		
