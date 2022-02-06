'''
Geometry module

This module contains functions for computing various geomtric characteristics
of 1D fields and upcrossings.
'''

# Copyright (C) 2022  Todd Pataky


from math import log
import numpy as np


# eps         = np.finfo(np.float).eps
eps         = np.finfo(float).eps



class Upcrossing(object):
	'''
	A class for computing upcrossing extents.
	Computing upcrossing extents is simple if the upcrossing extent is to be
	calculated using only the number of suprathreshold nodes (i.e. an integer).
	However, extent computation can be complicated by three factors:
	* interpolation
	* boundary touching
	* wrapping
	Interpolating to a specified height is straightforward, if the
	upcrossing does not touch the boundary.
	Boundary touching and wrapping are easy to deal with, if there is no
	interpolation.
	However, a number of cases needed to be programmed when interpolating and
	also allowing for both boundary touches and wrapping.
	This class accounts for all possibilities via the keywords *interp* and
	*wrap*.
	'''
	def __init__(self, y, b, interp=True, wrap=True):
		self.y             = y
		self.b             = b
		self.ind           = np.argwhere(b).flatten()
		self.touch_start   = b[0]
		self.touch_end     = b[-1]
		self.touch_both    = b[0] and b[-1]
		self.touch_neither = not (b[0] or b[-1])
		self.interp        = interp
		self.wrap          = wrap
	
	def _interp(self, y, i0, h):
		i1    = i0+1
		y0,y1 = y[i0], y[i1]
		x0    = float(i0)
		m     = y1-y0
		x     = (h-y0)/m + x0
		return x

	def endpoints(self, yi, h):
		if yi.size==1:    #no interp
			x0,x1  = 0,0
		elif yi.size==2:  #interp, or no wrapping
			if yi[0]>yi[1]:
				x0  = 0
				if self.interp:
					x1  = self._interp(yi, 0, h)
				else:
					x1  = 1
			else:
				x1  = 1
				if self.interp:
					x0  = self._interp(yi, 0, h)
				else:
					x0 = 0
		else:
			if yi[0] > h:  #no interpolation or no wrap
				x0  = 0
			else:
				x0  = self._interp(yi, 0, h)
			if yi[-1] > h:
				x1  = yi.size-1
			else:
				x1  = self._interp(yi, yi.size-2, h)
		return x0,x1

	def isolate(self):
		if self.interp:
			if self.touch_neither:
				i0      = self.ind[0]-1
				i1      = self.ind[-1]+2
				yi      = self.y[i0:i1]
			elif self.touch_both:
				if np.all(self.b):
					yi  = self.y
				else:  #wrapped
					L,n     = bwlabel(self.b)
					b0,b1   = L==1, L==2
					i0end   = np.argwhere(b0).flatten()[-1]
					i1start = np.argwhere(b1).flatten()[0]
					y0      = self.y[:i0end+2]
					y1      = self.y[i1start-1:]
					yi      = np.hstack([y1,y0])
			elif self.touch_start:
				if self.wrap:
					i1      = self.ind[-1]+2
					yi0     = self.y[-1]
					yi1     = self.y[:i1]
					yi      = np.hstack([yi0,yi1])
				else:
					i1      = self.ind[-1]+2
					yi      = self.y[:i1]
			elif self.touch_end:
				if self.wrap:
					i0      = self.ind[0]-1
					yi0     = self.y[i0:]
					yi1     = self.y[0]
					yi      = np.hstack([yi0,yi1])
				else:
					i0      = self.ind[0]-1
					yi      = self.y[i0:]

		else:  #no interpolation
			if self.touch_neither:
				i0      = self.ind[0]
				i1      = self.ind[-1]+1
				yi      = self.y[i0:i1]
			elif self.touch_both:
				if np.all(self.b):
					yi  = self.y
				else:  #wrapped
					L,n     = bwlabel(self.b)
					b0,b1   = L==1, L==2
					i0end   = np.argwhere(b0).flatten()[-1]
					i1start = np.argwhere(b1).flatten()[0]
					y0      = self.y[:i0end+1]
					y1      = self.y[i1start:]
					yi      = np.hstack([y1,y0])
			elif self.touch_start:
				i1      = self.ind[-1]+1
				yi      = self.y[:i1]
			elif self.touch_end:
				i0      = self.ind[0]
				yi      = self.y[i0:]
		return yi

	def extent(self, h, endpoints=False):
		if np.all(self.b):
			m      = self.y.size - 1
		elif self.interp:
			yi     = self.isolate()	
			x0,x1  = self.endpoints(yi, h)
			m      = x1 - x0
		else:
			m      = self.b.sum() - 1
		return m
	
	def extent_nodes(self, h):
		return self.extent(h) + 1




