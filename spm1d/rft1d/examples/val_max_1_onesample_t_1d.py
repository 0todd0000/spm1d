
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d



#(0) Set parameters:
np.random.seed(123456789)
nResponses  = 8
nIterations = 2000
nNodes      = 101
FWHM        = 10.0
### derived parameters:
df          = nResponses-1
sqrtN       = np.sqrt(nResponses)


#(1) Generate Gaussian 1D fields, compute test stat, store field maximum:
T           = []
generator   = rft1d.random.Generator1D(nResponses, nNodes, FWHM)
for i in range(nIterations):
	y       = generator.generate_sample()
	t       = y.mean(axis=0) / y.std(ddof=1, axis=0) * sqrtN
	T.append( t.max() )
T           = np.asarray(T)


#(2) Survival functions:
heights     = np.linspace(2, 5, 21)
sf          = np.array(  [ (T>h).mean()  for h in heights]  )
sfE         = rft1d.t.sf(heights, df, nNodes, FWHM)  #theoretical
sf0D        = rft1d.t.sf0d(heights, df) #theoretical (0D)


#(3) Plot results:
pyplot.close('all')
ax          = pyplot.axes()
ax.plot(heights, sf,   'o',  label='Simulated')
ax.plot(heights, sfE,  '-',  label='Theoretical')
ax.plot(heights, sf0D, 'r-', label='Theoretical (0D)')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (t_\mathrm{max} > u)$', size=20)
ax.legend()
ax.set_title('One-sample t validation (1D)', size=20)
pyplot.show()
