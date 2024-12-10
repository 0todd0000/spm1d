import numpy as np
from matplotlib import pyplot
import rft1d
np.random.seed(0)
nResponses   = 5
nNodes       = 101
FWHM         = 20.0
### create a boolean mask:
nodes        = np.array([True]*nNodes) #nothing masked out
nodes[20:30] = False  #this region will be masked out
nodes[60:80] = False  #this region will be masked out
### generate Gaussian 1D fields:
y          = rft1d.randn1d(nResponses, nodes, FWHM)
### plot:
pyplot.plot(y.T)