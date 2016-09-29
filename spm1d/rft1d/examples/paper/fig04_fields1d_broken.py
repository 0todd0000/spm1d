
import numpy as np
from scipy import stats
from matplotlib import pyplot,cm
from spm1d import rft1d


def scalar2color(x, cmap=cm.jet, xmin=None, xmax=None):
	x          = np.asarray(x, dtype=float)
	if xmin is None:
		xmin   = x.min()
	if xmax is None:
		xmax   = x.max()
	xn         = (x - xmin)  / (xmax-xmin)
	xn        *= 255
	xn         = np.asarray(xn, dtype=int)
	colors     = cmap(xn)
	return colors
	
	

### EPS production preliminaries:
fig_width_mm  = 240
fig_height_mm = 70
mm2in = 1/25.4
fig_width  = fig_width_mm*mm2in  	# width in inches
fig_height = fig_height_mm*mm2in    # height in inches
params = {	'backend':'ps', 'axes.labelsize':14,
			'font.size':12, 'text.usetex': False, 'legend.fontsize':11,
			'xtick.labelsize':8, 'ytick.labelsize':8,
			'font.family':'Times New Roman',  #Times
			'lines.linewidth':0.5,
			'patch.linewidth':0.25,
			'figure.figsize': [fig_width,fig_height]}
pyplot.rcParams.update(params)





#(0) Specify parameters:
np.random.seed(0)
nNodes       = 101
FWHM         = [5.0, 10.0, 25.0]
nResponses   = 20
heights      = np.linspace(1.0, 3.0, 11)
### generate mask:
nodes        = np.array([True]*nNodes)
nodes[20:35] = False
nodes[60:80] = False
### assemble the field's geometric characteristics:
nSegments    = rft1d.geom.bwlabel(nodes)[1]  #number of unbroken field segments (here: 3)
nNodesTotal  = nodes.sum() #number of nodes in the unbroken field segments
fieldSize    = nNodesTotal - nSegments


#(1) Generate broken random fields:
y0           = rft1d.randn1d(nResponses, nodes, FWHM[0], pad=True)
y1           = rft1d.randn1d(nResponses, nodes, FWHM[1], pad=True)
y2           = rft1d.randn1d(nResponses, nodes, FWHM[2], pad=True)





#(2) Plot results:
pyplot.close('all')
axx         = np.linspace(0.04, 0.695, 3)
AX          = [pyplot.axes([xx,0.18,0.29,0.8])   for xx in axx]
ax0,ax1,ax2 = AX
### plot fields:
colors      = scalar2color(range(nResponses+3), cmap=cm.RdPu)
[ax0.plot(yy, color=color)  for yy,color in zip(y0,colors)]
[ax1.plot(yy, color=color)  for yy,color in zip(y1,colors)]
[ax2.plot(yy, color=color)  for yy,color in zip(y2,colors)]
### adjust axes:
pyplot.setp(AX, xlim=(0,100), ylim=(-3.8,3.8))
pyplot.setp([ax1,ax2], yticklabels=[])
### panel labels:
for i,(ax,w) in enumerate(zip(AX,FWHM)):
	s   = '(%s)  FWHM = %d%%' %(chr(97+i), w)
	ax.text(0.05, 0.9, s, transform=ax.transAxes, size=12)
### label the axes:
[ax.set_xlabel('Field position  (%)', size=18)   for ax in AX]
ax0.text(-0.15, 0.5, '$z$', size=24, transform=ax0.transAxes, rotation=90, va='center')
pyplot.show()


# pyplot.savefig('fig_fields1d_broken.pdf')







