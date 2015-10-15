
'''
This module contains a variety of plotting functions.

The following functions may be accessed as methods of **spm1d** SPM objects:

=========================  ===================== ===============================
spm1d.plot                 SPM instance method   SPM inference instance method
=========================  ===================== ===============================
plot_spm                   plot
plot_spm_design            plot_design           plot_design
plot_spmi                                        plot
plot_spmi_p_values                               plot_p_values
plot_spmi_threshold_label                        plot_threshold_label
=========================  ===================== ===============================


All other plotting functions can only be accessed via **spm1d.plot**.
These include:

- plot_cloud
- plot_errorcloud
- plot_mean_sd
'''

# Copyright (C) 2014  Todd Pataky
# plot.py version: 0.2.0005 (2014/06/24)


from math import pi,sin,cos,acos,atan2
import numpy as np
from scipy import ndimage
import matplotlib
from matplotlib import pyplot, cm as colormaps
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



def _gca(ax):
	if ax==None:
		ax = pyplot.gca()
	return ax
def _getQ(x, Q):
	if x==None:
		x    = np.arange(Q)
	return x
def _set_ylim(ax, pad=0.075):
	def minmax(x):
		return min(x), max(x)
	ymin,ymax   = +1e10, -1e10
	for line in ax.lines:
		y0,y1   = minmax( line.get_data()[1] )
		ymin    = min(y0, ymin)
		ymax    = max(y1, ymax)
	for collection in ax.collections:
		datalim = collection.get_datalim(ax.transData)
		y0,y1   = minmax(  np.asarray(datalim)[:,1]  )
		ymin    = min(y0, ymin)
		ymax    = max(y1, ymax)
	for text in ax.texts:
		r       = matplotlib.backend_bases.RendererBase()
		bbox    = text.get_window_extent(r)
		y0,y1   = ax.transData.inverted().transform(bbox)[:,1]
		ymin    = min(y0, ymin)
		ymax    = max(y1, ymax)
	dy = 0.075*(ymax-ymin)
	ax.set_ylim(ymin-dy, ymax+dy)
def _stat2str(STAT):
	if STAT=='T':
		s    = 't'
	else:
		s    = STAT
	return s
def p2string(p):
	return 'p < 0.001' if p<0.0005 else 'p = %.03f'%p
	






