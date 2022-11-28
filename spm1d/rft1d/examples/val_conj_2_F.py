
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
nTestStatFields = 3
nNodes          = 101
nIterations     = 2000
FWHM            = 8.0
### derived parameters:
nGroups         = len(nResponses)
nTotal          = sum(nResponses)
df              = nGroups-1, nTotal-nGroups
X,X0,Xi,X0i     = here_design_matrices(nResponses, nGroups)
### initialize RFT calculator:
rftcalc         = rft1d.prob.RFTCalculator(STAT='F', df=df, nodes=nNodes, FWHM=FWHM, n=nTestStatFields)




#(1) Generate Gaussian 1D fields, compute test stat:
Fmax        = []
generator   = rft1d.random.Generator1D(nTotal, nNodes, FWHM)
for i in range(nIterations):
	F       = []
	for i in range(nTestStatFields):
		y   = generator.generate_sample()
		f   = here_anova1(y, X, X0, Xi, X0i, df)
		F.append( f )
	Fconj   = np.min(F, axis=0)  #minimum across the test stat fields
	Fmax.append(  Fconj.max()  )
Fmax        = np.array(Fmax)
	


#(2) Survival functions:
heights     = np.linspace(2, 5, 21)
sf          = np.array(  [ (Fmax>h).mean()  for h in heights]  )
sfE         = rftcalc.sf(heights)  #theoretical



#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
ax.plot(heights, sf,   'o',  label='Simulated')
ax.plot(heights, sfE,  '-',  label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P(F_\mathrm{conj} > u)$', size=20)
ax.legend()
ax.set_title('Conjunction validation (F fields)', size=20)
pyplot.show()