class ClusterMetricCalculator(object):
	'''
	A class for computing various geometric characteristics of the excursion set
	including number of upcrossings, upcrossing (cluster) extents, etc.
	
	:Parameters:

		*None*
		
	:Returns:

		*calc* --- a ClusterMetricCalculator instance
	
	:Example:
	
		>>> y = rft1d.random.randn1d(1, 101, 15.0)
		>>> calc = rft1d.geom.ClusterMetricCalculator()
		>>> k = calc.cluster_extents(y, 0.5) #cluster extents when thresholded at 0.5
	
	'''
	def __repr__(self):
		s    = ''
		s   += 'RFT1D ClusterMetricCalculator:\n'
		s   += '   (no attributes)\n'
		return s

	def cluster_extents(self, y, u, interp=True, wrap=False):
		'''
		Upcrossing extents (units: nodes).
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*interp* --- interpolate to threshold *u*
			
			*wrap* --- wrap upcrossings from the end to the start of the field

		:Returns:

			*k* --- list of upcrossing extents, or [0] if no upcrossings
	
		:Example:
	
			>>> k = calc.cluster_extents(y, 0.0) #cluster extents when thresholded at 0.0
			
		.. danger:: Setting *interp* to False is faster, but it will cause disagreements between node-based and element-based sampling. If the upcrossing is large this difference is negligible, but for small upcrossing there may be strange results (e.g. upcrossing with an extent of zero). Recommendation: **always interpolate**.
		'''
		# L,n = bwlabel(y >= u, merge_wrapped=wrap)
		L,n = bwlabel(np.array(y >= u), merge_wrapped=wrap)
		if n==0:
			m = [0]
		else:
			m   = []
			for i in range(n):
				b       = L==(i+1)
				if np.all(b):
					mm  = y.size - 1
				elif interp:
					up  = Upcrossing(y, b, interp, wrap)
					mm  = up.extent(u)
				else:
					mm  = b.sum() - 1
				m.append(mm)
		return m
	

	def cluster_extents_locations(self, y, u, interp=True, wrap=False):
		'''
		Compute both:
		-- Upcrossing extents (units: nodes)
		-- Upcrossing locations (units: continuum position units)
		
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*interp* --- interpolate to threshold *u*
			
			*wrap* --- wrap upcrossings from the end to the start of the field

		:Returns:

			*k* --- list of upcrossing extents, or [np.nan] if no upcrossings
			*q* --- list of upcrossing locations, or [np.nan] if no upcrossings

		:Example:
	
			>>> k,q = calc.cluster_extents_locations_lo(y, 0.0) #cluster extents and locations when thresholded at 0.0
			
		.. danger:: Setting *interp* to False is faster, but it will cause disagreements between node-based and element-based sampling. If the upcrossing is large this difference is negligible, but for small upcrossing there may be strange results (e.g. upcrossing with an extent of zero). Recommendation: **always interpolate**.
		'''
		# L,n = bwlabel(y >= u, merge_wrapped=wrap)
		L,n = bwlabel(np.array(y >= u), merge_wrapped=wrap)
		if n==0:
			x = [np.nan]
			m = [np.nan]
		else:
			m,x           = [],[]
			for i in range(n):
				b         = L==(i+1)
				if np.all(b):
					mm    = y.size - 1
					xx    = 0.5 * y.size
				elif interp:
					up    = Upcrossing(y, b, interp, wrap)
					yi    = up.isolate()	
					x0,x1 = up.endpoints(yi, u)
					mm    = x1 - x0
					xx    = 0.5 * (x0 + x1)
					xx   += np.argwhere(b)[0,0]
					
				else:
					mm    = b.sum() - 1
					xx    = np.argwhere(b).mean()
				m.append(mm)
				x.append(xx)
		return m,x


	def cluster_minima(self, y, u, interp=True):
		'''
		Minimum field height inside each upcrossing.
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*interp* --- interpolate to threshold *u*

		:Returns:

			*zmin* --- list of upcrossing minima; [0] if no upcrossings
	
		:Example:
	
			>>> k = calc.cluster_minima(y, 0.0)
			
		.. warning :: If *interp* is *True*, the minima are all *u*.
		
		.. danger:: If *u* is zero and *interp* is *True* the user may be unable to distinguish between two cases: (i) no upcrossings and (ii) one upcrossing with a minimum of zero. Most thresholds we're interested in are much higher than zero, so this buggy behavior is not deemed serious. To check the number of upcrossings use the **nMaxima** method.
		
		'''
		b   = np.array(y > u)
		if np.all(b):
			m = [y.min()]
		elif np.any(b):
			L,n        = bwlabel(b)
			if interp:
				m      = [u]*n
			else:
				m      = [y[L==(i+1)].min()  for i in range(n)]
		else:
			m = [0]
		return m
	
	def max_cluster_extent(self, y, u, interp=True, wrap=False):
		'''
		Maximum upcrossing extent
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*interp* --- interpolate to threshold *u*
			
			*wrap* --- wrap upcrossings from the end to the start of the field

		:Returns:

			*kmax* --- maximum upcrossing extent (unit: nodes)
	
		:Example:
	
			>>> k = calc.max_cluster_extent(y, 0.2)
			
		.. danger:: Setting *interp* to False is faster, but it will cause disagreements between node-based and element-based sampling. If the upcrossing is large this difference is negligible, but for small upcrossing there may be strange results (e.g. upcrossing with an extent of zero). Recommendation: **always interpolate**.
		'''
		return max(  self.cluster_extents(y, u, interp, wrap)  )
	
	def mean_cluster_extent(self, y, u, interp=True, wrap=False):
		'''
		Mean upcrossing extent
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*interp* --- interpolate to threshold *u*
			
			*wrap* --- wrap upcrossings from the end to the start of the field

		:Returns:

			*kmean* --- mean upcrossing extent (unit: nodes)
	
		:Example:
	
			>>> k = calc.mean_cluster_extent(y, 0.5)
		
		.. danger:: Setting *interp* to False is faster, but it will cause disagreements between node-based and element-based sampling. If the upcrossing is large this difference is negligible, but for small upcrossing there may be strange results (e.g. upcrossing with an extent of zero). Recommendation: **always interpolate**.
		'''
		return np.mean(  self.cluster_extents(y, u, interp, wrap)  )
		
	def nMaxima(self, y, u):
		'''
		Number of maxima. Equivalent to **nUpcrossings**.
		'''
		return self.nUpcrossings(y, u)
	

	def nSuprathresholdNodes(self, y, u):
		'''
		Number of nodes in the excursion set.
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
		:Returns:

			*nNodes* --- number of nodes which survive the threshold *u*
	
		:Example:
	
			>>> nNodes = calc.nSuprathresholdNodes(y, 0.5)
		
		.. warning:: This returns simply the number of nodes, which is not equivelent to extent. To compute the total extent you must subtract the number of upcrossings from this value. Otherwise use **rft1d.geom.nSuprathresholdResels** or **rft1d.geom.total_excursion_set_extent**.
		
		'''
		return (y > u).sum()

	def nSuprathresholdResels(self, y, u, fwhm=1.0, interp=True):
		'''
		Number of resels in the excursion set.
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*fwhm* --- actual or estimated FWHM
			
			*interp* --- interpolate to threshold *u*
			
		:Returns:

			*nResels* --- number of resels which survive the threshold *u*
	
		:Example:
	
			>>> nResels = calc.nSuprathresholdResels(y, 0.5)
			
		.. warning:: This is a length measure, so is similar to (**nSuprathresholdNodes** minus **nUpcrossings**) divided by the FWHM, with the exception that extents can be interpolated to *u*.
		
		.. danger:: Setting *interp* to False is faster, but it will cause disagreements between node-based and element-based sampling. If the upcrossing is large this difference is negligible, but for small upcrossing there may be strange results (e.g. upcrossing with an extent of zero). Recommendation: **always interpolate**.
		'''
		return self.total_excursion_set_extent(y, u, interp=interp) / float(fwhm)
		
	
	def nUpcrossings(self, y, u):
		'''
		Number of upcrossings.
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
		:Returns:

			*c* --- number of upcrossings
	
		:Example:
	
			>>> c = calc.nUpcrossings(y, 0.5)
		
		'''
		b   = np.array(y > u)
		if np.any(b):
			L,n        = bwlabel(b)
		else:
			n = 0
		return n
	
	def nUpcrossingsByExtent(self, y, u, k, interp=True, wrap=False):
		'''
		Number of upcrossings at threshold extent *k*.
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*k* --- cluster extent threshold (unit: nodes)
			
			*interp* --- interpolate to threshold *u*
			
			*wrap* --- wrap upcrossings from the end to the start of the field

		:Returns:

			*c* --- number of upcrossings whose extents equal or exceed *k*
	
		:Example:
	
			>>> c = calc.nUpcrossingsByExtent(y, 3.5, 5.0)
			
		.. danger:: Setting *interp* to False is faster, but it will cause disagreements between node-based and element-based sampling. If the upcrossing is large this difference is negligible, but for small upcrossing there may be strange results (e.g. upcrossing with an extent of zero). Recommendation: **always interpolate**.
		'''
		kk  = self.cluster_extents(y, u, interp, wrap)
		return (np.array(kk) >= k).sum()
	
	
	
	def total_excursion_set_extent(self, y, u, interp=True):
		'''
		Total extent of the excursion set.
		
		:Parameters:

			*y* --- a 1D field
		
			*u* --- threshold height
			
			*fwhm* --- actual or estimated FWHM
			
			*interp* --- interpolate to threshold *u*
			
		:Returns:

			*k* --- total extent of the excursion set *u*
	
		:Example:
	
			>>> nResels = calc.total_excursion_set_extent(y, 0.5)
			
		:Note:
		
			This is a length measure, so is similar to **nSuprathresholdNodes** minus **nUpcrossings**, with the exception that extents can be interpolated to *u*.
		
		.. danger:: Setting *interp* to False is faster, but it will cause disagreements between node-based and element-based sampling. If the upcrossing is large this difference is negligible, but for small upcrossing there may be strange results (e.g. upcrossing with an extent of zero). Recommendation: **always interpolate**.
		'''
		return sum( self.cluster_extents(y, u, interp=interp) )









