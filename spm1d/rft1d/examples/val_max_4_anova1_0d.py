
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot

eps           = np.finfo(float).eps

def here_anova1(Y, X, X0, Xi, X0i, df):
	Y         = np.matrix(Y).T
	### estimate parameters:
	b         = Xi*Y
	eij       = Y - X*b
	R         = eij.T*eij
	### reduced design:
	b0        = X0i*Y
	eij0      = Y - X0*b0
	R0        = eij0.T*eij0
	### compute F statistic:
	F         = ((np.diag(R0)-np.diag(R))/df[0]) / (np.diag(R+eps)/df[1])
	return float(F)

def here_design_matrices(nResponses, nGroups):
	nTotal    = sum(nResponses)
	X         = np.zeros((nTotal,nGroups))
	i0        = 0
	for i,n in enumerate(nResponses):
		X[i0:i0+n,i] = 1
		i0   += n
	X         = np.matrix(X)
	X0        = np.matrix(np.ones(nTotal)).T  #reduced design matrix
	Xi,X0i    = np.linalg.pinv(X), np.linalg.pinv(X0) #pseudo-inverses
	return X,X0,Xi,X0i
	




#(0) Set parameters:
np.random.seed(0)
nResponses  = 6,8,5  #responses per group
nIterations = 5000
### derived parameters:
nGroups     = len(nResponses)
nTotal      = sum(nResponses)
df          = nGroups-1, nTotal-nGroups
X,X0,Xi,X0i = here_design_matrices(nResponses, nGroups)


#(1) Generate random data and compute test statistic:
F             = []
for i in range(nIterations):
	y         = np.random.randn(nTotal)
	F.append( here_anova1(y, X, X0, Xi, X0i, df) )
F             = np.asarray(F)


#(2) Survival functions:
heights       = np.linspace(1, 10, 21)
sf            = np.array(  [ (F>h).mean()  for h in heights]  )
sfE           = stats.f.sf(heights, df[0], df[1])


#(3) Plot results:
pyplot.close('all')
ax            = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (F > u)$', size=20)
ax.legend()
ax.set_title('ANOVA validation (0D)', size=20)
pyplot.show()



