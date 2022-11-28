
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d




#(0) Set parameters:
np.random.seed(0)
nTestStatFields = 3
nNodes          = 101
nIterations     = 10000
FWHM            = 10.0
### initialize RFT calculator:
rftcalc         = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHM, n=nTestStatFields)




#(1) Generate Gaussian 1D fields, compute test stat:
generator       = rft1d.random.Generator1D(nTestStatFields, nNodes, FWHM)
Zmax            = []
for i in range(nIterations):
	y           = generator.generate_sample()
	Zconj       = y.min(axis=0)
	Zmax.append(  Zconj.max()  )
Zmax            = np.array(Zmax)



#(2) Survival functions:
heights     = np.linspace(0.5, 2, 21)
sf          = np.array(  [ (Zmax>h).mean()  for h in heights]  )
sfE         = rftcalc.sf(heights)  #theoretical



#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
ax.plot(heights, sf,   'o',  label='Simulated')
ax.plot(heights, sfE,  '-',  label='Theoretical')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P(z_\mathrm{conj} > u)$', size=20)
ax.legend()
ax.set_title('Conjunction validation (Gaussian fields)', size=20)
pyplot.show()
