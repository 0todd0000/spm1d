
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d


def here_hotellingsT2(y):
	N       = y.shape[0]
	m       = np.matrix(  y.mean(axis=0) )
	T2      = []
	for ii,mm in enumerate(m):
		W   = np.matrix( np.cov(y[:,ii,:].T, ddof=1) )  #estimated covariance
		t2  = N * mm * np.linalg.inv(W) * mm.T
		T2.append(  float(t2)  )
	return np.asarray(T2)




#(0) Set parameters:
np.random.seed(123456789)
nResponses  = 20
nNodes      = 101
nComponents = 3
nIterations = 50   #1000 or bigger for convergence
FWHM        = 15.0
W0          = np.eye(nComponents)
### derived parameters:
df          = nComponents, nResponses-1   #p,m


#(1) Generate Gaussian 1D fields, compute test stat, store field maximum:
T2          = []
generator   = rft1d.random.GeneratorMulti1D(nResponses, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
	y       = generator.generate_sample()
	t2      = here_hotellingsT2(y)
	T2.append( t2.max() )
T2          = np.asarray(T2)


#(2) Compute survival function (SF) for the field maximumimum:
heights     = np.linspace(10, 40, 21)
sf          = np.array(  [ (T2>h).mean()  for h in heights]  )
sfE         = rft1d.T2.sf(heights, df, nNodes, FWHM)  #theoretical
sf0D        = rft1d.T2.sf0d(heights, df) #theoretical (0D)


#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sf0D, 'r-', label='Theoretical (0D)')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (T^2_\mathrm{max} > u)$', size=20)
ax.legend()
ax.set_title("One-sample Hotelling's T2 validation (1D)", size=20)
pyplot.show()
