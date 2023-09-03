

'''
Clusters module
'''

# Copyright (C) 2023  Todd Pataky


# from copy import deepcopy
import numpy as np
# from matplotlib.patches import Polygon
# from matplotlib.collections import PatchCollection
from ... util import tuple2str
from . _base import _Cluster, _WithInference




class Cluster( _Cluster ):
	
	iswrapped       = False
	
	
	def __init__(self, x, z, u, sign=1):
		self._InferenceClass = ClusterWithInference
		self.Q              = None          # domain size (defined during right-boundary interpolation)
		self.x              = list( x )     # post-interpolated
		self.z              = list( z )     # post-interpolated
		self.u              = u             # threshold
		self.sign           = sign
		self._endpoints     = x[0], x[-1]   # pre-interpolation
		
	def __eq__(self, other):
		if type(self)!=type(other):
			return False
		eq = True
		for k,v in self.__dict__.items():
			if not k.startswith('_'):
				v1 = getattr(other, k)
				if v is None:
					eq = v1 is None
				elif isinstance(v, float) and np.isnan(v):
					eq = np.isnan( v1 )
				elif isinstance(v, (int,float,tuple,list,str)):
					eq = v==v1
				else:
					raise ValueError( f'Unable to hash type: {type(v)}' )
				if not eq:
					break
		return eq

	def __lt__(self, other):
		return self.x[0] < other.x[0]


	def _interp_left(self, zf):
		i,u        = self.x[0], self.u
		if (i==0) or np.ma.is_masked( zf[i-1] ): # leftmost domain point OR previous point outside ROI
			self.x = [i] + self.x
			self.z = [u] + self.z
		else:   # first cluster point not domain edge && previous point not outside ROI
			z0,z1  = zf[i-1], zf[i]
			dx     = (z1-u) / (z1-z0)
			self.x = [i-dx] + self.x
			self.z = [u] + self.z
	
	def _interp_right(self, zf):
		i,u,Q      = self.x[-1], self.u, zf.size
		if i==(Q-1) or np.ma.is_masked( zf[i+1] ): # rightmost domain point OR next point outside ROI
			self.x += [i]
			self.z += [u]
		else:  #last cluster point not domain edge && next point not outside ROI
			z0,z1   = zf[i], zf[i+1]
			dx      = (z0-u) / (z0-z1)
			self.x += [i+dx]
			self.z += [u]
		self.Q      = Q

	@property
	def centroid(self):
		x,z = self.asarray().T
		xc  = (x*z).sum() / z.sum()
		zc  = z.mean()
		return xc, zc
	
	@property
	def endpoints(self):
		return self.x[0], self.x[-1]

	@property
	def endpoints_preinterp(self):
		return self._endpoints
	
	@property
	def extent(self):
		x0,x1  = self.endpoints
		w      = x1 - x0
		if w == 0:
			w  = 1
			'''
			LEGACY COMMENTS:
			- when not interpolated, it is possible to have a single-node cluster
			- In this case the extent should be one (and not zero)
			- This case can be removed in future versions IFF all clusters are required to be interpolated
			'''
		return w

	@property
	def height(self):
		return min(self.z) if (self.sign==1) else max(self.z)
	
	@property
	def integral(self):
		x,z = np.asarray(self.x), np.asarray(self.z)
		if x.size==1:
			m = z - self.u
		else:
			m = np.trapz(  z - self.u  )
		return self.sign * m

	@property
	def isLboundary(self):
		return self._endpoints[0] == 0

	@property
	def isRboundary(self):
		return self._endpoints[1] == (self.Q-1)

	@property
	def min(self):
		return min(self.z) if (self.sign==1) else max(self.z)

	@property
	def max(self):
		return max(self.z) if (self.sign==1) else min(self.z)

	@property
	def nnodes(self):
		return len(self.x) - 2  # interpolation adds two points (one to each end)
	
	def asarray(self):
		return np.array( [ self.x, self.z ] ).T
	

	
	def interp(self, zfull):
		# interpolate to threshold u using similar triangles method
		self._interp_left(zfull)
		self._interp_right(zfull)
		
	def plot(self, ax, **kwargs):
		from matplotlib.patches import Polygon
		patch  = Polygon( self.asarray(), **kwargs )
		ax.add_patch( patch )





class ClusterWithInference(_WithInference, Cluster):
	pass



