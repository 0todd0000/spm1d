
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

# Copyright (C) 2016  Todd Pataky
# updated (2016/10/01) todd




import numpy as np
from . _plot import DataPlotter, SPMPlotter, SPMiPlotter, _legend_manual




def legend_manual(ax, colors=None, labels=None, linestyles=None, markerfacecolors=None, linewidths=None, **kwdargs):
	return _legend_manual(ax, colors, labels, linestyles, markerfacecolors, linewidths, **kwdargs)



def plot_ci_0d(ci, ax=None, color='b', color_criterion='r', markersize=10, autoset_ylim=True):
	'''
	Plot a one-sample confidence interval for 0D data.
	'''
	plotter   = DataPlotter(ax)
	plotter.plot_errorbar(ci.mean, ci.hstar, color=color, x=0)
	if ci.mu is not None:
		plotter.plot_datum(ci.mu, color=color_criterion, linestyle='--')
	plotter.set_ax_prop(xticks=[])
	if autoset_ylim:
		plotter._set_ylim(ax)



def plot_ci_multisample_0d(ci, ax=None, color='b', color_criterion='r', markersize=10, autoset_ylim=True):
	'''
	Plot a paired- or two-sample confidence interval for 0D data.
	'''
	plotter   = DataPlotter(ax)
	if ci.criterion_type == 'meanB':
		hbarw = 0.1
		x0,x1 = 0, 2.4*hbarw*ci.hstar
		plotter.plot_errorbar(ci.meanA, ci.hstar, color=color, x=x0, hbarw=hbarw)
		plotter.plot(x1, ci.meanB, 'o', color=color_criterion, markersize=markersize)
		# plotter.plot_errorbar(ci.meanB, ci.hstar, color=color_criterion, x=x1, hbarw=hbarw)
		plotter.plot_datum(ci.meanB, color=color_criterion, linestyle='--')
	elif ci.criterion_type == 'tailB':
		hbarw = 0.1
		x0,x1 = 0, 1.2*hbarw*ci.hstar
		plotter.plot_errorbar(ci.meanA, 0.5*ci.hstar, color=color, x=x0, hbarw=hbarw)
		plotter.plot_errorbar(ci.meanB, 0.5*ci.hstar, color=color_criterion, x=x1, hbarw=hbarw)
		y     = (ci.meanB - 0.5*ci.hstar) if ( ci.meanB > ci.meanA ) else (ci.meanB + 0.5*ci.hstar)
		plotter.plot_datum(y, color=color_criterion, linestyle='--')
	if autoset_ylim:
		plotter._set_ylim(ax)