class ClusterMetricCalculatorInitialized(object):
	def __init__(self, y, u, interp=True, wrap=False):
		self.y      = y
		self.u      = u
		L,n         = bwlabel(np.array(y >= u), merge_wrapped=wrap)
		self.L      = L
		self.n      = n
		self.interp = interp
		self.wrap   = wrap
		
	
	def cluster_centroids(self):
		c = []
		if self.n > 0:
			for i in range(self.n):
				i     = self.L==(i+1)
				x     = np.arange(self.y.size)[i]
				z     = self.y[i]
				z0    = np.sign(z[0]) * self.u * np.ones(z.size)
				z     = np.hstack([z,z0])
				c.append( (x.mean(), z.mean()) )
		return c
		
	
	def cluster_extents(self):
		if self.n==0:
			m = []
		else:
			m   = []
			for i in range(self.n):
				b       = self.L==(i+1)
				if np.all(b):
					mm  = self.y.size - 1
				elif self.interp:
					up  = Upcrossing(self.y, b, self.interp, self.wrap)
					mm  = up.extent(self.u)
				else:
					mm  = b.sum() - 1
				m.append(mm)
		return m
	
	
	def cluster_minima(self):
		b   = self.y > self.u
		if np.all(b):
			m = [self.y.min()]
		elif np.any(b):
			if self.interp:
				m      = [self.u]*self.n
			else:
				m      = [self.y[self.L==(i+1)].min()  for i in range(self.n)]
		else:
			m = []
		return m
	
	def get_all(self):
		if self.n > 0:
			extents    = self.cluster_extents()
			minima     = self.cluster_minima()
			centroids  = self.cluster_centroids()
		else:
			extents,minima,centroids = [],[],[]
		return extents, minima, centroids, self.L










