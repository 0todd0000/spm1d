
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d


def tstat_regress(Y, x):
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
	t = np.array(c.T*b).flatten()  /   np.sqrt(sigma2*float(c.T*(np.linalg.inv(X.T*X))*c))
	return t




#(0) Set parameters:
np.random.seed(123456789)
nResponses    = 12
nIterations   = 2000
nNodes        = 101
FWHM          = 10.0
### derived parameters:
x             = np.arange(nResponses)  #independent variable
df            = nResponses - 2


#(1) Generate Gaussian 1D fields, compute test stat, store field maximum:
T           = []
generator   = rft1d.random.Generator1D(nResponses, nNodes, FWHM)
for i in range(nIterations):
	y       = generator.generate_sample()
	t       = tstat_regress(y, x)
	T.append( t.max() )
T           = np.asarray(T)


#(2) Survival functions:
heights   = np.linspace(2, 5, 21)
sf        = np.array(  [ (T>h).mean()  for h in heights]  )
sfE       = rft1d.t.sf(heights, df, nNodes, FWHM)  #theoretical
sf0D      = rft1d.t.sf0d(heights, df) #theoretical (0D)


#(3) Plot results:
pyplot.close('all')
ax        = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sf0D, 'r-', label='Theoretical (0D)')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (t_\mathrm{max} > u)$', size=20)
ax.legend()
ax.set_title('Linear regression validation (1D)', size=20)
pyplot.show()

