
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d




#(0) Set parameters:
np.random.seed(1)
nResponses  = 8
nComponents = 2
nIterations = 5000  #approximately 20000 iterations required for convergence
W0          = np.array([[1,0.2],[0.2,1]]) #covariance
### derived parameters:
df          = nComponents, nResponses-1   #p,m


#(1) Generate random data and compute test statistic:
T2          = []
for i in range(nIterations):
	y       = np.random.multivariate_normal(np.zeros(nComponents), W0, nResponses)
	y       = np.matrix(y)
	m       = y.mean(axis=0)  #estimated mean
	W       = np.matrix( np.cov(y.T, ddof=1) )  #estimated covariance
	t2      = nResponses * m * np.linalg.inv(W) * m.T
	T2.append(float(t2))
T2          = np.asarray(T2)


#(2) Survival functions:
heights     = np.linspace(2, 10, 21)
sf          = np.array(  [ (T2>h).mean()  for h in heights]  )
sfE         = rft1d.T2.sf0d(heights, df)


#(3) Plot results:
pyplot.close('all')
ax            = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (T^2 > u)$', size=20)
ax.legend()
ax.set_title("One-sample Hotelling's T2 validation (0D)", size=20)
pyplot.show()

