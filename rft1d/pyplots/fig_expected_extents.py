
import numpy as np
from matplotlib import pyplot
import rft1d


### update rcParams:
fig_width_mm  = 140
fig_height_mm = 100
mm2in         = 1/25.4
fig_width     = fig_width_mm*mm2in
fig_height    = fig_height_mm*mm2in
params = {
	'backend':'ps',
	'axes.labelsize':14,
	'font.size':12,
	'text.usetex': False,
	'legend.fontsize':12,
	'xtick.labelsize':8,
	'ytick.labelsize':8,
	'font.family':'Times New Roman',
	'lines.linewidth':0.5,
	'patch.linewidth':0.25,
	'figure.figsize': [fig_width,fig_height]
}
pyplot.rcParams.update(params)



eps        = np.finfo(float).eps   #smallest float


#(0) Specify parameters:
np.random.seed(0)
nResponses   = 5000
nNodes       = 101
FWHM         = 10.0
interp       = True
wrap         = True
heights      = [2.2, 2.4, 2.6, 2.8]
### generate data:
y            = rft1d.randn1d(nResponses, nNodes, FWHM)
calc         = rft1d.geom.ClusterMetricCalculator()
rftcalc      = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHM)




#(1) Maximum region size:
K0      = np.linspace(eps, 15, 21)
K       = np.array([[calc.max_cluster_extent(yy, h, interp, wrap)   for yy in y]  for h in heights])
P       = np.array([(K>=k0).mean(axis=1)  for k0 in K0]).T
P0      = np.array([[rftcalc.p.cluster(k0, h)  for k0 in K0/FWHM]  for h in heights])




#(2) Plot results:
pyplot.close('all')
colors  = ['b', 'g', 'r', 'orange']
labels  = ['$u$ = %.1f'%h for h in heights]
ax      = pyplot.axes([0.12,0.11,0.86,0.80])
for color,p,p0,label in zip(colors,P,P0,labels):
	ax.plot(K0, p,  'o', color=color, markersize=5)
	ax.plot(K0, p0, '-', color=color, label=label)
ax.plot([0,1],[10,10], 'k-', label='Theoretical')
ax.plot([0,1],[10,10], 'ko-', label='Simulated')
ax.legend()
ax.set_xlabel('$x$', size=14)
ax.set_ylabel('$P(k) > x$', size=14)
ax.set_ylim(0, 0.25)
ax.set_title('Upcrossing extent validations (Gaussian fields)', size=16)
# pyplot.show()
