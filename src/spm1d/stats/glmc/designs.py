


import numpy as np
from . contrasts import ContrastF, ContrastT
from . factors import Factor
from . _la import rank
from ... util import array2shortstr, arraytuple2str, dflist2str, object2str, objectlist2str, resels2str, DisplayParams



class _Design(object):
	
	def __init__(self):
		self.X             = None   # design matrix
		self.contrasts     = None   # contrast object
		self.df0           = None   # unadjusted degrees of freedom
	
	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_header( f'Design ({self.__class__.__name__})' )
		dp.add( 'testname' )
		dp.add( 'X' , array2shortstr )
		# dp.add( 'contrasts' , object2str )
		dp.add( 'contrasts' , objectlist2str )
		dp.add( 'df0' , dflist2str )
		return dp.asstr()
	
	def _calculate_unadjusted_df(self):
		df  = [c.rank  for c in self.contrasts]
		dfe = self.J - rank(self.X)
		df0 = [(x,dfe)  for x in df]
		if len(df0)==1:
			df0 = df0[0]
		return df0

	@property
	def J(self):
		return self.X.shape[0]
	@property
	def df0list(self):
		return [self.df0] if self.ncontrasts==1 else self.df0
	@property
	def ncontrasts(self):
		return len(self.contrasts)
	@property
	def testname(self):
		return self.__class__.__name__.lower()


	def get_contrast_matrices(self):
		return [c.c  for c in self.contrasts]
	
	def get_variance_model(self, equal_var=False):  # abstract method
		pass
	
	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
		if not np.array_equal(self.X, other.X):
			return False
		if self.contrasts != other.contrasts:
			return False
		if self.df0 != other.df0:
			return False
		return True

	# def set_factor_names(self, names, names_short=None):
	# 	# self.set_factor_names(names, names_short)
	# 	if names_short is None:
	# 		names_short = [None] * self.nfactors
	# 	for factor,s,ss in zip(self.factors, names, names_short):
	# 		factor.set_name( s, ss )

# def _array2contrast(a, ind=None):
# 	return ContrastT(a) if a.ndim==1 else ContrastF(a, factors=None, ind=ind)

def _array2contrast(a, ind=None):
	return ContrastT(a) if a.ndim==1 else ContrastF(a, ind=ind)


class GLM(_Design):
	def __init__(self, X, c):
		self.X         = X
		self._c        = c
		self.contrasts = self._assemble_contrasts()
		self.df0       = self._calculate_unadjusted_df()

	def _assemble_contrasts(self):
		if isinstance(self._c, list):
			contrasts = [   _array2contrast( cc, ind=ii )  for ii,cc in enumerate(self._c) ]
		else:
			contrasts = [   _array2contrast( self._c )    ]
		return contrasts

	@property
	def ctype(self):
		return self.contrasts[0].type
	@property
	def has_contrast_list(self):
		return isinstance(self._c, list)  # and len(self._c)>1







# class REGRESS(_Design):
# 	def __init__(self, x):
# 		n              = x.size
# 		self.X         = np.ones((n,2))
# 		self.X[:,0]    = x
# 		c              = np.array( [1,0] )
# 		self.contrasts = [   Contrast( c, factors=None, ind=0 )   ]
# 		self.df0       = 1, n-2


# class TTEST(_Design):
# 	def __init__(self, n):
# 		self.X             = np.ones((n,1))
# 		A                  = np.ones(n)
# 		C                  = np.array( [1,] )
# 		self.factors       = [ Factor(A, name='A') ]
# 		self.contrasts     = [   Contrast( C, factors=self.factors, ind=0 )   ]
# 		self.df0           = (1, n-1)

# class TTEST2(_Design):
# 	def __init__(self, n0, n1):
# 		self.X             = np.zeros((n0+n1,2))
# 		self.X[:n0,0]      = 1
# 		self.X[n0:,1]      = 1
# 		A                  = np.array( [0]*n0 + [1]*n1 )
# 		C                  = np.array( [1,-1] )
# 		self.factors       = [ Factor(A, name='A') ]
# 		self.contrasts     = [   Contrast( C, factors=self.factors, ind=0 )   ]
# 		self.df0           = 1, n0+n1-2
#
#
# 	def get_variance_model(self, equal_var=False):
# 		if equal_var:
# 			QQ  = None
# 		else:
# 			A,u = self.factors[0].A, self.factors[0].u
# 			QQ  = [np.asarray(np.diag( A==uu ), dtype=float)  for uu in u]
# 		return QQ


class REGRESS(_Design):
	def __init__(self, x):
		n              = x.size
		self.X         = np.ones((n,2))
		self.X[:,0]    = x
		self.contrasts = [ContrastT( [1,0] )]
		self.df0       = (1, n-2)

