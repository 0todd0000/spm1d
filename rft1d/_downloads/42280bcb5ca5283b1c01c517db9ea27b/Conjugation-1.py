import numpy as np
from matplotlib import pyplot
import rft1d




#(0) Set parameters:
np.random.seed(0)
nResponses      = 12
nTestStatFields = 2
nNodes          = 101
nIterations     = 2000
FWHM            = 10.0
### derived parameters:
df              = nResponses-1
sqrtN           = np.sqrt(nResponses)
### initialize RFT calculator:
rftcalc         = rft1d.prob.RFTCalculator(STAT='T', df=(1,df), nodes=nNodes, FWHM=FWHM, n=nTestStatFields)



#(1) Generate Gaussian 1D fields, compute test stat:
generator       = rft1d.random.Generator1D(nResponses, nNodes, FWHM)
Tmax            = []
for i in range(nIterations):
        T           = []
        for i in range(nTestStatFields):
                y       = generator.generate_sample()
                t       = y.mean(axis=0) / y.std(ddof=1, axis=0) * sqrtN
                T.append( t )
        Tconj       = np.min(T, axis=0)  #minimum across the test stat fields
        Tmax.append(  Tconj.max()  )
Tmax            = np.array(Tmax)



#(2) Survival functions:
heights     = np.linspace(1, 3, 21)
sf          = np.array(  [ (Tmax>h).mean()  for h in heights]  )
sfE         = rftcalc.sf(heights)  #theoretical



#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
name        = 'Times New Roman'
ax.plot(heights, sf,   'o',  label='Simulated')
ax.plot(heights, sfE,  '-',  label='Theoretical')
ax.set_xlabel(r'$u$', size=20, usetex=True)
ax.set_ylabel(r'$P(t_\mathrm{conj} > u)$', size=20, usetex=True)
leg = ax.legend()
pyplot.setp( leg.get_texts(), name=name)
ax.set_title('Conjunction validation (t fields)', size=20, name=name)
pyplot.show()