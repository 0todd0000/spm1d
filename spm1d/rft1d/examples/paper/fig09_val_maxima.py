
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
fig_width_mm  = 100
fig_height_mm = 80
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
nResponses = 500  #increase this to 2000 to reproduce the results from the paper
nNodes     = 101
WW         = [5, 10, 20, 40]
heights    = np.linspace(2, 4, 21)



#(1) Simulate data and compute survival function:
SF         = []
for W in WW:
	y      = rft1d.random.randn1d(nResponses, nNodes, W, pad=True)
	sf     = np.array(  [ (y.max(axis=1)>h).mean()  for h in heights]  )
	SF.append(sf)



#(3) Get expected SF:
calc   = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=WW[0], withBonf=False)
SFE        = []
for W in WW:
	calc.set_fwhm(W)
	sfE    = calc.sf(heights)
	SFE.append(sfE)
#standard normal for comparison:
sfN        = stats.norm.sf(heights)



#(4) Plot results:
pyplot.close('all')
ax         = pyplot.axes([0.15,0.14,0.82,0.84])
colors     = scalar2color(range(len(WW)+2), cmap=cm.PuRd)
for W,sf,sfE,c in zip(WW,SF,SFE,colors[2:]):
	ax.plot(heights, sf,  'o', color=c, markersize=5, label='FWHM = %d%%'%W)
	ax.plot(heights, sfE, '-', color=c)
ax.plot(heights[[0,-1]],[2,2], 'k-', label='Theoretical')
ax.plot(heights, sfN, 'k-', lw=3, label='Standard normal')
ax.text(0.5, -0.15, '$u$', size=20, transform=ax.transAxes, ha='center')
ax.text(-0.17, 0.5, 'P ($z_{\mathrm{max}}$ > $u$)', size=18, transform=ax.transAxes, va='center', rotation=90)
ax.set_ylim(0,0.35)
ax.legend()
pyplot.show()



# pyplot.savefig('fig_valid_gauss1d.pdf')