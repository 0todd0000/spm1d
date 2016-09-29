
from math import sqrt,log
import numpy as np
from scipy import stats
from matplotlib import pyplot



def here_cca(y, x):
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




#(0) Set parameters:
np.random.seed(0)
nResponses  = 20
nComponents = 3
nIterations = 1000
W0          = np.eye(nComponents)
### derived parameters:
df          = nComponents
x           = np.linspace(0, 1, nResponses) #independent variable


#(1) Generate Gaussian data and compute test statistic:
X2          = []
for i in range(nIterations):
	y       = np.random.multivariate_normal(np.zeros(nComponents), W0, nResponses)
	chi2    = here_cca(y, x)
	X2.append( chi2 )
X2          = np.asarray(X2)


#(2) Survival functions:
heights     = np.linspace(3, 12, 21)
sf          = np.array(  [ (X2>h).mean()  for h in heights]  )
sfE         = stats.chi2.sf(heights, df)


#(3) Plot results:
pyplot.close('all')
ax            = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (\chi^2 > u)$', size=20)
ax.legend()
ax.set_title("CCA validation (0D)", size=20)
pyplot.show()

