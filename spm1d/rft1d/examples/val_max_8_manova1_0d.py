
from math import log
import numpy as np
from scipy import stats
from matplotlib import pyplot


def here_manova1(Y, GROUP):
	### assemble counts:
	u           = np.unique(GROUP)
	nGroups     = u.size
	nResponses  = Y.shape[0]
	nComponents = Y.shape[1]
	### create design matrix:
	X           = np.zeros((nResponses, nGroups))
	ind0        = 0
	for i,uu in enumerate(u):
		n       = (GROUP==uu).sum()
		X[ind0:ind0+n, i] = 1
		ind0   += n
	### SS for original design:
	Y,X   = np.matrix(Y), np.matrix(X)
	b     = np.linalg.pinv(X)*Y
	R     = Y - X*b
	R     = R.T*R
	### SS for reduced design:
	X0    = np.matrix(  np.ones(Y.shape[0])  ).T
	b0    = np.linalg.pinv(X0)*Y
	R0    = Y - X0*b0
	R0    = R0.T*R0
	### Wilk's lambda:
	lam   = np.linalg.det(R) / np.linalg.det(R0)
	### test statistic:
	N,p,k = float(nResponses), float(nComponents), float(nGroups)
	x2    = -((N-1) - 0.5*(p+k)) * log(lam)
	return x2

def here_get_groups(nResponses):
	GROUP      = []
	for i,n in enumerate(nResponses):
		GROUP += [i]*n
	return np.array(GROUP)



#(0) Set parameters:
np.random.seed(1)
nResponses  = 10,3,4
nComponents = 3
nGroups     = len(nResponses)
nIterations = 5000
W0          = np.eye(nComponents)
### derived parameters:
GROUP       = here_get_groups(nResponses)
nTotal      = sum(nResponses)
df          = nComponents * (nGroups-1)


#(1) Generate random data and compute test statistic:
X2          = []
for i in range(nIterations):
	y       = np.random.multivariate_normal(np.zeros(nComponents), W0, nTotal)
	chi2    = here_manova1(y, GROUP)
	X2.append( chi2 )
X2          = np.asarray(X2)


#(2) Survival functions:
heights     = np.linspace(5, 15, 21)
sf          = np.array(  [ (X2>h).mean()  for h in heights]  )
sfE         = stats.chi2.sf(heights, df)


#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (\chi^2 > u)$', size=20)
ax.legend()
ax.set_title("MANOVA validation (0D)", size=20)
pyplot.show()