class TTEST(_Design):
	def __init__(self, n):
		self.X         = np.ones((n,1))
		self.contrasts = [ContrastT( [1,] )]
		self.df0       = (1, n-1)


class TTEST2(_Design):
	def __init__(self, n0, n1):
		self.X             = np.zeros((n0+n1,2))
		self.X[:n0,0]      = 1
		self.X[n0:,1]      = 1
		self.contrasts     = [ContrastT( [1,-1] )]
		self.df0           = (1, n0+n1-2)

	def get_variance_model(self, equal_var=False):
		if equal_var:
			QQ  = None
		else:
			QQ  = [np.asarray(np.diag( x==1 ), dtype=float)  for x in self.X.T]
		return QQ


# class _DesignANOVA(object):
# 	def __init__(self):
# 		self.X             = None   # design matrix
# 		self.contrasts     = None   # contrast objects
# 		self.factors       = None   # list of factor objects
#
# 	def __eq__(self, other):
# 		return self.isequal(other, verbose=False)
#
# 	def __repr__(self):
# 		dp      = DisplayParams( self )
# 		dp.add_header( f'Design ({self.__class__.__name__})' )
# 		dp.add( 'testname' )
# 		dp.add( 'X' , array2shortstr )
# 		dp.add( 'contrasts' , objectlist2str )
# 		return dp.asstr()
#
# 	def _init_factors(self, *AA):
# 		self.factors = [Factor(A, name=chr(65+i))   for i,A in enumerate(AA)]
#
#
# 	@property
# 	def C(self):
# 		return self.get_contrast_matrices()
# 	@property
# 	def J(self):
# 		return self.X.shape[0]
# 	@property
# 	def nfactors(self):
# 		return len( self.factors )
# 	@property
# 	def testname(self):
# 		return self.__class__.__name__.lower()
#
# 	def _assemble(self):
# 		self.X         = self._build_design_matrix()
# 		self.contrasts = self._build_contrasts()
#
# 	def isequal(self, other, verbose=False):
# 		if type(self) != type(other):
# 			return False
#
# 		if not np.all(self.X == other.X):
# 			return False
#
# 		for c0,c1 in zip(self.contrasts, other.contrasts):
# 			if c0 != c1:
# 				return False
#
# 		if (self.factors is not None) and (other.factors is not None):
# 			for f0,f1 in zip(self.factors, other.factors):
# 				if f0 != f1:
# 					return False
#
# 		return True
#
# 	def get_contrast_matrices(self):
# 		return [c.C  for c in self.contrasts]
#
# 	def set_factor_names(self, names, names_short=None):
# 		# self.set_factor_names(names, names_short)
# 		if names_short is None:
# 			names_short = [None] * self.nfactors
# 		for factor,s,ss in zip(self.factors, names, names_short):
# 			factor.set_name( s, ss )


class _DesignANOVA(_Design):
	def _assemble(self):
		self.X         = self._build_design_matrix()
		self.contrasts = self._build_contrasts()
		self.df0       = self._calculate_unadjusted_df()

	@property
	def nfactors(self):
		return len(self.factors)
	
	# def _calculate_unadjusted_df(self):
	# 	df  = [c.rank for c in self.contrasts]
	# 	dfe = self.J - rank(self.X)
	# 	df0 = [(x,dfe)  for x in df]
	# 	return df0
	
	def _init_factors(self, *AA):
		self.factors = [Factor(A, name=chr(65+i))   for i,A in enumerate(AA)]

	


class ANOVA1(_DesignANOVA):
	def __init__(self, A):
		self.factors      = [ Factor(A, name='A') ]
		self._assemble()

	def _build_contrasts(self):
		n        = self.factors[0].nlevels
		C        = np.zeros( (n-1, n) )
		for i in range(n-1):
			C[i,i]   = 1
			C[i,i+1] = -1
		# C = ContrastF( C.T, factorors=self.factors, ind=0 )
		C = ContrastF( C.T, name='Main A', ind=0 )
		return [C]

	def _build_design_matrix(self):
		return self.factors[0].get_design_main()
		
	# def get_variance_model(self, equal_var=False):
	# 	if equal_var:
	# 		# Q   = [np.eye(self.J)]
	# 		QQ  = None
	# 	else:
	# 		A,u = self.factors[0].A, self.factors[0].u
	# 		QQ  = [np.asarray(np.diag( A==uu ), dtype=float)  for uu in u]
	# 	return QQ
	
	def get_variance_model(self, equal_var=False):
		if equal_var:
			QQ  = None
		else:
			from ._cov import gen_vc_model
			A   = self.factors[0].A
			QQ  = gen_vc_model(  np.array([A]).T , [1], [0]  )
		return QQ
	
	
	
