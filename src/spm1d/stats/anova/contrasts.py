
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
		

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'name' )
		dp.add( 'C' , array2shortstr )
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
		return 'x'.join( [f.name for f in self.factors] )
	@property
	def effect_name_s(self):
		return 'x'.join( [f.name_s for f in self.factors] )
	@property
	def effect_type(self):
		return 'Main' if self.ismain else 'Interaction'
	@property
	def factor_names(self):
		return [f.name for f in self.factors]
	@property
	def nfactors(self):
		return len(self.factors)

	@property
	def name(self):
		return f'{self.effect_type} {self.effect_name}'
	
	@property
	def name_s(self):
		return self.effect_name_s