def bwlabel(b, merge_wrapped=False):
	'''
	Label clusters in a binary field *b*.
	This function yields the same output as **scipy.ndimage.measurements.label**
	but is much faster for 1D fields.
	If *merge_wrapped* 
	
	:Parameters:

		*b* --- a binary field
		
		*merge_wrapped* --- if True, boundary upcrossings will be merged into a single cluster.

	:Returns:

		*L* --- labeled upcrossings (array of integers)
		
		*n* --- number of upcrossings
	
	
	:Example:
	
		>>> y = rft1d.random.randn1d(1, 101, 10.0)
		>>> b = y > 2.0
		>>> L,n = rft1d.geom.bwlabel(b)
	'''
	Q      = b.size
	d      = np.diff(b+0)
	i0     = list(1 + np.argwhere(d==1).flatten())
	i1     = list(np.argwhere(d==-1).flatten())
	if b[0]:
	    i0 = [0] + i0
	if b[-1]:
	    i1.append(Q-1)
	n      = len(i0)
	L      = np.zeros(Q)
	for i,(ii0,ii1) in enumerate(zip(i0,i1)):
	    L[ii0:ii1+1] = i+1
	if merge_wrapped and L[0] and L[-1]:
		L[L==L[-1]] = 1
		n -= 1
	return L,n



