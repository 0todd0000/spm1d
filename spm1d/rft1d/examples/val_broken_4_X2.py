
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
	b  = np.any(np.isnan(y), axis=0)[:,0]
	z  = []
	for q in range(Q):
		yy  = y[:,q,:]
		if np.any(np.isnan(yy)):
			z.append(0)
		else:
			z.append(   here_cca_single_node(yy, x)  )
	return np.array(z)




#(0) Set parameters:
np.random.seed(0)
nResponses      = 25
nComponents     = 2
nNodes          = 101
nIterations     = 500  #set this to a large number for convergence
FWHM            = 8.0
W0              = np.eye(nComponents)
### derived parameters:
df              = nComponents
x               = np.linspace(0, 1, nResponses) #independent variable
### generate a field mask:
nodes           = np.array([True]*nNodes) #nothing masked out
nodes[10:30]    = False  #this region will be masked out
nodes[60:85]    = False




#(1) Generate Gaussian 1D fields, compute test stat:
generator   = rft1d.random.GeneratorMulti1D(nResponses, nodes, nComponents, FWHM, W0)
X2          = []
for i in range(nIterations):
	y       = generator.generate_sample()
	x2      = here_cca(y, x)
	X2.append( np.nanmax(x2) )
X2          = np.array(X2)




#(2) Survival functions for field maximum:
heights    = np.linspace(8.0, 15, 21)
sf         = np.array(  [ (X2>=h).mean()  for h in heights]  )
sfE_full   = rft1d.chi2.sf(heights, df, nNodes, FWHM)  #theoretical (full)
sfE_broken = rft1d.chi2.sf(heights, df, nodes, FWHM)   #theoretical (broken)



#(3) Plot results:
pyplot.close('all')
ax         = pyplot.axes()
ax.plot(heights, sfE_full,   'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf,         'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (\chi^2_\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation ($\chi^2$)', size=20)
pyplot.show()

