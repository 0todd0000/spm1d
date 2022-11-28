
import numpy as np
from matplotlib import pyplot
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
			'font.family':'Times New Roman',  #Times
			'lines.linewidth':0.5,
			'patch.linewidth':0.25,
			'figure.figsize': [fig_width,fig_height]}
pyplot.rcParams.update(params)




#(0) Set parameters:
np.random.seed(0)
nResponses  = 10
nNodes      = 101
nIterations = 50  #raise this to 500 to reproduce the results from the paper


#(1) Cycle through smoothing kernels:
W           = np.linspace(1, 50, 15) #actual FWHM
We          = [] #estimated FWHM
for w in W:
	we      = []
	# g       = rft1d.random.Generator1D(nResponses, nNodes, w)
	for i in range(nIterations):
		y   = rft1d.random.randn1d(nResponses, nNodes, w)
		# y       = g.generate_sample()
		we.append( rft1d.geom.estimate_fwhm(y) )
	We.append(we)
	print( 'Actual FWHM: %06.3f, estimated FWHM: %06.3f' %(w, np.mean(We[-1])) )
We          = np.array(We)







#(2) Plot results:
pyplot.close('all')
ax   = pyplot.axes([0.11,0.14,0.86,0.84])
ax.plot(W, W,  'k-', lw=2, label='Actual')
ax.errorbar(W, We.mean(axis=1), yerr=We.std(ddof=1, axis=1), fmt='bo', ecolor='b', label='Estimated')
ax.legend(loc='upper left')
ax.set_xlabel('Actual  FWHM  (%)')
ax.set_ylabel('Estimated  FWHM  (%)')
### annotate:
pyplot.setp(ax, xlim=(0,54), ylim=(0,54))
pyplot.show()


# pyplot.savefig('fig_fwhm_estimatation.pdf')
