
import numpy as np
from . factors import Factor
from ... util import array2shortstr, arraytuple2str, dflist2str, objectlist2str, resels2str, DisplayParams



def nlevels2contrasts(k):
	# replicates functionality of SPM8's spm_make_contrasts.m
	nf = len(k)
	if nf == 1:
		k += [1,1]
	elif nf == 2:
		k += [1]
	elif nf > 3:
		raise ValueError('Automatic contrast generation is supported only for 1-, 2- and 3-way ANOVA')
	
	# common and differential vectors
	k0,k1,k2 = k
	C0   = np.ones((k0,1))
	C1   = np.ones((k1,1))
	C2   = np.ones((k2,1))
	D0   = -(  np.diff( np.eye(k0), axis=0 ).T  )
	D1   = -(  np.diff( np.eye(k1), axis=0 ).T  )
	D2   = -(  np.diff( np.eye(k2), axis=0 ).T  )

	def kronkron(aa, b):
		c = np.kron( np.kron(*aa), b ).T
		c[np.abs(c)<1e-9] = 0
		return c

	# cg   = np.kron( np.kron(C0, C1), C2 )  # global average
	c0     = kronkron( (D0,C1), C2 )
	c_main = [c0]
	c_intr = None
	
	if nf > 1:
		c1     = kronkron( (C0,D1), C2 )
		c01    = kronkron( (D0,D1), C2 )
		c_main.append( c1 )
		c_intr = [c01]
		
	if nf > 2:
		c2   = kronkron( (C0,C1), D2 )
		c02  = kronkron( (D0,C1), D2 )
		c12  = kronkron( (C0,D1), D2 )
		c012 = kronkron( (D0,D1), D2 )
		c_main.append( c2 )
		c_intr += [c02, c12, c012]
		
	return c_main, c_intr
	

def factors2contrasts(F):
	if isinstance(F, tuple):
		F = np.vstack( F ).T
	else:
		F = np.asarray(F)
	if F.ndim==1:
		k  = [np.unique(F).size]
	else:
		k  = [np.unique(f).size for f in F.T]
	return nlevels2contrasts(k)
	
	
	
class _Contrast(object):
	
	def __init__(self, c, name=None):
		self.c       = np.asarray(c)  # contrast vector
		self.name    = name
		self.type    = 'T'

	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		_afmt   = None if self.type=='T' else array2shortstr
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'name' )
		dp.add( 'c', _afmt )
		return dp.asstr()

	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
		if not np.array_equal(self.c, other.c):
			return False
		return True


class ContrastT(_Contrast):
	
	def __init__(self, c, name=None):
		self.c       = np.asarray(c)  # contrast vector
		self.name    = name
		self.type    = 'T'

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'name' )
		dp.add( 'c' )
		return dp.asstr()

	@property
	def rank(self):
		return 1


class ContrastF(_Contrast):
	def __init__(self, c, name=None, ind=0, isrm=False):
		self.c       = c        # contrast matrix
		self.ind     = ind      # list index (if contrast appears in a list of contrasts)
		self.isrm    = isrm
		self.name    = name
		self.type    = 'F'

	def __repr__(self):
		s       = super().__repr__()
		dp      = DisplayParams( self )
		dp.add( 'ind' )
		return s + dp.asstr()

	@property
	def name_s(self):
		return self.name.split(' ')[1]
		
	@property
	def rank(self):
		from . _la import rank
		return rank( self.c )



# class ContrastF(_Contrast):
# 	def __init__(self, c, factors, ind=0, isrm=False):
# 		self.c       = c        # contrast matrix
# 		self.factors = factors  # list of Factor objects (used only for factor names)
# 		self.ind     = ind      # list index (if contrast appears in a list of F contrasts)
# 		self.isrm    = isrm
# 		self.type    = 'F'
#
#
# 	def __eq__(self, other):
# 		return self.isequal(other, verbose=False)
#
# 	def __repr__(self):
# 		s       = super().__repr__()
# 		dp      = DisplayParams( self )
# 		dp.add( 'ind' )
# 		return s + dp.asstr()
#
#
# 	@property
# 	def isinteraction(self):
# 		return self.nfactors > 1
# 	@property
# 	def ismain(self):
# 		return self.nfactors == 1
# 	@property
# 	def effect_name(self):
# 		return None if (self.factors is None) else 'x'.join( [f.name for f in self.factors] )
# 	@property
# 	def effect_name_s(self):
# 		return None if (self.factors is None) else 'x'.join( [f.name_s for f in self.factors] )
# 	@property
# 	def effect_type(self):
# 		if self.factors is None:
# 			s = 'Regress'
# 		elif self.isrm:
# 			s = 'Main (RM)'
# 		elif self.ismain:
# 			s = 'Main'
# 		elif self.isrm:
# 			s
# 		else:
# 			s = 'Interaction'
# 		return s
# 	@property
# 	def factor_names(self):
# 		return None if (self.factors is None) else [f.name for f in self.factors]
# 	@property
# 	def nfactors(self):
# 		return 0 if (self.factors is None) else len( self.factors )
#
# 	@property
# 	def name(self):
# 		return f'{self.effect_type} {self.effect_name}'
#
# 	@property
# 	def name_s(self):
# 		return self.effect_name_s
#
# 	@property
# 	def rank(self):
# 		from . _la import rank
# 		return rank( self.c )
#
#
# 	def isequal(self, other, verbose=False):
# 		if not super().isequal():
# 			return False
# 		# if type(self) != type(other):
# 		# 	return False
# 		#
# 		# if not np.all(self.c == other.c):
# 		# 	return False
#
# 		if (self.factors is not None) and (other.factors is not None):
# 			for f0,f1 in zip(self.factors, other.factors):
# 				if f0 != f1:
# 					return False
#
# 		if self.ind != other.ind:
# 			return False
#
# 		return True



