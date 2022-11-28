
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d




#(0) Set parameters:
np.random.seed(0)
nResponses    = 10000
nNodes        = 101
FWHM          = 13.1877
### generate a field mask:
nodes_full    = np.array([True]*nNodes) #nothing masked out
nodes         = nodes_full.copy()
nodes[20:45]  = False  #this region will be masked out
nodes[60:80]  = False



#(1) Generate Gaussian 1D fields and extract maxima::
y_full        = rft1d.randn1d(nResponses, nNodes, FWHM)
np.random.seed(0)
y_broken      = rft1d.randn1d(nResponses, nodes, FWHM)
ymax_full     = y_full.max(axis=1)
ymax_broken   = np.nanmax(y_broken, axis=1)


#(2) Survival functions for field maximum:
heights    = np.linspace(2.0, 4, 21)
sf_full    = np.array(  [ (ymax_full>=h).mean()  for h in heights]  )
sf_broken  = np.array(  [ (ymax_broken>=h).mean()  for h in heights]  )
### expected:
sfE_full   = rft1d.norm.sf(heights, nNodes, FWHM)  #theoretical
sfE_broken = rft1d.norm.sf(heights, nodes, FWHM)  #theoretical


#(3) Plot results:
pyplot.close('all')
ax         = pyplot.axes()
ax.plot(heights, sfE_full,   'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf_full,    'bo', label='Simulated (full)')
ax.plot(heights, sf_broken,  'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (z_\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation (Gaussian)', size=20)
pyplot.show()

