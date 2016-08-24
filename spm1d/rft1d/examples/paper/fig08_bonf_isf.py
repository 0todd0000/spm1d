
import numpy as np
from scipy import stats,optimize
from matplotlib import pyplot,cm
from spm1d import rft1d




### EPS production preliminaries:
fig_width_mm  = 100
fig_height_mm = 80
mm2in = 1/25.4
fig_width  = fig_width_mm*mm2in  	# width in inches
fig_height = fig_height_mm*mm2in    # height in inches
params = {	'backend':'ps', 'axes.labelsize':14,
			'font.size':12, 'text.usetex': False, 'legend.fontsize':12,
			'xtick.labelsize':8, 'ytick.labelsize':8,
			'font.family':u'Times New Roman',  #Times
			'lines.linewidth':0.5,
			'patch.linewidth':0.25,
			'figure.figsize': [fig_width,fig_height]}
pyplot.rcParams.update(params)





#(0) Set parameters:
nNodes     = 101
FWHMs      = np.linspace(1, 5, 11)
ALPHAs     = [0.001, 0.01, 0.05, 0.1]


#(1) Inverse survival function (Bonferroni):
ISFbonf    = []
for alpha in ALPHAs:
	objfn  = lambda x: (rft1d.prob.p_bonferroni('Z', x, None, nNodes) - alpha)**2
	x0     = 5.0
	ustar  = optimize.fmin(objfn, 5, disp=0)
	ISFbonf.append( float(ustar) )


#(2) Inverse survival function (RFT)
rftcalc    = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=10, withBonf=False)
ISF        = []
for W in FWHMs:
	rftcalc.set_fwhm(W)
	ISF.append(  [rftcalc.isf(alpha) for alpha in ALPHAs]  )
ISF        = np.asarray(ISF).T




#(4) Plot results:
pyplot.close('all')
ax         = pyplot.axes([0.12,0.14,0.86,0.84])
colors     = ['b', 'g', 'r', 'orange']
for alpha,isf,isfbonf,color in zip(ALPHAs,ISF,ISFbonf,colors):
	ax.plot(FWHMs, isf, color=color, lw=1)
	ax.plot(FWHMs, [isfbonf]*len(FWHMs), '--', color=color, lw=1)
### label the isoprobabilities:
XY         = [(0.31,0.75), (0.35,0.52), (0.3, 0.35), (0.1, (0.15))]
for xy,alpha,color in zip(XY,ALPHAs,colors):
	ax.text(xy[0], xy[1], r'$\alpha=%.3f$'%alpha, transform=ax.transAxes, color=color)
### create legend:
ax.plot(FWHMs, [100]*len(FWHMs), 'k-', lw=1, label='RFT')
ax.plot(FWHMs, [100]*len(FWHMs), 'k--', lw=1, label='Bonferroni')
ax.legend()
### axis labels:
ax.text(0.5, -0.15, 'FWHM  (%)', size=16, transform=ax.transAxes, ha='center')
ax.text(-0.14, 0.5, '$z^*$', size=20, transform=ax.transAxes, va='center', rotation=90)
ax.set_ylim(2.5, 5)
pyplot.show()


# pyplot.savefig('fig_bonf_B.pdf')