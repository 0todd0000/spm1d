
import numpy as np
from ... util import array2shortstr, arraylist2str, arraytuple2str, dflist2str, objectlist2str, resels2str, scalarlist2string, DisplayParams



class _TestStatistic(object):
	
	_attrs2test    = ['STAT', 'C', 'z', 'df']
	
	def __init__(self, z, df, c, df0=None):
		self.STAT  = 'T'
		self.c     = c
		self.z     = z
		self.df    = df
		self.df0   = df0   # unadjusted degrees of freedom
		# print(df, df0)
		
	def __eq__(self, other):
		return self.isequal(other, verbose=False)
	
	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'STAT' )
		dp.add( 'c', array2shortstr )
		_astr      = array2shortstr if self.dvdim==1 else None
		dp.add( 'z', _astr )
		if self.df0 is not None:
			dp.add( 'df0', dflist2str )
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
	
	_attrs2test    = ['STAT', 'C', 'z', 'df', 'df0', 'ss', 'ms', 'ind']
	
	def __init__(self, f, df, ss, sse, ms, mse, c, ind=0, df0=None):
		self.STAT  = 'F'
		self.c     = c
		self.z     = f
		self.df0   = df0   # unadjusted degrees of freedom
		self.df    = df
		# self.v     = v     # unadjusted degrees of freedom
		self.ss    = ss
		self.sse   = sse
		self.ms    = ms
		self.mse   = mse
		self.ind   = ind

	def __repr__(self):
		s0      = super().__repr__()
		dp      = DisplayParams( self )
		_astr   = array2shortstr if self.dvdim==1 else None
		dp.add( 'ss', _astr )
		dp.add( 'sse', _astr )
		dp.add( 'ms', _astr )
		dp.add( 'mse', _astr )
		dp.add( 'ind' )
		return s0 + dp.asstr()

