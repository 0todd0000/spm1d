
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot



def tstat_regress(Y, x):
	Y      = np.array([Y]).T
	X      = np.ones((Y.shape[0],2))
	X[:,0] = x
	### assemble data:
	Y      = np.matrix(Y)
	X      = np.matrix(X)
	c      = np.matrix([1,0]).T
	### solve:
	b      = np.linalg.pinv(X)*Y            #parameters
	eij    = Y - X*b                        #residuals
	R      = eij.T*eij                      #residuals sum of squares
	df     = Y.shape[0] - 2                 #degrees of freedom
	sigma2 = np.diag(R)/df                  #variance
	### compute t statistic
	return np.array(c.T*b).flatten()  /   np.sqrt(sigma2*float(c.T*(np.linalg.inv(X.T*X))*c))




#(0) Set parameters:
np.random.seed(0)
nResponses  = 10
nIterations = 5000
### derived parameters:
x           = np.arange(nResponses)  #independent variable
df          = nResponses - 2


#(1) Generate random data and compute test statistic:
T           = []
for i in range(nIterations):
	y       = np.random.randn(nResponses)
	t       = tstat_regress(y, x)
	T.append(t)
T           = np.asarray(T)


#(2) Survival functions:
heights     = np.linspace(1, 4, 21)
sf          = np.array(  [ (T>h).mean()  for h in heights]  )
sfE         = stats.t.sf(heights, df) #theoretical
sfN         = stats.norm.sf(heights)  #standard normal (for comparison)


#(3) Plot results:
pyplot.close('all')
ax            = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sfN, 'r-', label='Standard normal')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (t > u)$', size=20)
ax.legend()
ax.set_title('Linear regression validation (0D)', size=20)
pyplot.show()



