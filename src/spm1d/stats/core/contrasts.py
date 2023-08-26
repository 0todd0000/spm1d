
import numpy as np
from . factors import Factor
from ... util import array2shortstr, arraytuple2str, dflist2str, objectlist2str, resels2str, DisplayParams


# class ContrastList( list ):
# 	pass
#
# 	# def __repr__(self):
# 	# 	return f'List of {len(self)} Contrast objects'
# 	#
# 	# def __repr__(self):
# 	# 	dp      = DisplayParams( self )
# 	# 	dp.add_default_header()
# 	# 	dp.add( 'name' )
# 	# 	dp.add( 'C' , array2shortstr )
# 	# 	return dp.asstr()



class Contrast(object):
	def __init__(self, C, factors, ind=0):
		self.C       = C       # contrast matrix
		self.factors = factors # list of Factor objects (used only for factor names)
		self.ind     = ind
		

	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		_afmt   = None if self.C.ndim == 1 else array2shortstr
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'name' )
		dp.add( 'C' , _afmt )
		dp.add( 'ind' )
		return dp.asstr()


	@property
	def isinteraction(self):
		return self.nfactors > 1
	@property
	def ismain(self):
		return self.nfactors == 1
	@property
	def effect_name(self):
		return None if (self.factors is None) else 'x'.join( [f.name for f in self.factors] )
	@property
	def effect_name_s(self):
		return None if (self.factors is None) else 'x'.join( [f.name_s for f in self.factors] )
	@property
	def effect_type(self):
		if self.factors is None:
			s = 'Regress'
		elif self.ismain:
			s = 'Main'
		else:
			s = 'Interaction'
		return s
	@property
	def factor_names(self):
		return None if (self.factors is None) else [f.name for f in self.factors]
	@property
	def nfactors(self):
		return 0 if (self.factors is None) else len( self.factors )

	@property
	def name(self):
		return f'{self.effect_type} {self.effect_name}'
	
	@property
	def name_s(self):
		return self.effect_name_s
		
	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
			
		if not np.all(self.C == other.C):
			return False
			
		if (self.factors is not None) and (other.factors is not None):
			for f0,f1 in zip(self.factors, other.factors):
				if f0 != f1:
					return False
				
		if self.ind != other.ind:
			return False

		return True
