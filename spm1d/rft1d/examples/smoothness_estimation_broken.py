
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

'''
WARNING!
Calls to rft1d.random.randn1d must set pad=True
when FWHM is greater than 50
'''

#(0) Set parameters:
np.random.seed(0)
nResponses   = 1000
nNodes       = 101
### generate a field mask:
nodes        = np.array([True]*nNodes) #nothing masked out
nodes[10:30] = False  #this region will be masked out
nodes[60:85] = False


#(1) Cycle through smoothing kernels:
FWHM       = np.linspace(1, 50, 21) #actual FWHM
FWHMe      = [] #estimated FWHM
for w in FWHM:
	y      = rft1d.random.randn1d(nResponses, nodes, w, pad=False)  #broken fields
	FWHMe.append(   rft1d.geom.estimate_fwhm(y)   )
	print( 'Actual FWHM: %06.3f, estimated FWHM: %06.3f' %(w, FWHMe[-1])  )


#(2) Plot results:
pyplot.close('all')
pyplot.plot(FWHM, FWHM,  'k:', label='Actual')
pyplot.plot(FWHM, FWHMe, 'go', label='Estimated')
pyplot.legend(loc='upper left')
pyplot.xlabel('Actual FWHM', size=16)
pyplot.ylabel('Estimated FWHM', size=16)
pyplot.title('FWHM estimation validation (broken fields)', size=20)
pyplot.show()