def estimate_fwhm(R):
	'''
	Estimate field smoothness (FWHM) from a set of random fields or a set of residuals.
	
	:Parameters:

		*R* --- a set of random fields, or a set of residuals
		
	:Returns:

		*FWHM* --- the estimated FWHM
	
	:Example:
	
		>>> FWHM = 12.5
		>>> y = rft1d.random.randn1d(8, 101, FWHM)
		>>> w = rft1d.geom.estimate_fwhm(y) #should be close to 12.5
		
	.. note:: The estimated FWHM will differ from the specified FWHM (just like sample means differ from the population mean). This function implements an unbiased estimate of the FWHM, so the average of many FWHM estimates is expected to converge to the specified value.
	
	'''
	ssq    = (R**2).sum(axis=0)
	# ### gradient estimation (Method 1:  SPM5, SPM8)
	# dx     = np.diff(R, axis=1)
	# v      = (dx**2).sum(axis=0)
	# v      = np.append(v, 0)   #this is likely a mistake but is entered to match the code in SPM5 and SPM8;  including this yields a more conservative estimate of smoothness
	### gradient estimation (Method 2)
	dy,dx  = np.gradient(R)
	v      = (dx**2).sum(axis=0)
	# normalize:
	v     /= (ssq + eps)
	# ### gradient estimation (Method 3)
	# dx     = np.diff(R, axis=1)
	# v      = (dx**2).sum(axis=0)
	# v     /= (ssq[:-1] + eps)
	# ignore zero-variance nodes:
	i      = np.isnan(v)
	v      = v[np.logical_not(i)]
	# global FWHM estimate:
	reselsPerNode = np.sqrt(v / (4*log(2)))
	FWHM   = 1 / reselsPerNode.mean()
	return FWHM


def resel_counts(R, fwhm=1, element_based=False):
	'''
	Resolution element (resel) counts.
	
	This function assembles resel counts, either from a set of residuals or
	from a binary mask. If using a binary mask, True represents regions which
	are masked out.
	
	:Parameters:

		*R* --- a set of random fields, a set of residuals, or a binary field mask
		
		*fwhm* --- the true or estimated FWHM
		
		*element_based* --- element-based sampling (default: node-based sampling)
		
	:Returns:

		*resels* --- (*r0*, *r1*):  0D and 1D resel counts, respectively
	
	:Note:
	
		The resel counts define the field on which the random process occurs.
		The first count (*r0*) is the Hadwiger characteristic, which specifies
		the number of unbroken field segments. An unbroken field has *r0* = 1.
		The second count (*r1*) is the field size divided by the FWHM.
		
	:Important:
	
		All RFT expectations stem directly from these resel counts.

	:Important cases:
	
		1. Node-based sampling (default), unbroken field with Q nodes --- the field size is (Q-1) and **resels = [1, (Q-1)/FWHM]**
		
		2. Element-based sampling, unbroken field, Q elements --- the field size is Q and **resels = [1, Q/FWHM]**
		
		3. Node-based sampling (default), broken field with S segements and Q nodes --- the field size is (Q-S) and **resels = [S, (Q-S)/FWHM]**
		
		4. Element-based sampling, broken field with S segements and Q elements --- the field size is Q and **resels = [S, Q/FWHM]**

	:Examples (unbroken field):
	
		>>> import numpy as np
		>>> b = np.zeros(101) #no masked regions
		>>> resels = rft1d.geom.resel_counts(b, fwhm=10.0) #yields(1,10)
		>>> resels = rft1d.geom.resel_counts(b, fwhm=10.0, element_based=True) #yields(1,10.1)

	:Examples (broken field):
	
		>>> b = np.zeros(101)
		>>> b[25:55] = 1
		>>> resels = rft1d.geom.resel_counts(b, fwhm=10.0) #yields(2,6.9)
		>>> resels = rft1d.geom.resel_counts(b, fwhm=10.0, element_based=True) #yields(2,7.1)
		
	'''
	### Define binary search area (False = masked):
	if R.ndim==2:
		b     = np.any( np.logical_not(np.isnan(R)), axis=0)
	else:
		b     = np.asarray(np.logical_not(R), dtype=bool)
	### Summarize search area geometry:
	nNodes    = b.sum()
	nClusters = bwlabel(b)[1]
	if element_based:
		resels    = nClusters,  float(nNodes)/fwhm
	else:
		resels    = nClusters,  float(nNodes-nClusters)/fwhm
	return resels



