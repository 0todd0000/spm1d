
import numpy as np
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
nNodes     = 101
FWHMs         = [1, 2, 3]
heights    = np.linspace(2.5, 4.0, 21)



#(1) RFT survival function:
rftcalc    = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHMs[0], withBonf=False)
SFE        = []
for W in FWHMs:
	rftcalc.set_fwhm(W)
	sfE    = rftcalc.p.upcrossing(heights)
	SFE.append(sfE)
#Bonferroni-corrected survival function:
sfB        = [rft1d.prob.p_bonferroni('Z', u, None, nNodes)  for u in heights]



#(2) Plot results:
pyplot.close('all')
ax         = pyplot.axes([0.15,0.14,0.82,0.84])
colors     = scalar2color(range(len(FWHMs)+2), cmap=cm.PuRd)
for W,sfE,c in zip(FWHMs,SFE,colors[2:]):
	ax.plot(heights, sfE, '-', lw=2, color=c, label='FWHM = %d%%'%W)
ax.plot(heights, sfB, 'k--', lw=4, label='Bonferroni')
ax.text(0.5, -0.15, '$u$', size=20, transform=ax.transAxes, ha='center')
ax.text(-0.17, 0.5, 'P ($z_{\mathrm{max}}$ > $u$)', size=18, transform=ax.transAxes, va='center', rotation=90)
ax.set_xlim(2.7,3.6)
ax.set_ylim(0,0.30)
ax.legend()
pyplot.show()



# pyplot.savefig('fig_bonf_A.pdf')