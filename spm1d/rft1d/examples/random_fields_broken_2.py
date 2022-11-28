
'''
Broken (piecewise continuous) random field generation using
rft1d.random.Generator1D

Note:
When FWHM gets large (2FWHM>nNodes), the data should be padded
using the *pad* keyword.
'''


import numpy as np
from matplotlib import pyplot
from spm1d import rft1d


#(0) Set parameters:
np.random.seed(12345)
nResponses   = 5
nNodes       = 101
FWHM         = 20.0
### create a boolean mask:
nodes        = np.array([True]*nNodes) #nothing masked out
nodes[20:30] = False  #this region will be masked out
nodes[60:80] = False  #this region will be masked out


#(1) Generate Gaussian 1D fields:
generator    = rft1d.random.Generator1D(nResponses, nodes, FWHM)
y            = generator.generate_sample()
y            = generator.generate_sample()
y            = generator.generate_sample()
y            = generator.generate_sample()


#(2) Plot fields:
pyplot.close('all')
pyplot.plot(y.T)
pyplot.plot([0,100], [0,0], 'k:')
pyplot.xlabel('Field position', size=16)
pyplot.ylabel('z', size=20)
pyplot.title('Broken (piecewise continuous) random fields', size=20)
pyplot.show()
