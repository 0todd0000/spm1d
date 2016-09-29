
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d



#(0) Set parameters:
np.random.seed(123456789)
nResponses = 10000
nNodes     = 101
FWHM       = 10.0


#(1) Generate Gaussian 1D fields and extract maxima:
y          = rft1d.randn1d(nResponses, nNodes, FWHM)
ymax       = y.max(axis=1)


#(2) Survival functions for field maximum:
heights    = np.linspace(2, 4, 21)
sf         = np.array(  [ (ymax>h).mean()  for h in heights]  )
sfE        = rft1d.norm.sf(heights, nNodes, FWHM)  #theoretical
sfN        = rft1d.norm.sf0d(heights) #theoretical (0D)

#(3) Plot results:
pyplot.close('all')
ax         = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sfN, 'r-', label='Standard normal')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (z_\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Gaussian univariate validation (1D)', size=20)
pyplot.show()
