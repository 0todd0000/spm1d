
'''
Clusters module

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
'''

# Copyright (C) 2016  Todd Pataky
# _spm.py version: 0.3.2.5 (2016/06/27)


from math import floor,ceil
import numpy as np
import rft1d







class Cluster(object):
	def __init__(self, x, z, u, interp=True):
		self._X        = x
		self._Z        = z
		self._u        = u
		self._other    = None       #wrapped cluster
		self._interp   = interp
		self.P         = None       #probability value (based on h and extentR)
		self.csign     = int(np.sign(u))
		self.endpoints = None
		self.extent    = None       #cluster size (absolute)
		self.extentR   = None      #cluster size (resels)
		self.h         = None       #cluster height (minimum above threshold)
		self.iswrapped = False
		self.xy        = None      #cluster centroid
		self._assemble()
		
	def __repr__(self):
		s            = ''
		if self.iswrapped:
			s       += 'Cluster at location: (%.3f, %.3f)\n' %self.xy[0]
		else:
			s       += 'Cluster at location: (%.3f, %.3f)\n' %self.xy
		s           += '   iswrapped       :  %s\n' %self.iswrapped
		if self._interp:
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
		if self.extentR is None:
			s       += '   extent (resels) :  None\n'
		else:
			s       += '   extent (resels) :  %.5f\n' %self.extentR
		s           += '   height (min)    :  %.5f\n' %self.h
		if self.P is None:
			s       += '   P               :  None\n\n'
		else:
			s       += '   P               :  %.5f\n\n' %self.P
		return s

	def _assemble(self):
		x0,x1               = self._X[0], self._X[-1]
		z                   = self._Z
		if not self._interp:
			x0,x1           = int(ceil(x0)), int(floor(x1))
			z               = z[1:-1]
		self.endpoints      = x0, x1
		self.extent         = x1 - x0
		if self.extent==0:  #to reproduce results from previous versions, minimum extent must be one (when not interpolated)
			self.extent     = 1
		self.h              = (self.csign*z).min()
		x,z                 = self._X, self._Z
		self.xy             = (x*z).sum() / z.sum(),  z.mean()

	def get_patch_vertices(self):
		x,z,u   = self._X.tolist(), self._Z.tolist(), self._u
		if z[0]!=u:
			x  = [x[0]] + x
			z  = [u] + z
		if z[-1]!=u:
			x += [x[-1]]
			z += [u]
		return x,z

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
		self.iswrapped  = True
		self.extent     = self.extent + other.extent
		self.endpoints  = [other.endpoints, self.endpoints]
		self.h          = min(self.h, other.h)
		self.xy         = [other.xy, self.xy]
		self._other     = other








class ClusterNonparam(Cluster):
	def __init__(self, cluster, metric, iterations, nPermUnique):
		self._X        = cluster._X
		self._Z        = cluster._Z
		self._u        = cluster._u
		self._other    = cluster._other       #wrapped cluster
		self._interp   = cluster._interp
		self.P         = None       #probability value (based on h and extentR)
		self.csign     = cluster.csign
		self.endpoints = cluster.endpoints
		self.extent    = cluster.extent
		self.iswrapped = cluster.iswrapped
		self.xy        = cluster.xy       #cluster centroid
		### non-parametric attributes:
		self.metric        = metric
		self.iterations    = iterations
		self.nPerm         = iterations if iterations > 0 else nPermUnique
		self.nPermUnique   = nPermUnique
		self.metric_value  = None
		self.metric_label  = None
		self._calculate_metric_value()
		

	def __repr__(self):
		s        = ''
		
		if self.iswrapped:
			s       += 'Cluster(NP) at location: (%.3f, %.3f)\n' %self.xy[0]
		else:
			s       += 'Cluster(NP) at location: (%.3f, %.3f)\n' %self.xy
		s           += '   iswrapped       :  %s\n' %self.iswrapped
		if self._interp:
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
		s           += '   metric          :  %s\n'   %self.metric_label
		s           += '   metric_value    :  %.5f\n' %self.metric_value
		if self.P is None:
			s       += '   P               :  None\n\n'
		else:
			s       += 'Inference:\n'
			s       += '   nPermUnique     :  %d unique permutations possible\n' %self.nPermUnique
			s       += '   nPermActual     :  %d actual permutations\n' %self.nPerm
			s       += '   P               :  %.5f\n\n' %self.P
		return s



	def _calculate_metric_value(self):
		self.metric_value    = self.metric.get_single_cluster_metric_xz(self._X, self._Z, self._u)
		self.metric_label    = self.metric.get_label_single()


	def inference(self, pdf):
		self.P      = (pdf > self.metric_value).mean()
		self.P      = max( self.P,  1.0/self.nPermUnique )





