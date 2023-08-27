
'''
Common parametric (0D) probabilities
'''

import numpy as np
from .. util import array2shortstr, arraytuple2str, dflist2str, float2string, largeint2str, resels2str, p2string, p2string5, plist2string, DisplayParams
from .. util import p2string_none, plist2string_none, float2string_none



class ParamResults(object):
	
	isparametric      = True
	method            = 'param'
	
	def __init__(self, STAT, z, alpha, dirn, zc, p):
		self.STAT     = STAT
		self.z        = z
		self.alpha    = alpha
		self.dirn     = dirn
		self.zc       = zc
		self.p        = p
		self.extras   = {}
		
	def __eq__(self, other):
		return self.isequal(other, verbose=False)

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_header( 'Inference results:' )
		dp.add( 'method' )
		dp.add( 'isparametric' )
		dp.add( 'alpha' )
		if self.STAT == 'T':
			dp.add( 'dirn' )
		dp.add( 'zc', float2string_none )
		dp.add( 'h0reject' )
		dp.add( 'p', p2string5 )
		return dp.asstr()

	@property
	def h0reject(self):
		zc       = self.zc
		if zc is None:
			return False
		if self.dirn in (None,1):
			h       = self.z > zc
		elif self.dirn==0:
			h       = (self.z < -zc) or (self.z > zc)
		elif self.dirn==-1:
			h       = self.z < -zc
		return h

	def isequal(self, other, verbose=False):
		import pytest
		if type(self) != type(other):
			return False
			
		for s in ['STAT', 'alpha', 'dirn', 'p', 'z', 'zc']:
			x0,x1  = getattr(self, s), getattr(other, s)
			if s in ['p', 'z', 'zc']:
				if not x0 == pytest.approx(x1):
					return False
			else:
				if not x0 == x1:
					return False
	
		return True

def isf_sf_t(z, df, alpha=0.05, dirn=0):
	import rft1d
	# critical value:
	a      = 0.5 * alpha if (dirn==0) else alpha
	zc     = rft1d.t.isf0d( a, df )
	zc     = -zc if (dirn==-1) else zc
	# p-value:
	zz     = np.abs(z) if (dirn==0) else dirn*z
	p      = rft1d.t.sf0d( zz, df )
	p      = min(1, 2*p) if (dirn==0) else p
	return zc,p



# def isf_sf_F(z, df, alpha=0.05):
# 	return zc,p


def param(STAT, z, df, alpha=0.05, dirn=None):
	import rft1d
	if STAT=='T':
		v    = df[1] if isinstance(df, (list,tuple,np.ndarray)) else df
		zc,p = isf_sf_t(z, v, alpha, dirn=dirn)
	elif STAT=='F':
		zc   = rft1d.f.isf0d( alpha, df )
		p    = rft1d.f.sf0d( z, df )
	elif STAT=='T2':
		zc   = rft1d.T2.isf0d( alpha, df )
		p    = rft1d.T2.sf0d( z, df )
	elif STAT=='X2':
		v    = df[1] if isinstance(df, (list,tuple,np.ndarray)) else df
		zc   = rft1d.chi2.isf0d( alpha, v )
		p    = rft1d.chi2.sf0d( z, v )
	else:
		raise ValueError( f'Unknown statistic: {stat}. Must be one of: ["T", "F", "T2", "X2"]' )
	results = ParamResults( STAT, z, alpha, dirn, zc, p )
	return results



	# ### non-sphericity:
	# Q        = None
	# if not equal_var:
	# 	J           = JA + JB
	# 	q0,q1       = np.eye(JA), np.eye(JB)
	# 	Q0,Q1       = np.matrix(np.zeros((J,J))), np.matrix(np.zeros((J,J)))
	# 	Q0[:JA,:JA] = q0
	# 	Q1[JA:,JA:] = q1
	# 	Q           = [Q0, Q1]