
import numpy as np
from scipy.stats import percentileofscore
from rft1d.geom import bwlabel
import spm1d


# def list2str(x):
# 	fmt   = '(' + ('%d, '*len(x))[:-2] + ')'
# 	return fmt %tuple(x)






	# def compute_centroid(self, z, b, zstar):
	# 	x     = np.arange(z.size)[b]
	# 	zz    = z[b]
	# 	z0    = np.sign(zz[0]) * zstar * np.ones(zz.size)
	# 	zz    = np.hstack([zz,z0])
	# 	xm,zm = x.mean(), zz.mean()
	# 	if self.isnegative:
	# 		zm *= -1
	# 	return xm, zm
	# def compute_geom(self, z, b, zstar):
	# 	self.extent  = int( b.sum() )
	# 	self.nodes   = np.argwhere(b).flatten()
	# 	self.xy      = self.compute_centroid(z, b, zstar)
	# def compute_pvalue(self, Z):
	# 	self.P     = 1 - 0.01*percentileofscore(Z, self.m)
	#
	#
	# def get_patch_vertices(self):
	# 	x,z,u   = self._X.tolist(), self._Z.tolist(), self._u
	# 	if z[0]!=u:
	# 		x  = [x[0]] + x
	# 		z  = [u] + z
	# 	if z[-1]!=u:
	# 		x += [x[-1]]
	# 		z += [u]
	# 	return x,z
	#
	# # def compute_p_value(self, Z):
	# # 	i     = L==1
	# # 	if np.sign( spm.z[i].mean() ) > 0:
	# # 		m = self.metric.get_single_cluster_metric(spm.z, zstar, i)
	# # 	else:
	# # 		m = self.metric.get_single_cluster_metric(-spm.z, zstar, i)
	# # 	p     = 1 - 0.01*stats.percentileofscore(spm.permuter.Z1, m)
	# # 	if iterations==-1:
	# # 		p = max(p, 1.0/maxIterations)
	# # 	else:
	# # 		p = max(p, 1.0/iterations)
	# # 	self.P            = p
	# # 	self.metric_value = m
	
	

# class Cluster(object):
# 	def __init__(self, z, zstar, Z, b, m, metric_label, isnegative=False):
# 		self._X           = np.arange(z.size)
# 		self._Z           = z
# 		self._u           = zstar
# 		self.iswrapped    = False
# 		self.P            = None          #probability value (based on metric_value)
# 		self.B            = b             #binary field specifying cluster location
# 		self.isnegative   = isnegative    #True if the cluster lies beyond the lower threshold in two-tailed inference
# 		self.extent       = None          #cluster size (continuum nodes)
# 		self.nodes        = None          #continuum node indices
# 		self.metric_label = metric_label  #metric label
# 		self.m            = m             #metric value (upon which inference is based)
# 		self.xy           = None          #cluster centroid
# 		self.compute_geom(z, b, zstar)
# 		self.compute_pvalue(Z)
#
# 	def __repr__(self):
# 		s        = ''
# 		s       += 'Cluster at location: (%.3f, %.3f)\n' %self.xy
# 		s       += '   extent          :  %d\n'   %self.extent
# 		s       += '   nodes           :  %s\n'   %list2str(self.nodes)
# 		s       += '   metric          :  %s\n'   %self.metric_label
# 		s       += '   metric_value    :  %.5f\n' %self.m
# 		if self.P==None:
# 			s   += '   P               :  None\n\n'
# 		else:
# 			s   += '   P               :  %.5f\n\n' %self.P
# 		return s
# 	def compute_centroid(self, z, b, zstar):
# 		x     = np.arange(z.size)[b]
# 		zz    = z[b]
# 		z0    = np.sign(zz[0]) * zstar * np.ones(zz.size)
# 		zz    = np.hstack([zz,z0])
# 		xm,zm = x.mean(), zz.mean()
# 		if self.isnegative:
# 			zm *= -1
# 		return xm, zm
# 	def compute_geom(self, z, b, zstar):
# 		self.extent  = int( b.sum() )
# 		self.nodes   = np.argwhere(b).flatten()
# 		self.xy      = self.compute_centroid(z, b, zstar)
# 	def compute_pvalue(self, Z):
# 		self.P     = 1 - 0.01*percentileofscore(Z, self.m)
#
#
# 	def get_patch_vertices(self):
# 		x,z,u   = self._X.tolist(), self._Z.tolist(), self._u
# 		if z[0]!=u:
# 			x  = [x[0]] + x
# 			z  = [u] + z
# 		if z[-1]!=u:
# 			x += [x[-1]]
# 			z += [u]
# 		return x,z
#
# 	# def compute_p_value(self, Z):
# 	# 	i     = L==1
# 	# 	if np.sign( spm.z[i].mean() ) > 0:
# 	# 		m = self.metric.get_single_cluster_metric(spm.z, zstar, i)
# 	# 	else:
# 	# 		m = self.metric.get_single_cluster_metric(-spm.z, zstar, i)
# 	# 	p     = 1 - 0.01*stats.percentileofscore(spm.permuter.Z1, m)
# 	# 	if iterations==-1:
# 	# 		p = max(p, 1.0/maxIterations)
# 	# 	else:
# 	# 		p = max(p, 1.0/iterations)
# 	# 	self.P            = p
# 	# 	self.metric_value = m