class ANOVA1RM(_DesignANOVA):
	def __init__(self, A, SUBJ):
		self.factors      = [ Factor(A, name='A'), Factor(SUBJ, name='SUBJ') ]
		self._assemble()

	# @property
	# def df0(self):
	# 	n     = self.factors[0].n
	# 	df_w  = self.J - n
	# 	df_b  = int( self.J / n ) - 1
	# 	df    = n - 1, df_w - df_b
	# 	return df

	def _build_contrasts(self):
		n        = self.factors[0].nlevels
		C        = np.zeros( (n-1, n) )
		for i in range(n-1):
			C[i,i]   = 1
			C[i,i+1] = -1

		nz       = self.factors[1].nlevels
		Cz       = np.zeros(  (n-1,  nz)  )
		C        = np.hstack([C, Cz])
		# return [C.T]
		# C = ContrastF( C.T, factors=self.factors, ind=0, isrm=True )
		C = ContrastF( C.T, name='Main A', ind=0, isrm=True )
		return [C]



	def _build_design_matrix(self):
		XA       = self.factors[0].get_design_main()
		XS       = self.factors[1].get_design_main()
		return np.hstack( [XA, XS] )


	# def get_variance_model(self, equal_var=False):
	# 	if equal_var:
	# 		# QQ  = [np.eye(self.J)]
	# 		QQ  = None
	# 	else:
	# 		A,u = self.factors[0].A, self.factors[0].u
	# 		QQ  = [np.asarray(np.diag( A==uu ), dtype=float)  for uu in u]
	#
	# 		n   = (A == u[0]).sum()
	# 		for i,a0 in enumerate(u):
	# 			for a1 in u[i+1:]:
	# 				q   = np.zeros( (self.J, self.J) )
	# 				i0  = np.argwhere(A==a0).flatten()  # rows
	# 				i1  = np.argwhere(A==a1).flatten()  # columns
	# 				for ii0,ii1 in zip(i0,i1):
	# 					q[ii0,ii1] = 1
	# 				QQ.append( q + q.T )
	# 	return QQ

	def get_variance_model(self, equal_var=False):
		if equal_var:
			QQ  = None
		else:
			from ._cov import gen_vc_model
			A   = self.factors[0].A
			S   = self.factors[1].A
			QQ  = gen_vc_model(  np.vstack([A,S]).T , [1,0], [0,1]  )
		return QQ






class ANOVA2(_DesignANOVA):
	def __init__(self, A, B):
		self._init_factors( A, B )
		self._assemble()

	# @property
	# def df0(self):
	# 	return None # self._df0

	def _build_contrasts(self):
		# from . contrasts import Contrast #, ContrastList

		fA,fB = self.factors
		n     = self.X.shape[1]
		nA    = fA.n - 1
		nB    = fB.n - 1
		nAB   = nA * nB

		CA = []
		for i in range(nA):
			c   = np.zeros(n)
			c[i] = 1
			CA.append(c)
		# CA = Contrast( np.asarray(CA).T, name=f'Main {fA.name}', name_s=fA.name_s )
		CA = ContrastF( np.asarray(CA).T, name='Main A', ind=0 )


		CB = []
		for i in range(nB):
			c   = np.zeros(n)
			c[nA+i] = 1
			CB.append(c)
		# CB = Contrast( np.asarray(CB).T, name=f'Main {fB.name}', name_s=fB.name_s )
		CB = ContrastF( np.asarray(CB).T, name='Main B', ind=1 )



		CAB  = []
		for i in range(nAB):
			c   = np.zeros(n)
			c[nA+nB+i] = 1
			CAB.append(c)
		# CAB = Contrast( np.asarray(CAB).T, name=f'Interaction {fA.name} x {fB.name}', name_s=f'{fA.name_s}x{fB.name_s}' )
		CAB = ContrastF( np.asarray(CAB).T, name='Interaction AB', ind=2 )

		return [CA, CB, CAB]



	def _build_design_matrix(self):
		fA,fB     = self.factors
		XA        = fA.get_design_mway_main()
		XB        = fB.get_design_mway_main()
		XAB       = np.asarray(  [np.kron( XA[i], XB[i] )   for i in range(XA.shape[0])] )
		X0        = fA.get_design_intercept()
		X         = np.hstack( [XA, XB, XAB, X0] )
		return X

	def get_variance_model(self, equal_var=False):
		if equal_var:
			QQ  = None
		else:
			from ._cov import gen_vc_model
			A   = self.factors[0].A
			B   = self.factors[1].A
			QQ  = gen_vc_model(  np.vstack([A,B]).T , [1,1], [0,1]  )
		return QQ
		

