
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d



eps        = np.finfo(float).eps   #smallest float



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
nResponses   = 500  #raise to 50000 to reproduce the results from the paper
nNodes       = 101
FWHM         = 8.5
interp       = True
wrap         = True
heights      = [2.0, 2.2, 2.4]
c            = 2
### generate data:
y            = rft1d.randn1d(nResponses, nNodes, FWHM)
calc         = rft1d.geom.ClusterMetricCalculator()
rftcalc      = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHM)




#(1) Maximum region size:
K0      = np.linspace(eps, 8, 21)
K       = [[calc.cluster_extents(yy, h, interp, wrap)   for yy in y]  for h in heights]
### compute number of upcrossings above a threshold:
C       = np.array([[[  sum([kkk>=k0 for kkk in kk])  for kk in k]  for k in K]   for k0 in K0])
P       = np.mean(C>=c, axis=2).T
P0      = np.array([[rftcalc.p.set(c, k0, h)  for h in heights]  for k0 in K0/FWHM]).T




#(2) Plot results:
pyplot.close('all')
colors  = ['b', 'g', 'r']
ax      = pyplot.axes([0.17,0.14,0.80,0.84])
for color,p,p0,u in zip(colors,P,P0,heights):
	ax.plot(K0, p,  'o', color=color, markersize=5)
	ax.plot(K0, p0, '-', color=color, label='$u$ = %.1f'%u)
### legend:
ax.plot([0,1],[10,10], 'k-', label='Theoretical')
ax.plot([0,1],[10,10], 'ko-', label='Simulated', markersize=5)
ax.legend()
### axis labels:
ax.set_xlabel('$k_\mathrm{min}$', size=16)
ax.set_ylabel('$P(c | k_\mathrm{min}) >= 2$', size=16)
ax.set_ylim(0, 0.08)
pyplot.show()


# pyplot.savefig('fig_valid_gauss1d_set.pdf')