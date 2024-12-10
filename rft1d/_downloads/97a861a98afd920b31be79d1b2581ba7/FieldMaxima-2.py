import numpy as np
from matplotlib import pyplot
import rft1d

np.random.seed(123456789)
nResponses = 2000
nNodes     = 101
u          = 2.7
FWHM       = np.linspace(5, 25, 11)

#(1) Generate Gaussian 1D fields and extract maxima:
SF         = []
for w in FWHM:
        y      = rft1d.randn1d(nResponses, nNodes, w, pad=True)
        ymax   = y.max(axis=1)
        SF.append(  (ymax>u).mean()  )

#(2) Expected survival functions:
FWHMi      = np.linspace(min(FWHM), max(FWHM), 51)
sfE        = [rft1d.norm.sf(u, nNodes, w)  for w in FWHMi]

#(3) Plot results:
pyplot.close('all')
name       = 'Times New Roman'
ax         = pyplot.axes()
ax.plot(FWHM, SF, 'bo', label='Simulated')
ax.plot(FWHMi, sfE, 'b-', label='Theoretical')
ax.set_xlabel(r'$FWHM$', size=20, name=name, usetex=True)
ax.set_ylabel('$P (z_\mathrm{max} > %.3f)$'%u, size=20, name=name, usetex=True)
leg = ax.legend()
pyplot.setp( leg.get_texts(), name=name )
ax.set_title('Survival function validation (Gaussian)', size=20, name=name)
pyplot.show()