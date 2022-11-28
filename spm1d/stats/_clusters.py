
'''
Clusters module

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
'''

# Copyright (C) 2020  Todd Pataky



from math import floor,ceil
import numpy as np
from .. import rft1d



class _Cluster(object):
	def __init__(self, x, z, u, interp=True):
		self.name           = 'Cluster'
		self._X             = x
		self._Z             = z
		self._other         = None       #wrapped cluster
		self.P              = None       #probability value (based on h and extentR)
		self.centroid       = None
		self.csign          = int(np.sign(u))
		self.endpoints      = None
		self.extent         = None       #cluster size (absolute)
		self.isinterpolated = interp     #interpolated to threshold?
		self.isparam        = True       #parametric (derived from parametric inference)
		self.iswrapped      = False
		self.threshold      = u
		self.xy             = None       #redundant attribute (centroid)
		


	def __repr__(self):
		s            = '%s\n' %self.name
		s           += '   threshold       :  %.3f\n' %self.threshold
		if self.iswrapped:
			s       += '   centroid        :  (%.3f, %.3f)\n' %self.centroid[0]
		else:
			s       += '   centroid        :  (%.3f, %.3f)\n' %self.centroid
		s           += '   isinterpolated  :  %s\n' %self.isinterpolated
		s           += '   iswrapped       :  %s\n' %self.iswrapped
		if self.isinterpolated:
			if self.iswrapped:
				(x0,x1),(x2,x3) = self.endpoints[0], self.endpoints[1]
				s   += '   endpoints       :  [(%.3f, %.3f), (%.3f, %.3f)]\n' %(x0,x1,x2,x3)
			else:
				s   += '   endpoints       :  (%.3f, %.3f)\n' %self.endpoints
			s       += '   extent          :  %.3f\n' %self.extent
				
		else:
			if self.iswrapped:
				(x0,x1),(x2,x3) = self.endpoints[0], self.endpoints[1]
				s   += '   endpoints       :  [(%d, %d), (%d, %d)]\n' %(x0,x1,x2,x3)
			else:
				s   += '   endpoints       :  (%d, %d)\n' %self.endpoints
			s       += '   extent          :  %d\n' %self.extent
		if self.isparam:
			if self.extentR is None:
				s   += '   extent (resels) :  None\n'
			else:
				s   += '   extent (resels) :  %.5f\n' %self.extentR
			s       += '   height (min)    :  %.5f\n' %self.h
		else:
			s       += '   metric          :  %s\n'   %self.metric_label
			s       += '   metric_value    :  %.5f\n' %self.metric_value
		if self.P is None:
			s       += '   P               :  None\n\n'
		else:
			if not self.isparam:
				s   += '   nPermUnique     :  %s unique permutations possible\n' %self.get_nPermUnique_asstr()
				s   += '   nPermActual     :  %d actual permutations\n' %self.nPerm
			s       += '   P               :  %.5f\n\n' %self.P
		return s
		


	def _assemble(self):
		x0,x1               = self._X[0], self._X[-1]
		z                   = self._Z
		if not self.isinterpolated:
			x0,x1           = int(ceil(x0)), int(floor(x1))
			z               = z[1:-1]
		self.endpoints      = x0, x1
		self.extent         = x1 - x0
		if self.extent==0:  #to reproduce results from previous versions, minimum extent must be one (when not interpolated)
			self.extent     = 1
		self.h              = (self.csign*z).min()
		x,z                 = self._X, self._Z
		self.xy             = (x*z).sum() / z.sum(),  z.mean()
		self.centroid       = self.xy

	def get_patch_vertices(self):
		x,z,u   = self._X.tolist(), self._Z.tolist(), self.threshold
		if z[0]!=u:
			x  = [x[0]] + x
			z  = [u] + z
		if z[-1]!=u:
			x += [x[-1]]
			z += [u]
		return x,z

	def inference(self):
		pass
		
	def merge(self, other):
		self.iswrapped  = True
		self.extent     = self.extent + other.extent
		self.endpoints  = [other.endpoints, self.endpoints]
		self.xy         = [other.xy, self.xy]
		self.centroid   = self.xy
		self._other     = other





class Cluster(_Cluster):
	'''
	Suprathreshold cluster (or "upcrossing"):  parametric inference
	'''
	def __init__(self, x, z, u, interp=True):
		super(Cluster, self).__init__(x, z, u, interp=interp)
		self.name      = 'Cluster'  #class label
		self.extentR   = None       #cluster size (resels)
		self.h         = None       #cluster height (minimum above threshold)
		self._assemble()
		
	def inference(self, STAT, df, fwhm, resels, two_tailed, withBonf, nNodes):
		self.extentR        = float(self.extent) / fwhm
		k,u                 = self.extentR, self.h
		if STAT == 'T':
			p = rft1d.t.p_cluster_resels(k, u, df[1], resels, withBonf=withBonf, nNodes=nNodes)
			p = min(1, 2*p) if two_tailed else p
		elif STAT == 'F':
			p = rft1d.f.p_cluster_resels(k, u, df, resels, withBonf=withBonf, nNodes=nNodes)
		elif STAT == 'T2':
			p = rft1d.T2.p_cluster_resels(k, u, df, resels, withBonf=withBonf, nNodes=nNodes)
		elif STAT == 'X2':
			p = rft1d.chi2.p_cluster_resels(k, u, df[1], resels, withBonf=withBonf, nNodes=nNodes)
		self.P    = p

	def merge(self, other):
		super(Cluster, self).merge(other)
		self.h          = min(self.h, other.h)








class ClusterNonparam(Cluster):
	'''
	Suprathreshold cluster (or "upcrossing"):  non-parametric inference
	'''
	def __init__(self, x, z, u, interp=True):
		super(Cluster, self).__init__(x, z, u, interp=interp)
		self.name          = 'Cluster (NonParam)'
		self.isparam       = False
		self.metric        = None
		self.iterations    = None
		self.nPerm         = None
		self.nPermUnique   = None
		self.metric_value  = None
		self.metric_label  = None
		self._assemble()
		
	def get_nPermUnique_asstr(self):
		n = self.nPermUnique
		return n if (n < 1e6) else '%.4g' %n
	
	def set_metric(self, metric, iterations, nPermUnique, two_tailed):
		self.metric        = metric
		self.iterations    = iterations
		self.nPerm         = iterations if iterations > 0 else nPermUnique
		self.nPermUnique   = nPermUnique
		self.metric_label  = metric.get_label_single()
		### compute metric value:
		x                  = metric.get_single_cluster_metric_xz(self._X, self._Z, self.threshold, two_tailed)
		if self.iswrapped:
			x             += metric.get_single_cluster_metric_xz(self._other._X, self._other._Z, self.threshold, two_tailed)
		self.metric_value  = x

	def inference(self, pdf, two_tailed):
		pdf      = np.asarray(pdf, dtype=float)  # fix for ragged nested sequences
		self.P   = (pdf >= self.metric_value).mean()
		# self.P             = max( self.P,  1.0/self.nPermUnique )





