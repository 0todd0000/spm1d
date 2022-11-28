
import numpy as np
from matplotlib import pyplot
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from spm1d import rft1d



def plot_filled(y, ax, thresh=None, plot_thresh=True, color='k', lw=2, facecolor='0.8', two_tailed=False, thresh_color='k'):
	y        = np.asarray(y, dtype=float)
	x        = np.arange(y.size)
	if thresh is None:
		thresh      = 0
	x0,y0,ind0      = x.copy(), y.copy(), np.arange(y.size)
	### threshold:
	if two_tailed:
		L,n      = rft1d.geom.bwlabel( np.abs(y)>thresh )
	else:
		L,n      = rft1d.geom.bwlabel( y>thresh )
	### plot:
	ax.plot(x0, y0, color=color, lw=lw)
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
			polyg.append(  Polygon( np.array((x,y)).T  )  )
		patches         = PatchCollection(polyg, edgecolors=None)
		ax.add_collection(patches)
		pyplot.setp(patches, facecolor=facecolor, edgecolor=facecolor)
	#set axis limits:
	pyplot.setp(ax, xlim=(x0.min(), x0.max())  )
	#plot threshold(s):
	if (thresh is not None) and plot_thresh:
		h      = [ax.hlines(thresh, x0.min(), x0.max())]
		if two_tailed:
			h.append( ax.hlines(-thresh, x0.min(), x0.max()) )
		pyplot.setp(h, color=thresh_color, lw=1, linestyle='--')




### EPS production preliminaries:
fig_width_mm  = 200
fig_height_mm = 85
mm2in = 1/25.4
fig_width  = fig_width_mm*mm2in  	# width in inches
fig_height = fig_height_mm*mm2in    # height in inches
params = {	'backend':'ps', 'axes.labelsize':14,
			'font.size':12, 'text.usetex': False, 'legend.fontsize':12,
			'xtick.labelsize':8, 'ytick.labelsize':8,
			'font.family':'Times New Roman',  #Times
			'lines.linewidth':0.5,
			'patch.linewidth':0.25,
			'figure.figsize': [fig_width,fig_height]}
pyplot.rcParams.update(params)




#(0) Set parameters:
np.random.seed(0)
nNodes      = 101
W           = 20
h           = 0.55
y           = rft1d.random.randn1d(1, nNodes, W, pad=True)



#(1) Plot results:
pyplot.close('all')
color0      = 0.24, 0.41, 0.72
color1      = 0.74, 0.76, 0.89
color2      = 0.21, 0.57, 0.89
### create axes:
ax0   = pyplot.axes([0.06,0.14,0.44,0.84])
ax1   = pyplot.axes([0.55,0.14,0.44,0.84])
AX    = ax0,ax1
for ax in [ax0,ax1]:
	plot_filled(y, ax, thresh=h, plot_thresh=False, color='k', lw=2, facecolor=color0)
	ax.hlines(0, 0, 100, color='k', linestyle='-', lw=0.5)
	ax.hlines(h, 0, 100, color=color0, linestyle='--')
### plot nNodes:
ind   = range(25,38)
ax1.plot(ind, y[ind], 'o', markersize=6, markerfacecolor=color1, markeredgecolor=color0)
ax1.plot(ind, [h]*len(ind), 'o', markersize=6, markerfacecolor=color1, markeredgecolor=color0)
for i in ind:
	ax1.plot([i,i], [h,y[i]], '0.7')
ax1.text(31, 0.58, 'extent (nodes)', color='w', ha='center', size=14)
### label threshold:
ax0.text(72, 0.4, 'threshold  $u$', color=color0, size=12)
### plot maximum:
ax0.plot(y.argmax(), y.max(), 'o', markersize=5, markerfacecolor='w', markeredgecolor=color0)
ax1.plot(y.argmax(), y.max(), 'o', markersize=12, markerfacecolor='w', markeredgecolor=color0)
ax0.plot([48]*2, [0,y.max()], '-', lw=3, marker='<', color=color0)
ax0.text(52, y.max(), 'maximum height  $z_{\mathrm{max}}$', color=color0, size=12)
### plot extent:
ax1.hlines(h, 0, 100, color=color0, linestyle='-', lw=3)
ax1.plot([24.1,37.9], [0.519]*2, '^-', lw=3, color=color0)
ax1.text(31, 0.49, 'extent (interpolated)', color=color0, ha='center', size=14)
### axes labels:
[ax.set_xlabel('Field position  (%)')   for ax in AX]
ax0.text(-0.15, 0.5, '$z$', size=24, transform=ax0.transAxes, rotation=90, va='center')
### annotate:
pyplot.setp(ax0, xlim=(0,100), ylim=(-1.2,1.2))
pyplot.setp(ax1, xlim=(23,39), ylim=(0.47,0.92))
### panel labels:
ax0.text(0.04, 0.91, '(a) Upcrossing', transform=ax0.transAxes)
ax1.text(0.04, 0.91, '(b) Upcrossing  (zoomed)', transform=ax1.transAxes)
pyplot.show()



