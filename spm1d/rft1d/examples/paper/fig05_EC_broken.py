
from math import pi,log,sqrt,exp
import numpy as np
from scipy import stats
from matplotlib import pyplot
from spm1d import rft1d





### EPS production preliminaries:
fig_width_mm  = 100
fig_height_mm = 80
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



### Expected Euler characteristic (EC) densitites
### Reference:  Worsley KJ (1995). Estimating the number of peaks in
###    a random field using the Hadwiger characteristic of excursion sets,
###    with applications to medical images. Annals of Statistics, 640-669.
def here_ec_0d(u, nSegments):   #0D component
	return nSegments * stats.norm.sf(u)
def here_ec_1d(u, fieldSize, FWHM):
	return float(fieldSize)/W * sqrt(4*log(2)) / (2*pi) * exp(-0.5*(u*u))  #1D component
### actual EC:
def here_ec_actual(yy, u):
	y   = yy.copy()
	y[np.isnan(yy)] = -1e9
	b   = y>u
	L,n = rft1d.geom.bwlabel(b)  #actually the Hadwiger characteristic
	return n




#(0) Set parameters:
np.random.seed(0)
nNodes       = 101
FWHM         = [5.0, 10.0, 25.0]
nIterations  = 100   #increase this to 1000 to reproduce the results from the paper
heights      = np.linspace(1.0, 3.0, 11)
### generate mask:
nodes        = np.array([True]*nNodes)
nodes[20:35] = False
nodes[60:80] = False
### assemble the field's geometric characteristics:
nSegments    = rft1d.geom.bwlabel(nodes)[1]  #number of unbroken field segments (here: 3)
nNodesTotal  = nodes.sum() #number of nodes in the field segments
fieldSize    = nNodesTotal - nSegments



#(1) Expected EC:
expectedEC           = []
expectedECunbroken   = []
for W in FWHM:
	EC0,EC0u         = [],[]
	for u in heights:
		ec0          = here_ec_0d(u, nSegments)
		ec1          = here_ec_1d(u, fieldSize, W)
		### expectations for unbroken fields:
		ec0u         = here_ec_0d(u, 1)
		ec1u         = here_ec_1d(u, fieldSize, W)
		EC0.append( ec0 + ec1 )
		EC0u.append( ec0u + ec1u )
	expectedEC.append(EC0)
	expectedECunbroken.append(EC0u)
expectedEC           = np.array(expectedEC)
expectedECunbroken   = np.array(expectedECunbroken)
	


#(2) Simulate broken random fields and compute their EC:
EC          = []
for W in FWHM:
	y       = rft1d.randn1d(nIterations, nodes, W, pad=True)
	ec      = np.array([[here_ec_actual(yy, u)  for u in heights]   for yy in y]).mean(axis=0)
	EC.append(ec)
EC          = np.array(EC)




#(3) Plot results:
pyplot.close('all')
ax      = pyplot.axes([0.11,0.14,0.86,0.84])
colors  = ['b', 'r', 'g']
for color,ec0,ec0u,ec in zip(colors, expectedEC, expectedECunbroken, EC):
	ax.plot(heights, ec0u, '-', lw=1, color=color)    #expectation for an unbroken field
	ax.plot(heights, ec0, ':', lw=2, color=color)  #expectation for broken field
	ax.plot(heights, ec, 'o', color=color, markersize=5)  #simulated data
### add a legend:
ax.plot([0,1],[1000,1000], 'k-', lw=1, label='Unbroken field')
ax.plot([0,1],[1000,1000], 'k:', lw=2, label='Broken field')
ax.plot([0,1],[1000,1000], 'ko', label='Simulated (broken field)', markersize=5)
for color,W in zip(colors,FWHM):
	ax.plot([0,1],[1000,1000], '-', lw=2, color=color, label='FWHM = %d'%W)
ax.set_xlim(heights.min(), heights.max())
ax.set_ylim(0, EC.max())
ax.legend()
### label the axes:
ax.set_xlabel('$u$', size=18)
ax.set_ylabel('Hadwiger characteristic', size=16)
pyplot.show()


# pyplot.savefig('fig_expected_EC_broken.pdf')