def resels2fwhm(resels, nNodes, element_based=False):
	'''
	Get the FWHM from resel counts based on the number of field nodes.
	
	:Parameters:

		*resels* --- resel counts
		
		*nNodes* --- number of field nodes (in broken fields: number of unbroken nodes)
		
		*element_based* --- element-based sampling (default: node-based sampling)
		
	:Returns:

		*fwhm* --- field FWHM
	
	:Example:
	
		>>> resels = (1, 10.0)
		>>> w = rft1d.geom.resels2fwhm(resels, 101) #yields 10.0
		>>> resels = (2, 6.9)
		>>> w = rft1d.geom.resels2fwhm(resels, 71) #yields 10.0
		
	:Note:
		
		See **rft1d.geom.resel_counts** for details regarding the keyword "element_based"** and node-based vs. element-based sampling.
	'''
	if element_based:
		return float(nNodes) / resels[1]
	else:
		return float(nNodes - resels[0]) / resels[1]
def resels2fwhm_masked(resels, mask, element_based=False):
	'''
	Get the FWHM from resel counts based on a binary field mask
	
	:Parameters:

		*resels* --- resel counts
		
		*mask* --- binary field mask
		
		*element_based* --- element-based sampling (default: node-based sampling)
		
	:Returns:

		*fwhm* --- field FWHM
	
	:Example:
	
		>>> resels = (2, 6.9)
		>>> b = np.zeros(101)
		>>> b[25:55] = 1
		>>> w = rft1d.geom.resels2fwhm_masked(resels, b) #yields 10.0
	
	:Note:
		
		See **rft1d.geom.resel_counts** for details regarding the keyword "element_based"** and node-based vs. element-based sampling.
	'''
	nNodes = np.logical_not(mask).sum()
	return resels2fwhm(resels, nNodes, element_based)
def resels2nelements(resels, fwhm):
	'''
	Get the field size from resel counts based on the FWHM (element-based sampling).

	:Example:
	
		>>> resels = (1, 10.0)
		>>> nNodes = rft1d.geom.resels2nelements(resels, 10.0) #yields 100
		>>> resels = (2, 6.9)
		>>> nNodes = rft1d.geom.resels2nelements(resels, 10.0) #yields 69
	
	:Note:
		
		See **rft1d.geom.resel_counts** for details regarding node-based vs. element-based sampling.
	'''
	return int(fwhm*resels[1])
def resels2nnodes(resels, fwhm):
	'''
	Get the number of field nodes from resel counts based on the FWHM
	
	:Parameters:

		*resels* --- resel counts
		
		*fwhm* --- actual or estimated FWHM*element_based* --- element-based sampling (default: node-based sampling)
		
	:Returns:

		*nNodes* --- number of field nodes
	
	:Example:
	
		>>> resels = (1, 10.0)
		>>> nNodes = rft1d.geom.resels2nnodes(resels, 10.0) #yields 101
		>>> resels = (2, 6.9)
		>>> nNodes = rft1d.geom.resels2nnodes(resels, 10.0) #yields 71
	
	:Note:
		
		See **rft1d.geom.resel_counts** for details regarding node-based vs. element-based sampling.
	'''
	return int(resels[0] + fwhm*resels[1])
def resels2fieldsize(resels, fwhm, element_based=False):
	'''
	Get the field size from resel counts based on the FWHM.
	Equivalent to **rft1d.geom.resels2nnodes** minus the number of unbroken
	field segments.

	:Example:
	
		>>> resels = (1, 10.0)
		>>> nNodes = rft1d.geom.resels2fieldsize(resels, 10.0) #yields 100
		>>> resels = (2, 6.9)
		>>> nNodes = rft1d.geom.resels2fieldsize(resels, 10.0) #yields 69
	
	:Note:
		
		See **rft1d.geom.resel_counts** for details regarding the keyword "element_based"** and node-based vs. element-based sampling.
	'''
	if element_based:
		return resels2nelements(resels, fwhm)
	else:
		return resels2nnodes(resels, fwhm) - resels[0]



