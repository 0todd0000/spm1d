
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

eps           = np.finfo(float).eps

def here_anova1(Y, X, X0, Xi, X0i, df):
	Y         = np.matrix(Y)
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
	return F

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
nResponses      = 9,8,9
nNodes          = 101
nIterations     = 2000
FWHM            = 8.0
### derived parameters:
nGroups         = len(nResponses)
nTotal          = sum(nResponses)
df              = nGroups-1, nTotal-nGroups
X,X0,Xi,X0i     = here_design_matrices(nResponses, nGroups)
### generate a field mask:
nodes           = np.array([True]*nNodes) #nothing masked out
nodes[10:25]    = False  #this region will be masked out
nodes[60:85]    = False




#(1) Generate Gaussian 1D fields, compute test stat:
generator   = rft1d.random.Generator1D(nTotal, nodes, FWHM)
F           = []
for i in range(nIterations):
	y       = generator.generate_sample()
	f       = here_anova1(y, X, X0, Xi, X0i, df)
	F.append( np.nanmax(f) )
F           = np.array(F)




#(2) Survival functions for field maximum:
heights    = np.linspace(2.0, 8, 21)
sf         = np.array(  [ (F>=h).mean()  for h in heights]  )
sfE_full   = rft1d.f.sf(heights, df, nNodes, FWHM)  #theoretical (full)
sfE_broken = rft1d.f.sf(heights, df, nodes, FWHM)   #theoretical (broken)



#(3) Plot results:
pyplot.close('all')
ax         = pyplot.axes()
ax.plot(heights, sfE_full,   'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf,         'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (F_\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation (F)', size=20)
pyplot.show()

