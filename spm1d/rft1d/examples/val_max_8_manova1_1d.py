
from math import log
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d



def here_manova1_single_node(Y, GROUP):
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

def here_manova1(Y, GROUP):
	nNodes  = Y.shape[1]
	X2      = [here_manova1_single_node(Y[:,i,:], GROUP)  for i in range(nNodes)]
	return np.array(X2)

def here_get_groups(nResponses):
	GROUP      = []
	for i,n in enumerate(nResponses):
		GROUP += [i]*n
	return np.array(GROUP)





#(0) Set parameters:
np.random.seed(123456789)
nResponses  = 40,20,10
nNodes      = 101
nComponents = 2
FWHM        = 15.0
W0          = np.eye(nComponents)
nIterations = 200
### derived parameters:
GROUP       = here_get_groups(nResponses)
nGroups     = len(nResponses)
nTotal      = sum(nResponses)
df          = nComponents * (nGroups-1)


#(1) Generate Gaussian 1D fields, compute test stat, store field maximum:
X2          = []
generator   = rft1d.random.GeneratorMulti1D(nTotal, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
	y       = generator.generate_sample()
	chi2    = here_manova1(y, GROUP)
	X2.append( chi2.max()  )
X2          = np.asarray(X2)


#(2) Compute survival function (SF) for the field maximumimum:
heights     = np.linspace(10, 18, 21)
sf          = np.array(  [ (X2>h).mean()  for h in heights]  )
sfE         = rft1d.chi2.sf(heights, df, nNodes, FWHM)  #theoretical
sf0D        = rft1d.chi2.sf0d(heights, df) #theoretical (0D)


#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sf0D, 'r-', label='Theoretical (0D)')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (\chi^2_\mathrm{max} > u)$', size=20)
ax.legend()
ax.set_title("MANOVA validation (1D)", size=20)
pyplot.show()