def plot_ci(ci, ax=None, x=None, linecolor='k', facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
	'''
	Plot a condfidence interval.
	'''
	y,h,Q     = ci.mean, ci.hstar, ci.Q
	### initialize plotter:
	plotter   = DataPlotter(ax)
	plotter._set_x(x, Q)
	### plot datum, error cloud and threshold:
	plotter.plot(y, color=linecolor, lw=3)
	plotter.plot_cloud([y+h, y-h], facecolor, edgecolor, alpha)
	if ci.mu is not None:
		if ci.isscalarmu:
			plotter.plot_datum(y=ci.mu, color='r', linestyle='--')
		else:
			plotter.plot(ci.mu, color='r', linestyle='--')
	### set axes limits:
	if autoset_ylim:
		plotter._set_ylim(ax)
	plotter._set_xlim()


def plot_ci_multisample(ci, ax=None, x=None, linecolors=('k','b'), facecolors=('0.8','b'), edgecolors=('0.8','b'), color_criterion='r', alphas=(0.5,0.5), autoset_ylim=True):
	'''
	Plot a multi-mean condfidence interval.
	'''
	### assemble means and thresholds:
	mA,mB,h     = ci.meanA, ci.meanB, ci.hstar
	### initialize plotter:
	plotter     = DataPlotter(ax)
	plotter._set_x(x, ci.Q)
	### assemble line and face properties:
	linecolors  = linecolors if isinstance(linecolors, (tuple,list)) else [linecolors]*2
	facecolors  = facecolors if isinstance(facecolors, (tuple,list)) else [facecolors]*2
	edgecolors  = edgecolors if isinstance(edgecolors, (tuple,list)) else [edgecolors]*2
	alphas      = alphas     if isinstance(alphas, (tuple,list))     else [alphas]*2
	### datum- and criterion-dependent plotting:
	if ci.criterion_type == 'meanB':
		plotter.plot(mA, color=linecolors[0], lw=3)
		plotter.plot_cloud([mA+h, mA-h], facecolors[0], edgecolors[0], alphas[0])
		plotter.plot(mB, color=color_criterion, linestyle='--')
	elif ci.criterion_type == 'tailB':
		plotter.plot(mA, color=linecolors[0], lw=3)
		plotter.plot(mB, color=linecolors[1], lw=3)
		hA = plotter.plot_cloud([mA+0.5*h, mA-0.5*h], facecolors[0], edgecolors[0], alphas[0], edgelinestyle='--')
		hB = plotter.plot_cloud([mB+0.5*h, mB-0.5*h], facecolors[1], edgecolors[1], alphas[1], edgelinestyle='--')
	if autoset_ylim:
		plotter._set_ylim(ax)
	plotter._set_xlim()





def plot_errorcloud(datum, sd, ax=None, x=None, facecolor='0.8', edgecolor='0.8', alpha=0.5, autoset_ylim=True):
	'''
	Plot an arbitrary error cloud surrounding a datum continuum.
	
	:Parameters:
	
	- *datum* --- a 1D list or numpy array
	- *sd* --- a 1D list or numpy array
	- *ax* --- optional matplotlib.axes object
	- *x* --- optional vector of x positions  [default: np.arange(datum.size)]
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
	plotter  = DataPlotter(ax)
	plotter._set_x(x, datum.size)
	y,s      = np.asarray(datum, dtype=float), np.asarray(sd, dtype=float)
	Y        = np.array([y+s, y-s])
	h        = plotter.plot_cloud(Y, facecolor, edgecolor, alpha)
	if autoset_ylim:
		plotter._set_ylim(ax)
	return h






def plot_mean_sd(Y, ax=None, x=None, lw=3, linecolor='k', linestyle='-', facecolor='0.8', edgecolor='0.8', alpha=0.5, label=None, autoset_ylim=True, roi=None):
	'''
	Plot mean continuum with standard deviation cloud.
	
	:Parameters:
	
	- *Y* --- a (J x Q) numpy array
	- *ax* --- optional matplotlib.axes object  [default: matplotlib.pyplot.gca()]
	- *x* --- optional vector of x positions  [default: np.arange(Y.shape[1])]
	- *lw* --- optional integer specify line width
	- *linecolor* --- optional line color specifier (for the mean continuum)
	- *linestyle* --- optional line style specifier (for the mean continuum)
	- *facecolor* --- optional face color (for the SD cloud)
	- *edgecolor* --- optional edge color (for the SD cloud)
	- *alpha* --- optional face alpha value (for the SD cloud)
	- *label* --- optional string to label the mean continuum (for use with matplotlib.pyplot.legend())
	- *autoset_ylim* --- if True (default), will set the y axis limits so that all text, line and patch objects are visible inside the axes
	- *roi* --- optional region-of-interest vector (either boolean OR vector of (-1, 0, +1))
	
	:Returns:
	
	- *None*
	
	:Example:
	
	>>> Y  = np.random.randn(10,101)
	>>> spm1d.plot.plot_mean_sd(Y)
	'''
	plotter  = DataPlotter(ax)
	plotter._set_x(x, Y.shape[1])
	### plot mean and SD:
	Y        = Y if roi is None else np.ma.masked_array(   Y, np.vstack([np.logical_not(roi)]*Y.shape[0])   )
	m,s      = Y.mean(axis=0), Y.std(ddof=1, axis=0)
	h        = plotter.plot(m, color=linecolor, lw=lw, linestyle=linestyle)[0]
	if label is not None:
		h.set_label(label)
	### plot SD:
	Y        = np.array([m+s, m-s])
	hc       = plotter.plot_cloud(Y, facecolor, edgecolor, alpha)
	if autoset_ylim:
		plotter._set_axlim()
	return h,hc




def plot_roi(roi, ax=None, facecolor='0.7', alpha=1, edgecolor='w', ylim=None):
	plotter   = DataPlotter(ax)
	plotter.plot_roi(roi, ylim=ylim, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha)




def plot_spm(spm, ax=None, plot_ylabel=True, autoset_xlim=True, autoset_ylim=True, **kwdargs):
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
	plotter = SPMPlotter(spm, ax=ax)
	plotter.plot(**kwdargs)
	if plot_ylabel:
		plotter.plot_ylabel()
	if autoset_xlim:
		plotter._set_xlim()
	if autoset_ylim:
		plotter._set_ylim()
	




def plot_spm_design(spm, ax=None, factor_labels=None, fontsize=10):
	'''
	Plot the design matrix.
	
	:Returns:
	
	None
	'''
	plotter = SPMPlotter(spm, ax=ax)
	plotter.plot_design(factor_labels, fontsize)


def plot_spmi(spmi, ax=None, color='k', linestyle='-', marker='', facecolor='0.8', lw=2, plot_thresh=True,
			  plot_ylabel=True, thresh_color='k', autoset_xlim=True, autoset_ylim=True, label=None):
	'''
	Plot an **spm1d** SPM inference object as a line.
	
	:Parameters:
	
	- *spmi* --- an **spm1d** SPM object
	- *ax* --- optional matplotlib.axes object  [default: matplotlib.pyplot.gca()]
	- *color* --- optional line color specifier (for the raw SPM)
	- *linestyle* --- optional line style specifier (for the raw SPM)
	- *marker* --- optional marker specifier (for the raw SPM)
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
	plotter = SPMiPlotter(spmi, ax=ax)
	plotter.plot(color=color, lw=lw, linestyle=linestyle, marker= marker, facecolor=facecolor, label=label, thresh_color=thresh_color)
	if plot_ylabel:
		plotter.plot_ylabel()
	if autoset_xlim:
		plotter._set_xlim()
	if autoset_ylim:
		plotter._set_ylim()




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
	plotter = SPMiPlotter(spmi, ax=ax)
	h       = plotter.plot_p_values(size, offsets, offset_all_clusters)
	if autoset_ylim:
		plotter._set_ylim(ax)
	return h







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
	plotter = SPMiPlotter(spmi, ax=ax)
	h       = plotter.plot_threshold_label(lower=False, pos=pos, **kwdargs)
	if autoset_ylim:
		plotter._set_ylim(ax)
	return h