class _Metric(object):
	def get_label(self):
		return self.__class__.__name__
	def get_label_single(self):
		return self.__class__.__name__.strip('Max')
	def get_all_clusters(self, z, zstar, Z, two_tailed=False):
		clusters      = []
		mlabel        = self.get_label_single()
		L,n           = bwlabel( z > zstar )
		for i in range(n):
			m         = self.get_single_cluster_metric(z, zstar, L==i+1)
			# cluster   = Cluster(z, zstar, Z, L==i+1, m, mlabel)
			cluster   = ClusterNP(np.arange(z.size), z, zstar, interp=True, mvalue=m, mlabel=mlabel)
			
			clusters.append( cluster )
		# if two_tailed:
		# 	L,n       = bwlabel( -z > zstar )
		# 	for i in range(n):
		# 		m         = self.get_single_cluster_metric(-z, zstar, L==i+1)
		# 		cluster   = Cluster(-z, zstar, Z, L==i+1, m, mlabel, isnegative=True)
		# 		clusters.append( cluster )
			
		return clusters
		# if two_tailed:
		# 	L,n       = bwlabel( -z > zstar )


	def get_all_cluster_metrics(self, z, thresh=3.0, circular=False):
		L,n     = bwlabel(z>thresh)
		x       = [0]
		if n > 0:
			x   = [self.get_single_cluster_metric(z, thresh, L==i+1)   for i in range(n)]
			if circular and (n > 1):  #merge clusters for circular fields:
				if (L==1)[0] and (L==n)[-1]:
					x[0] += x[-1]
					x     = x[:-1]
		return x
	def get_max_metric(self, z, thresh=3.0, circular=False):
		return max(  self.get_all_cluster_metrics(z, thresh, circular)  )



class MaxClusterExtent(_Metric):
	def get_single_cluster_metric(self, z, thresh, i):
		return i.sum()
	def get_single_cluster_metric_xz(self, x, z, zstar, two_tailed=False):
		return x.max() - x.min()


class MaxClusterHeight(_Metric):
	def get_single_cluster_metric(self, z, thresh, i):
		return z[i].max()
	def get_single_cluster_metric_xz(self, x, z, zstar, two_tailed=False):
		return z.max()


class MaxClusterIntegral(_Metric):
	def get_single_cluster_metric(self, z, thresh, i):
		if i.sum()==1:
			x = z[i] - thresh
		else:
			x = np.trapz(  z[i]-thresh  )
		return x

	def get_single_cluster_metric_xz(self, x, z, zstar, two_tailed=False):
		if x.size==1:
			m = float(z - zstar)
		else:
			m = np.trapz(  z - zstar  )
		if two_tailed and (m < 0):
			m *= -1
		return m





metric_dict  = {
	'MaxClusterExtent'   : MaxClusterExtent(),
	'MaxClusterHeight'   : MaxClusterHeight(),
	'MaxClusterIntegral' : MaxClusterIntegral()
	}





def _cluster_geom(self, u, interp, circular, csign=+1):
	Q,Z      = self.Q, self.z
	X        = np.arange(Q)
	if np.ma.is_masked(Z):
		i    = Z.mask
		Z    = np.array(Z)
		B    = (csign*Z) >= u
		B[i] = False
		Z[i] = np.nan
	else:
		B    = (csign*Z) >= u
	Z        = csign*Z
	L,n      = rft1d.geom.bwlabel(B)
	clusters = []
	for i in range(n):
		b    = L==(i+1)
		x,z  = X[b].tolist(), Z[b].tolist()
		# interpolate to threshold u using similar triangles method
		# (interpolate for plotting whether or not "interp" is true)
		if (x[0]>0) and not np.isnan( Z[x[0]-1] ):  #first cluster point not continuum edge && previous point not outside ROI
			z0,z1  = Z[x[0]-1], Z[x[0]]
			dx     = (z1-u) / (z1-z0)
			x      = [x[0]-dx] + x
			z      = [u] +z
		if (x[-1]<Q-1) and not np.isnan( Z[x[-1]+1] ):  #last cluster point not continuum edge && next point not outside ROI
			z0,z1  = Z[x[-1]], Z[x[-1]+1]
			dx     = (z0-u) / (z0-z1)
			x     += [x[-1]+dx]
			z     += [u]
		# create cluster:
		x,z  = np.array(x), csign*np.array(z)
		clusters.append(  Cluster(x, z, csign*u, interp) )
	#merge clusters if necessary (circular fields only)
	if circular and (clusters!=[]):
		xy         = np.array([c.endpoints  for c in clusters])
		i0,i1      = xy[:,0]==0, xy[:,1]==Q-1
		ind0,ind1  = np.argwhere(i0), np.argwhere(i1)
		if (len(ind0)>0) and (len(ind1)>0):
			ind0,ind1 = ind0[0][0], ind1[0][0]
			if (ind0!=ind1) and (clusters[ind0].csign == clusters[ind1].csign):
				clusters[ind0].merge( clusters[ind1] )
				clusters.pop( ind1 )
	return clusters
	
	
def _get_clusters(zstar, check_neg, interp, circular):
	clusters      = _cluster_geom(zstar, interp, circular, csign=+1)
	# if check_neg:
	# 	clustersn = self._cluster_geom(zstar, interp, circular, csign=-1)
	# 	clusters += clustersn
	# 	if len(clusters) > 1:
	# 		### reorder clusters left-to-right:
	# 		x         = [c.xy[0]  for c in clusters]
	# 		ind       = np.argsort(x).flatten()
	# 		clusters  = np.array(clusters)[ind].tolist()
	return clusters
	# def get_all_cluster_metrics(self, z, thresh=3.0):
	# 	L,n     = bwlabel(z>thresh)
	# 	if n>0:
	# 		x   = []
	# 		for i in range(n):
	# 			if (L==i+1).sum()==1:
	# 				x.append(z[L==i+1]-thresh)
	# 			else:
	# 				x.append(  np.trapz(z[L==i+1]-thresh)  )
	# 	else:
	# 		x   = [0]
	# 	return x
		



