
import numpy as np
from ... util import array2shortstr, arraylist2str, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams



class _TestStatistic(object):
	
	_attrs2test    = ['STAT', 'C', 'z', 'df']
	
	def __init__(self, z, df, C):
		self.STAT  = 'T'
		self.C     = C
		self.z     = z
		self.df    = df
		
	def __eq__(self, other):
		return self.isequal(other, verbose=False)
	
	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'STAT' )
		dp.add( 'C', array2shortstr )
		_astr      = array2shortstr if self.dvdim==1 else None
		dp.add( 'z', _astr )
		dp.add( 'df', dflist2str )
		return dp.asstr()
		
	@property
	def dvdim(self):
		return 0 if isinstance(self.z, float) else 1

	def isequal(self, other, verbose=False):
		if type(self) != type(other):
			return False
		for s in self._attrs2test: 
			x0,x1  = getattr(self, s), getattr(other, s)
			if not np.all(x0 == x1):
				return False
		return True
		
		

class TestStatisticT(_TestStatistic):
	pass


class TestStatisticF(_TestStatistic):
	
	_attrs2test    = ['STAT', 'C', 'z', 'df', 'v', 'ss', 'ms', 'ind']
	
	def __init__(self, f, df, v, ss, ms, C, ind=0):
		self.STAT  = 'F'
		self.C     = C
		self.z     = f
		self.df    = df
		self.v     = v     # unadjusted degrees of freedom
		self.ss    = ss
		self.ms    = ms
		self.ind   = ind

	def __repr__(self):
		s0      = super().__repr__()
		dp      = DisplayParams( self )
		_astr   = array2shortstr if self.dvdim==1 else None
		dp.add( 'ms', _astr )
		dp.add( 'ss', _astr )
		dp.add( 'ind' )
		return s0 + dp.asstr()