# class ContrastF(_Contrast):
# 	def __init__(self, C, factors, ind=0, isrm=False):
# 		self.C       = C        # contrast matrix
# 		self.factors = factors  # list of Factor objects (used only for factor names)
# 		self.ind     = ind      # list index (if contrast appears in a list of F contrasts)
# 		self.isrm    = isrm
# 		self.type    = 'F'
#
#
# 	def __eq__(self, other):
# 		return self.isequal(other, verbose=False)
#
# 	def __repr__(self):
# 		_afmt   = None if self.C.ndim == 1 else array2shortstr
# 		dp      = DisplayParams( self )
# 		dp.add_default_header()
# 		dp.add( 'name' )
# 		dp.add( 'C' , _afmt )
# 		dp.add( 'ind' )
# 		return dp.asstr()
#
#
# 	@property
# 	def isinteraction(self):
# 		return self.nfactors > 1
# 	@property
# 	def ismain(self):
# 		return self.nfactors == 1
# 	@property
# 	def effect_name(self):
# 		return None if (self.factors is None) else 'x'.join( [f.name for f in self.factors] )
# 	@property
# 	def effect_name_s(self):
# 		return None if (self.factors is None) else 'x'.join( [f.name_s for f in self.factors] )
# 	@property
# 	def effect_type(self):
# 		if self.factors is None:
# 			s = 'Regress'
# 		elif self.isrm:
# 			s = 'Main (RM)'
# 		elif self.ismain:
# 			s = 'Main'
# 		elif self.isrm:
# 			s
# 		else:
# 			s = 'Interaction'
# 		return s
# 	@property
# 	def factor_names(self):
# 		return None if (self.factors is None) else [f.name for f in self.factors]
# 	@property
# 	def nfactors(self):
# 		return 0 if (self.factors is None) else len( self.factors )
#
# 	@property
# 	def name(self):
# 		return f'{self.effect_type} {self.effect_name}'
#
# 	@property
# 	def name_s(self):
# 		return self.effect_name_s
#
# 	@property
# 	def rank(self):
# 		from . _la import rank
# 		return rank( self.C )
#
#
# 	def isequal(self, other, verbose=False):
# 		if type(self) != type(other):
# 			return False
#
# 		if not np.all(self.C == other.C):
# 			return False
#
# 		if (self.factors is not None) and (other.factors is not None):
# 			for f0,f1 in zip(self.factors, other.factors):
# 				if f0 != f1:
# 					return False
#
# 		if self.ind != other.ind:
# 			return False
#
# 		return True
#


# class Contrast(object):
#
# 	type             = 'F'
#
# 	def __init__(self, C, factors, ind=0, isrm=False):
# 		self.C       = C        # contrast matrix
# 		self.factors = factors  # list of Factor objects (used only for factor names)
# 		self.ind     = ind      # list index (if contrast appears in a list of F contrasts)
# 		self.isrm    = isrm
#
#
# 	def __eq__(self, other):
# 		return self.isequal(other, verbose=False)
#
# 	def __repr__(self):
# 		_afmt   = None if self.C.ndim == 1 else array2shortstr
# 		dp      = DisplayParams( self )
# 		dp.add_default_header()
# 		dp.add( 'name' )
# 		dp.add( 'C' , _afmt )
# 		dp.add( 'ind' )
# 		return dp.asstr()
#
#
# 	@property
# 	def isinteraction(self):
# 		return self.nfactors > 1
# 	@property
# 	def ismain(self):
# 		return self.nfactors == 1
# 	@property
# 	def effect_name(self):
# 		return None if (self.factors is None) else 'x'.join( [f.name for f in self.factors] )
# 	@property
# 	def effect_name_s(self):
# 		return None if (self.factors is None) else 'x'.join( [f.name_s for f in self.factors] )
# 	@property
# 	def effect_type(self):
# 		if self.factors is None:
# 			s = 'Regress'
# 		elif self.isrm:
# 			s = 'Main (RM)'
# 		elif self.ismain:
# 			s = 'Main'
# 		elif self.isrm:
# 			s
# 		else:
# 			s = 'Interaction'
# 		return s
# 	@property
# 	def factor_names(self):
# 		return None if (self.factors is None) else [f.name for f in self.factors]
# 	@property
# 	def nfactors(self):
# 		return 0 if (self.factors is None) else len( self.factors )
#
# 	@property
# 	def name(self):
# 		return f'{self.effect_type} {self.effect_name}'
#
# 	@property
# 	def name_s(self):
# 		return self.effect_name_s
#
# 	@property
# 	def rank(self):
# 		if self.C.ndim == 1:
# 			rnk = 1
# 		else:
# 			from . _la import rank
# 			rnk = rank( self.C )
# 		return rnk
#
#
#
# 	def isequal(self, other, verbose=False):
# 		if type(self) != type(other):
# 			return False
#
# 		if not np.all(self.C == other.C):
# 			return False
#
# 		if (self.factors is not None) and (other.factors is not None):
# 			for f0,f1 in zip(self.factors, other.factors):
# 				if f0 != f1:
# 					return False
#
# 		if self.ind != other.ind:
# 			return False
#
# 		return True