def plot_cloud(Y, ax=None, facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
	'''
	Plot an arbitrary 1D cloud.
	
	:Parameters:
	
	- *Y* --- a (2 x Q) numpy array containing y coordinates of the cloud's top and bottom surfaces, respectively
	- *ax* --- optional matplotlib.axes object
	- *facecolor* --- optional face color (for the SD cloud)
	- *edgecolor* --- optional edge color (for the SD cloud)
	- *alpha* --- optional face alpha value (for the SD cloud)
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes

	:Returns:
	
	- a **matplotlib.collections.PatchCollection** object
	
	:Example:
	
	>>> import numpy as np
	>>> from matplotlib import pyplot
	
	>>> y_top     = np.random.rand(50)
	>>> y_bottom  = -0.5 * np.ones(50)
	>>> Y         = np.vstack([y_top, y_bottom])
	>>> spm1d.plot.plot_cloud(Y)
	>>> pyplot.xlim(0, 50)
	>>> pyplot.ylim(-1, 1)
	'''
	x           = _getQ(None, Y.shape[1])
	ax          = _gca(ax)
	### create patches:
	y0,y1       = Y
	x,y0,y1     = x.tolist(), y0.tolist(), y1.tolist()
	x           = [x[0]]  + x  + [x[-1]]
	y0          = [y0[0]] + y0 + [y0[-1]]
	y1          = [y1[0]] + y1 + [y1[-1]]
	y1.reverse()
	### concatenate:
	x1          = np.copy(x).tolist()
	x1.reverse()
	x,y         = x + x1, y0 + y1
	patches     = PatchCollection([Polygon(zip(x,y))], edgecolors=None)
	### plot:
	ax.add_collection(patches)
	pyplot.setp(patches, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha)
	if autoset_ylim:
		_set_ylim(ax)
	return patches






def plot_errorcloud(datum, sd, ax=None, facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True, perpendicular=False):
	'''
	Plot an arbitrary error cloud surrounding a datum continuum.
	
	:Parameters:
	
	- *datum* --- a 1D list or numpy array
	- *sd* --- a 1D list or numpy array
	- *ax* --- optional matplotlib.axes object
	- *facecolor* --- optional face color (for the SD cloud)
	- *edgecolor* --- optional edge color (for the SD cloud)
	- *alpha* --- optional face alpha value (for the SD cloud)
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes

	:Returns:
	
	- a **matplotlib.collections.PatchCollection** object
	
	:Example:
	
	>>> import numpy as np
	>>> from matplotlib import pyplot
	
	>>> a     = np.random.rand(50)
	>>> b     = np.random.rand(50)
	>>> spm1d.plot.plot_errorcloud(a, b)
	>>> pyplot.xlim(0, 50)
	'''
	ax       = _gca(ax)
	y,s      = np.asarray(datum, dtype=float), np.asarray(sd, dtype=float)
	Y        = np.array([y+s, y-s])
	h        = plot_cloud(Y, ax, facecolor, edgecolor, alpha, autoset_ylim=False)
	# if perpendicular:
	# 	w        = 0.2
	# 	x        = _getQ(None, y.size)
	# 	line     = ThickSegmentedLine(x, y, sd=s)
	# 	h        = line.plot(vertical_ends=True, lw=3)
	#
	# else:
	# 	Y        = np.array([y+s, y-s])
	# 	h        = plot_cloud(Y, ax, facecolor, edgecolor, alpha, autoset_ylim=False)
	if autoset_ylim:
		_set_ylim(ax)
	return h





def plot_filled(y, ax=None, thresh=None, plot_thresh=True, color='k', lw=2, facecolor='0.8', two_tailed=False, thresh_color='k', autoset_ylim=True, label=None):
	'''
	Plot a filled cluster.
	
	(This function should only be used through **spm1d.plot.plot_spmi**)
	'''
	y        = np.asarray(y, dtype=float)
	x        = _getQ(None, y.size)
	ax       = _gca(ax)
	if thresh==None:
		thresh      = 0
	x0,y0,ind0      = x.copy(), y.copy(), np.arange(y.size)
	### threshold:
	if two_tailed:
		L,n      = ndimage.label(np.abs(y)>thresh)
	else:
		L,n      = ndimage.label(y>thresh)
	### plot:
	ax.plot(x0, y0, color=color, lw=lw, label=label)
	### create patches if needed:
	if n>0:
		polyg = []
		for i in range(n):
			ind         = ind0[L==i+1].tolist()
			x           = x0[L==i+1].tolist()
			y           = y0[L==i+1].tolist()
			csign       = np.sign(y[0])
			### insert extra nodes for interpolation:
			x           = [x[0]] + x + [x[-1]]
			y           = [csign*thresh] + y + [csign*thresh]
			### interpolate if necessary:
			if ind[0]  != ind0[0]:
				dx      = x0[ind[0]] - x0[ind[0]-1]
				dy      = (csign*thresh - y0[ind[0]])  / (y0[ind[0]] - y0[ind[0]-1])
				x[0]   += dy*dx
			if ind[-1] != ind0[-1]:
				dx      = x0[ind[-1]+1] - x0[ind[-1]]
				dy      = (csign*thresh - y0[ind[-1]])  / (y0[ind[-1]+1] - y0[ind[-1]])
				x[-1]  += dy*dx
			polyg.append(  Polygon(zip(x,y))  )
		patches         = PatchCollection(polyg, edgecolors=None)
		ax.add_collection(patches)
		pyplot.setp(patches, facecolor=facecolor, edgecolor=facecolor)
	#set axis limits:
	# pyplot.setp(ax, xlim=(x0.min(), x0.max()), ylim=(y0.min(), y0.max()))
	pyplot.setp(ax, xlim=(x0.min(), x0.max())  )
	#plot threshold(s):
	if (thresh!=None) and plot_thresh:
		h      = [ax.hlines(thresh, x0.min(), x0.max())]
		if two_tailed:
			h.append( ax.hlines(-thresh, x0.min(), x0.max()) )
		pyplot.setp(h, color=thresh_color, lw=1, linestyle='--')
	if autoset_ylim:
		_set_ylim(ax)







def plot_mean_sd(Y, ax=None, lw=3, linecolor='k', linestyle='-', facecolor='0.8', edgecolor='0.8', alpha=0.5, label=None, autoset_ylim=True, perpendicular=True):
	'''
	Plot mean continuum with standard deviation cloud.
	
	:Parameters:
	
	- *Y* --- a (J x Q) numpy array
	- *ax* --- optional matplotlib.axes object  [default: matplotlib.pyplot.gca()]
	- *lw* --- optional integer specify line width
	- *linecolor* --- optional line color specifier (for the mean continuum)
	- *linestyle* --- optional line style specifier (for the mean continuum)
	- *facecolor* --- optional face color (for the SD cloud)
	- *edgecolor* --- optional edge color (for the SD cloud)
	- *alpha* --- optional face alpha value (for the SD cloud)
	- *label* --- optional string to label the mean continuum (for use with matplotlib.pyplot.legend())
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes
	
	:Returns:
	
	- *None*
	
	:Example:
	
	>>> Y  = np.random.randn(10,101)
	>>> spm1d.plot.plot_mean_sd(Y)
	'''
	x        = _getQ(None, Y.shape[1])
	ax       = _gca(ax)
	m,s      = Y.mean(axis=0), Y.std(ddof=1, axis=0)
	h        = ax.plot(x, m, color=linecolor, lw=lw, linestyle=linestyle)[0]
	if label:
		h.set_label(label)
	plot_errorcloud(m, s, ax, facecolor, edgecolor, alpha, autoset_ylim=False, perpendicular=perpendicular)
	pyplot.setp(ax, xlim=(x.min(), x.max())  )
	if autoset_ylim:
		_set_ylim(ax)






def plot_spm(spm, ax=None, plot_ylabel=True, autoset_ylim=True, **kwdargs):
	'''
	Plot an **spm1d** SPM object as a line.
	
	:Parameters:
	
	- *spm* --- an **spm1d** SPM object (not needed if using the SPM.plot method)
	- *ax* --- optional matplotlib.axes object  [default: matplotlib.pyplot.gca()]
	- *plot_ylabel* --- if *True*, then an "SPM{t}" or "SPM{F}" label will automatically be added to the y axis
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes
	- *kwdards* --- any keyword argument accepted by **matplotlib.pyplot.plot**
	
	:Returns:
	
	- *h* --- a **matplotlib.lines.Line2D** object
	
	:Example:
	
	>>> t     = spm1d.stats.ttest(Y)
	>>> line  = t.plot()   # equivalent to "line = spm1d.plot.plot_spm(t)"
	>>> line.set_color('r')
	'''
	ax     = _gca(ax)
	x      = _getQ(None, spm.Q)
	keys   = kwdargs.keys()
	if 'color' not in keys:
		kwdargs.update( dict(color='k') )
	if ('lw' not in keys) or ('linewidth' not in keys):
		kwdargs.update( dict(lw=2) )
	if plot_ylabel:
		ax.set_ylabel('SPM{%s}'%_stat2str(spm.STAT), size=16)
	h      = ax.plot(x, spm.z, **kwdargs)[0]
	if autoset_ylim:
		_set_ylim(ax)
	return h




def plot_spm_design(spm, ax=None, factor_labels=None, fontsize=10):
	'''
	Plot the design matrix.
	
	:Returns:
	
	None
	'''
	def scaleColumns(X):
		mn,mx     = np.min(X,axis=0) , np.max(X,axis=0)
		Xs        = (X-mn)/(mx-mn+eps)
		Xs[np.isnan(Xs)] = 1   #if the whole column is a constant
		return Xs
	ax            = _gca(ax)
	X             = spm.X
	vmin,vmax     = None, None
	if np.all(X==1):
		vmin,vmax = 0, 1
	ax.imshow(scaleColumns(X), cmap=colormaps.gray, interpolation='nearest', vmin=vmin, vmax=vmax)
	if factor_labels != None:
		gs        = X.shape
		tx        = [ax.text(i, -0.05*gs[0], label)   for i,label in enumerate(factor_labels)]
		pyplot.setp(tx, ha='center', va='bottom', color='k', fontsize=fontsize)
	ax.axis('normal')
	ax.axis('off')






def plot_spmi(spmi, ax=None, color='k', facecolor='0.8', plot_thresh=True, plot_ylabel=True, thresh_color='k', autoset_ylim=True, label=None):
	'''
	Plot an **spm1d** SPM inference object as a line.
	
	:Parameters:
	
	- *spmi* --- an **spm1d** SPM object
	- *ax* --- optional matplotlib.axes object  [default: matplotlib.pyplot.gca()]
	- *color* --- optional line color specifier (for the raw SPM)
	- *facecolor* --- optional face color (for suprathreshold clusters)
	- *plot_thresh* --- if *True*, one or two horizontal threshold lines will be plotted (for one- or two-tailed inference)
	- *plot_ylabel* --- if *True*, an "SPM{t}" or "SPM{F}" label will automatically be added to the y axis
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes
	
	:Returns:
	
	- *None*
	
	:Example:
	
	>>> t     = spm1d.stats.ttest(Y)
	>>> ti    = t.inference(0.05)
	>>> ti.plot()   # equivalent to "spm1d.plot.plot_spmi(ti)"
	'''
	ax     = _gca(ax)
	x      = _getQ(None, spmi.Q)
	plot_filled(spmi.z, ax, spmi.zstar, color=color, plot_thresh=plot_thresh, facecolor=facecolor, two_tailed=spmi.two_tailed, thresh_color=thresh_color, autoset_ylim=False, label=label)
	ax.hlines(0, x.min(), x.max(), color='k', lw=1, linestyle=':')
	if plot_ylabel:
		ax.set_ylabel('SPM{%s}'%_stat2str(spmi.STAT), size=16)
	if autoset_ylim:
		_set_ylim(ax)




def plot_spmi_p_values(spmi, ax=None, size=8, offsets=None, offset_all_clusters=None, autoset_ylim=True):
	'''
	Plot an **spm1d** SPM inference object's p values as text (if they exist).
	
	:Parameters:
	
	- *spmi* --- an **spm1d** SPM inference object
	- *ax* --- optional matplotlib.axes object  [default: matplotlib.pyplot.gca()]
	- *size* --- optional integer specifying font size
	- *offsets* --- optional list of 2-tuples specifying (x,y) offsets with respect to cluster centroids
	- *offset_all_clusters* --- optional 2-tuple specifying the (x,y) offset for all clusters, with respect to cluster centroids
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes
	
	:Returns:
	
	- *None*
	
	:Example:
	
	>>> t   = spm1d.stats.ttest(Y)
	>>> ti  = t.inference(0.05)
	>>> ti.plot()
	>>> myoffsets = [(0,0), (0,0.2), (0,0.1)]  # if there are three clusters, there must be three 2-tuple offsets
	>>> ti.plot_p_values(offsets=myoffsets) #equivalent to: "spm1d.plot.plot_p_values(ti, offsets=myoffsets)"
	
	'''
	ax         = _gca(ax)
	n          = len(spmi.p)
	if offsets is None:
		if offset_all_clusters is None:
			offsets = [(0,0)]*n
		else:
			offsets = [offset_all_clusters]*n
	if len(offsets) < n:
		print('WARNING:  there are fewer offsets than clusters.  To set offsets for all clusters use the offset_all_clusters keyword.')
	for cluster,offset in zip(spmi.clusters, offsets):
		x,y    = cluster.xy
		x     += offset[0]
		y     += offset[1]
		s      = p2string(cluster.P)
		ax.text(x, y, s, size=size, ha='center', va='center', bbox=dict(facecolor='w', alpha=0.3))
	if autoset_ylim:
		_set_ylim(ax)






def plot_spmi_threshold_label(spmi, ax=None, lower=False, pos=None, autoset_ylim=True, **kwdargs):
	'''
	Plot an **spm1d** SPM inference object as a line.
	
	:Parameters:
	
	- *spmi* --- an **spm1d** SPM inference object
	- *ax* --- optional matplotlib.axes object  [default: matplotlib.pyplot.gca()]
	- *lower* --- if True, will plot the label on the lower threshold (if two-tailed inference has been conducted)
	- *pos* --- optional 2-tuple specifying text object location; setting "pos" over-rides "lower"
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes
	- *kwdards* --- any keyword argument accepted by **matplotlib.pyplot.text**
	
	:Returns:
	
	- a **matplotlib.text.Text** object
	
	:Example:
	
	>>> t     = spm1d.stats.ttest(Y)
	>>> ti    = t.inference(0.05)
	>>> ti.plot_threshold_label(pos=(50,3.0))   # equivalent to "spm1d.plot.plot_spmi_threshold_label(ti, pos=(50,3.0))"
	'''
	q         = _getQ(None, spmi.Q)
	ax        = _gca(ax)
	if pos==None:
		x0,x1 = q.min(), q.max()
		y0,y1 = ax.get_ylim()
		x     = x0 + 0.4*(x1-x0)
		if lower and spmi.two_tailed:
			y     = -spmi.zstar + 0.005*(y1-y0)
		else:
			y     = spmi.zstar + 0.005*(y1-y0)
	else:
		x,y   = pos
	if 'color' not in kwdargs.keys():
		kwdargs.update( dict(color='r') )
	s         = r'$\alpha$=%.2f:  $%s^*$=%.3f' %(spmi.alpha, _stat2str(spmi.STAT), spmi.zstar)
	h         = ax.text(x, y, s, **kwdargs)
	if autoset_ylim:
		_set_ylim(ax)
	return h

