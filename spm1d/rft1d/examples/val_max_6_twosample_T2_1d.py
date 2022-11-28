
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

def here_hotellingsT2_2samp(yA, yB):
	NA,NB   = float(yA.shape[0]), float(yB.shape[0])
	N       = NA + NB
	mA,mB   = np.matrix(yA.mean(axis=0)), np.matrix(yB.mean(axis=0))
	T2      = []
	for ii,(mmA,mmB) in enumerate(zip(mA,mB)):
		yyA,yyB = np.matrix(yA[:,ii,:]), np.matrix(yB[:,ii,:])
		WA,WB   = np.cov(yyA.T), np.cov(yyB.T)
		W       = ((NA-1)*WA + (NB-1)*WB) / (N-2)
		t2      = (NA*NB)/float(NA+NB)  * (mmB-mmA) * np.linalg.inv(W) * (mmB-mmA).T
		T2.append(  float(t2)  )
	return np.asarray(T2)




#(0) Set parameters:
np.random.seed(123456789)
nResponsesA = 15
nResponsesB = 15
nComponents = 2
nIterations = 50   #1000 or bigger for convergence
nNodes      = 101
FWHM        = 15.0
W0          = np.eye(nComponents)
### derived parameters:
nTotal      = nResponsesA + nResponsesB
df          = nComponents, nTotal-2


#(1) Generate Gaussian 1D fields, compute test stat, store field maximum:
T2          = []
generatorA  = rft1d.random.GeneratorMulti1D(nResponsesA, nNodes, nComponents, FWHM, W0)
generatorB  = rft1d.random.GeneratorMulti1D(nResponsesB, nNodes, nComponents, FWHM, W0)
for i in range(nIterations):
	yA      = generatorA.generate_sample()
	yB      = generatorA.generate_sample()
	t2      = here_hotellingsT2_2samp(yA, yB)
	T2.append(  t2.max()  )
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
ax.set_title("Two-sample Hotelling's T2 validation (1D)", size=20)
pyplot.show()

