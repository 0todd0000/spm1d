

from . permuters import get_permuter
from ... geom import assemble_clusters, ClusterList



class PermResults1D(object):
	
	isparametric      = False
	method            = 'perm'
	
	def __init__(self, alpha, dirn, zc, clusters, p_max, p_set, permuter, nperm):
		self.method   = 'perm'
		self.alpha    = alpha
		self.dirn     = dirn
		self.zc       = zc
		self.p_max    = p_max
		self.p_set    = p_set
		self.clusters = clusters
		self.extras   = dict(permuter=permuter, nperm_possible=permuter.nPermTotal, nperm_actual=nperm)

	def __repr__(self):
		s  = 'PermResults1D\n'
		s += '   zc    = %.5f\n' %self.zc
		s += '   p_max = %.5f\n' %self.p_max
		s += '   p_set = %s\n'   %('None' if (self.p_set is None) else '%.5f'%self.p_set)
		s += '   nperm = %d\n'   %self.nperm
		return s




def inference1d(stat, z, alpha=0.05, dirn=0, testname=None, args=None, nperm=10000, circular=False, cluster_metric='MaxClusterExtent'):
	from . probcalc1d import ProbCalc1DSingleStat
	permuter  = get_permuter(testname, 1)( *args )
	if alpha < 1/permuter.nPermTotal:
		raise( ValueError(f'alpha ({alpha:0.5f}) must be greater than or equal to 1/nPermTotal = {1/permuter.nPermTotal:0.5f}') )
	# build primary PDF:
	permuter.build_pdf(  nperm  )
	probcalc = ProbCalc1DSingleStat(stat, permuter, z, alpha, dirn)
	zc       = probcalc.get_z_critical()
	
	if probcalc.h0rejected:
		# build secondary PDF:
		permuter.set_metric( cluster_metric )
		permuter.build_secondary_pdf( zc, circular )
		# cluster-level inference:
		clusters = assemble_clusters(z, zc, dirn=dirn, circular=circular)
		clusters = probcalc.cluster_inference( clusters )
		# set-level inference:
		p_set    = probcalc.setlevel_inference( clusters )
	else:
		clusters = ClusterList( [] )
		p_set    = None


	# maximum inference:
	p_max    = probcalc.get_p_max()
	
	
	results  = PermResults1D(alpha, dirn, zc, clusters, p_max, p_set, permuter, nperm)
	return results





def inference1d_multi(stat, z, alpha=0.05, dirn=0, testname=None, args=None, nperm=10000, circular=False, cluster_metric='MaxClusterExtent'):
	from . probcalc1d import ProbCalc1DMultiStat
	permuter  = get_permuter(testname, 1)( *args )
	# build primary PDF:
	permuter.build_pdf(  nperm  )
	probcalc = ProbCalc1DMultiStat(stat, permuter, z, alpha, dirn)
	zc       = probcalc.get_z_critical()

	dirn     = None

	if probcalc.anyh0rejected:
		permuter.set_metric( cluster_metric )
		permuter.build_secondary_pdfs( zc, circular )

	results = []
	for i,(zz,zzc,Z2,C2) in enumerate( zip(z , zc, permuter.Z2, permuter.C2) ):
		if zz.max() > zzc:
			# cluster-level inference:
			clusters = assemble_clusters(zz, zzc, dirn=1, circular=circular)
			clusters = probcalc.cluster_inference( Z2, clusters )
			# set-level inference:
			p_set    = None
			p_set    = probcalc.setlevel_inference( Z2, C2, clusters )
		else:
			clusters = ClusterList( [] )
			p_set    = None
		
		p_max    = probcalc.get_p_max( i )
		res      = PermResults1D(alpha, dirn, zzc, clusters, p_max, p_set, permuter, nperm)
		results.append( res )


	return results

