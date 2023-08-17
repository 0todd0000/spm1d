

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


