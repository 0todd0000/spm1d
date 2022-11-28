
from math import sqrt,log
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d


eps            = np.finfo(float).eps


def here_cca_single_node(y, x):
	N          = y.shape[0]
	X,Y        = np.matrix(x.T).T, np.matrix(y)
	Z          = np.matrix(np.ones(N)).T
	Rz         = np.eye(N) - Z*np.linalg.inv(Z.T*Z)*Z.T
	XStar      = Rz * X
	YStar      = Rz * Y
	p,r        = 1.0, 1.0   #nContrasts, nNuisanceFactors
	m          = N - p - r
	H          = YStar.T * XStar  *  np.linalg.inv( XStar.T * XStar  )  * XStar.T * YStar / p
	W          = YStar.T  * (np.eye(nResponses)  -  XStar*np.linalg.inv(XStar.T*XStar)*XStar.T) * YStar  / m
	#estimate maximum canonical correlation:
	F          = np.linalg.inv(W)*H
	ff         = np.linalg.eigvals(  F  )
	fmax       = float( np.real(ff.max()) )
	r2max      = fmax * p  / (m + fmax*p)
	rmax       = sqrt(r2max)
	### compute test statistic:
	p,m        = float(N), float(y.shape[1])
	x2         = -(p-1-0.5*(m+2)) * log(  (1-rmax**2) )
	return x2


def here_cca(y, x):
	Q  = y.shape[1]
	z  = [here_cca_single_node(y[:,q,:], x)   for q in range(Q)]
	return np.array(z)



#(0) Set parameters:
np.random.seed(0)
nResponses   = 30
nComponents  = 2
nNodes       = 101
nIterations  = 500   #this should be 1000 or larger
FWHM         = 10.0
W0           = np.eye(nComponents)
interp       = True
wrap         = True
heights      = [8, 10, 12, 14]
### derived parameters:
df          = nComponents
x           = np.linspace(0, 1, nResponses) #independent variable
### initialize RFT calculators:
calc         = rft1d.geom.ClusterMetricCalculator()
rftcalc      = rft1d.prob.RFTCalculator(STAT='X2', df=(1,df), nodes=nNodes, FWHM=FWHM)



#(1) Generate Gaussian 1D fields, compute test stat:
X2          = []
generator   = rft1d.random.GeneratorMulti1D(nResponses, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
	y       = generator.generate_sample()
	chi2    = here_cca(y, x)
	X2.append( chi2  )
X2          = np.asarray(X2)


#(2) Maximum region size:
K0      = np.linspace(eps, 12, 21)
K       = np.array([[calc.max_cluster_extent(yy, h, interp, wrap)   for yy in X2]  for h in heights])
P       = np.array([(K>=k0).mean(axis=1)  for k0 in K0]).T
P0      = np.array([[rftcalc.p.cluster(k0, h)  for k0 in K0/FWHM]  for h in heights])




#(3) Plot results:
pyplot.close('all')
colors  = ['b', 'g', 'r', 'orange']
labels  = ['u = %.1f'%h for h in heights]
ax      = pyplot.axes()
for color,p,p0,label in zip(colors,P,P0,labels):
	ax.plot(K0, p,  'o', color=color)
	ax.plot(K0, p0, '-', color=color, label=label)
ax.plot([0,1],[10,10], 'k-', label='Theoretical')
ax.plot([0,1],[10,10], 'ko-', label='Simulated')
ax.set_xlabel('x', size=16)
ax.set_ylabel('P(k_max) > x', size=16)
ax.set_ylim(0, 0.30)
ax.legend()
ax.set_title('Upcrossing extent validations ($\chi^2$ fields)', size=20)
pyplot.show()
