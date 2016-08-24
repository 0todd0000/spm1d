
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
nResponses      = 25
nTestStatFields = 2
nComponents     = 2
nNodes          = 101
nIterations     = 100  #set this to a large number for convergence
FWHM            = 8.0
W0              = np.eye(nComponents)
### derived parameters:
df              = nComponents
x               = np.linspace(0, 1, nResponses) #independent variable
### initialize RFT calculator:
rftcalc         = rft1d.prob.RFTCalculator(STAT='X2', df=(1,df), nodes=nNodes, FWHM=FWHM, n=nTestStatFields)




#(1) Generate Gaussian 1D fields, compute test stat:
X2max       = []
generator   = rft1d.random.GeneratorMulti1D(nResponses, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
	X2      = []
	for i in range(nTestStatFields):
		y   = generator.generate_sample()
		x2  = here_cca(y, x)
		X2.append( x2  )
	X2conj  = np.min(X2, axis=0)  #minimum across the test stat fields
	X2max.append(  X2conj.max()  )
X2max       = np.array(X2max)




#(2) Survival functions:
heights     = np.linspace(5, 10, 21)
sf          = np.array(  [ (X2max>h).mean()  for h in heights]  )
sfE         = rftcalc.sf(heights)  #theoretical



#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
ax.plot(heights, sf,   'o',  label='Simulated')
ax.plot(heights, sfE,  '-',  label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P(\chi^2_\mathrm{conj} > u)$', size=20)
ax.legend()
ax.set_title('Conjunction validation ($\chi^2$ fields)', size=20)
pyplot.show()
