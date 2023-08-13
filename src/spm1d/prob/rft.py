
'''
Common parametric (0D) probabilities
'''

import numpy as np
from .. geom import assemble_clusters
from .. util import array2shortstr, arraytuple2str, dflist2str, float2string, largeint2str, resels2str, p2string, plist2string, DisplayParams
from .. util import p2string_none, plist2string_none, float2string_none



class RFTResults(object):
	
	isparametric      = True
	method            = 'rft'
	
	def __init__(self, STAT, z, alpha, dirn, zc, clusters, p_set, p_max):
		self.STAT     = STAT
		self.z        = z
		self.alpha    = alpha
		self.dirn     = dirn
		self.zc       = zc
		self.clusters = clusters
		self.p_set    = p_set
		self.p_max    = p_max
		self.extras   = {}
		
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
		dp.add( 'p_max', p2string_none )
		dp.add( 'p_set', p2string_none )
		dp.add( 'p_cluster', plist2string_none )
		return dp.asstr()

	@property
	def h0reject(self):
		zc       = self.zc
		if zc is None:
			return False
		if self.dirn in (None,1):
			h       = self.z.max() > zc
		elif self.dirn==0:
			h       = (self.z.min() < -zc) or (self.z.max() > zc)
		elif self.dirn==-1:
			h       = self.z.min() < -zc
		return h

	@property
	def p_cluster(self):
		return [c.p  for c in self.clusters]


def _clusterlevel_inference(calc, z, zc, fwhm, dirn=1, circular=False):
	clusters = assemble_clusters(z, zc, dirn=dirn, circular=circular)
	sc       = 2 if (dirn==0) else 1
	for i,c in enumerate( clusters ):
		k,u  = c.extent / fwhm, abs(c.height)
		p    = sc * calc.p.cluster(k, u)
		clusters[i] = c.as_inference_cluster(k, p)
	return clusters


def _pmax(calc, z, dirn):
	if dirn==0:
		z = np.abs(z).max()
		s = 2
	elif dirn==1:
		z = z.max()
		s = 1
	else:
		z = z.min()
		s = 1
	return s * calc.sf(z)


def _setlevel_inference(calc, zc, clusters):
	c = len(clusters)
	if c==0:
		# p = np.nan
		p = None
	else:
		k = min([c.metric for c in clusters])  # min extent_resels
		p = calc.p.set(c, k, zc)
	return p
	


	
def rft(STAT, z, df, fwhm, resels, alpha=0.05, cluster_size=0, circular=False, withBonf=True, dirn=1, equal_var=False):
	
	'''
	COMMENT:  fwhm is needed ONLY for cluster extent (in FWHM units)
	'''
	import rft1d
	_stats = ["T", "F", "T2", "X2"]
	if STAT not in _stats:
		raise ValueError( f'Unknown statistic: {STAT}. Must be one of: {_stats}' )
	

	if STAT=='T':
		a    = 0.5 * alpha if (dirn==0) else alpha
	else:
		if dirn!=1:
			raise ValueError('"dirn=0" and "dirn=-1" can only be used when STAT=="T"')
		a    = alpha
	calc     = rft1d.prob.RFTCalculatorResels(STAT=STAT, df=df, resels=resels, withBonf=withBonf, nNodes=z.size)
	zc       = calc.isf(a)
	clusters = _clusterlevel_inference(calc, z, zc, fwhm, dirn=dirn, circular=circular)
	p_set    = _setlevel_inference(calc, zc, clusters)
	p_max    = _pmax(calc, z, dirn)
	results  = RFTResults( STAT, z, alpha, dirn, zc, clusters, p_set, p_max )
	return results
	







