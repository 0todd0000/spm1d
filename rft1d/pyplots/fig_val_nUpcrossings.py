
import numpy as np
from matplotlib import pyplot
import rft1d


#(0) Specify parameters:
np.random.seed(0)
nResponses = 1000
nNodes     = 101
FWHM       = 10.0
U          = np.linspace(1, 4, 21)   #threshold heights

#(1) Expected number of upcrossings:
rftcalc    = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHM)
nExpected  = rftcalc.expected.number_of_upcrossings(U)


#(2) Generate null data:
y          = rft1d.randn1d(nResponses, nNodes, FWHM)


#(3) Compute actual number of upcrossings:
calc       = rft1d.geom.ClusterMetricCalculator()
nActual    = np.array([[calc.nUpcrossings(yy, uu)   for yy in y]  for uu in U]).mean(axis=1)


#(4) Plot results:
pyplot.close('all')
ax      = pyplot.axes()
ax.plot(U, nExpected, 'b-', label='Expected')
ax.plot(U, nActual, 'bo', label='Actual')
ax.legend()
ax.set_xlabel('Threshold ($u$)', size=16)
ax.set_ylabel('Number of upcrossings', size=16)
ax.set_title('Validation for number of upcrossings (Gaussian fields)', size=20)
# pyplot.show()
