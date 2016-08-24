
'''
Random field generation using rft1d.randn1d

Note:
When FWHM gets large (2FWHM>nNodes), the data should be padded
using the *pad* keyword.
'''


import numpy as np
from matplotlib import pyplot
from spm1d import rft1d


#(0) Set parameters:
np.random.seed(12345)
nResponses = 5
nNodes     = 101
FWHM       = 20.0


#(1) Generate Gaussian 1D fields:
y          = rft1d.randn1d(nResponses, nNodes, FWHM, pad=False)


#(2) Plot:
pyplot.close('all')
pyplot.plot(y.T)
pyplot.plot([0,100], [0,0], 'k:')
pyplot.xlabel('Field position', size=16)
pyplot.ylabel('z', size=20)
pyplot.title('Random (Gaussian) fields', size=20)
pyplot.show()
