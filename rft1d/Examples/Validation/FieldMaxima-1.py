import numpy as np
from matplotlib import pyplot
import rft1d

np.random.seed(123456789)
nResponses = 10000
nNodes     = 101
FWHM       = 10.0

#(1) Generate Gaussian 1D fields and extract maxima:
y          = rft1d.randn1d(nResponses, nNodes, FWHM)
ymax       = y.max(axis=1)

#(2) Survival functions for field maximum:
heights    = np.linspace(2, 4, 21)
sf         = np.array(  [ (ymax>u).mean()  for u in heights]  )
sfE        = rft1d.norm.sf(heights, nNodes, FWHM)  #theoretical
sfN        = rft1d.norm.sf0d(heights) #theoretical (0D)

#(3) Plot results:
pyplot.close('all')
name       = 'Times New Roman'
ax         = pyplot.axes()
ax.plot(heights, sf, 'bo', label='Simulated')
ax.plot(heights, sfE, 'b-', label='Theoretical')
ax.plot(heights, sfN, 'r-', label='Standard normal')
ax.set_xlabel(r'$u$', size=20, usetex=True)
ax.set_ylabel(r'$P (z_\mathrm{max} > u)$', size=20, usetex=True)
leg = ax.legend()
pyplot.setp( leg.get_texts(), name=name )
ax.set_title('Survival function validation (Gaussian)', size=20, name=name)
pyplot.show()