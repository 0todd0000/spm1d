
import numpy as np
from ... util import array2shortstr, arraylist2str, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams


class TestStatisticT(object):
	def __init__(self, z, df, C, ind=0):
		self.STAT  = 'T'
		self.C     = C
		# self.ind   = ind
		self.z     = z
		self.df    = df
		# self.v     = v
		# self.ss    = ss
		# self.ms    = ms
		
	def __eq__(self, other):
		return self.isequal(other, verbose=False)
	
	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'STAT' )
		dp.add( 'C', array2shortstr )
		# dp.add( 'ind' )
		_astr      = array2shortstr if self.dvdim==1 else None
		dp.add( 'z', _astr )
		dp.add( 'df', dflist2str )
		# dp.add( 'ms', _astr )
		# dp.add( 'ss', _astr )
		return dp.asstr()
		
		
	@property
	def dvdim(self):
		return 0 if isinstance(self.z, float) else 1


	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
			
		if self.STAT != other.STAT:
			return False
		
		if not self.df == other.df:
			return False

		for s in ['C', 'z']: 
			x0,x1  = getattr(self, s), getattr(other, s)
			if not np.all(x0 == x1):
				return False

		return True
		
		

class TestStatisticF(object):
	def __init__(self, f, df, v, ss, ms, C, ind=0):
		self.STAT  = 'F'
		self.C     = C
		self.ind   = ind
		self.z     = f
		self.df    = df
		self.v     = v
		self.ss    = ss
		self.ms    = ms
		
	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'STAT' )
		dp.add( 'C', array2shortstr )
		dp.add( 'ind' )
		_astr      = array2shortstr if self.dvdim==1 else None
		dp.add( 'z', _astr )
		dp.add( 'df', dflist2str )
		dp.add( 'ms', _astr )
		dp.add( 'ss', _astr )
		return dp.asstr()
		
		
	@property
	def dvdim(self):
		return 0 if isinstance(self.z, float) else 1


	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
			
		if self.STAT != other.STAT:
			return False
		
		if not self.df == other.df:
			return False

		for s in ['C', 'z']: 
			x0,x1  = getattr(self, s), getattr(other, s)
			if not np.all(x0 == x1):
				return False

		return True