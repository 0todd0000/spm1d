
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
nResponses  = 7,8,9   #number of responses in each group
nNodes      = 101
nIterations = 5000
FWHM        = 10.0
interp      = True
wrap        = True
heights     = [6, 7, 8]
c           = 2
### derived parameters:
nGroups     = len(nResponses)
nTotal      = sum(nResponses)
df          = nGroups-1, nTotal-nGroups
X,X0,Xi,X0i = here_design_matrices(nResponses, nGroups)
### initialize RFT calculators:
calc         = rft1d.geom.ClusterMetricCalculator()
rftcalc      = rft1d.prob.RFTCalculator(STAT='F', df=df, nodes=nNodes, FWHM=FWHM)



#(1) Generate Gaussian 1D fields, compute test stat:
F           = []
generator   = rft1d.random.Generator1D(nTotal, nNodes, FWHM)
for i in range(nIterations):
	y       = generator.generate_sample()
	f       = here_anova1(y, X, X0, Xi, X0i, df)
	F.append( f )
F           = np.asarray(F)



#(2) Maximum region size:
K0      = np.linspace(eps, 8, 21)
K       = [[calc.cluster_extents(yy, h, interp, wrap)   for yy in F]  for h in heights]
### compute number of upcrossings above a threshold:
C       = np.array([[[  sum([kkk>=k0 for kkk in kk])  for kk in k]  for k in K]   for k0 in K0])
P       = np.mean(C>=c, axis=2).T
P0      = np.array([[rftcalc.p.set(c, k0, h)  for h in heights]  for k0 in K0/FWHM]).T




#(3) Plot results:
pyplot.close('all')
colors  = ['b', 'g', 'r']
ax      = pyplot.axes()
for color,p,p0,u in zip(colors,P,P0,heights):
	ax.plot(K0, p,  'o', color=color)
	ax.plot(K0, p0, '-', color=color, label='u = %.1f'%u)
ax.set_xlabel('x', size=16)
ax.set_ylabel('P(c, k_min) > x', size=16)
ax.legend()
ax.set_title('Set-level inference validations (F fields)', size=20)
pyplot.show()
