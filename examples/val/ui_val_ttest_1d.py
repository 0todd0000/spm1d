
'''
Example spm1d.util.val.ui-based validation of spm1d hypothesis tests.

This script uses spm1d.stats.ttest and random 0D data as an example.

This UI-based validation is the highest-level validation procedure
available in spm1d.

A valid hypothesis testing procedure will achieve a false positive
rate (FPR) of alpha (usually 0.05) over a large number of datasets.
Usually at least 10,000 random datasets are required for numerical
stability, but here 1000 are used in favor of fast execution.

This script is meant only to demonstrate key aspects of numerical
validation. More thorough validation possibilities are available
in spm1d.util.val and in the "tests" directory of this repository.

Below "valtype=z" indicates that only the critical threshold (and not
other probability quantities) should be used in validation.
'''

import numpy as np
import matplotlib.pyplot as plt
from spm1d.util.val.ui import val_ttest



np.random.seed(5)  # random number generator seed (for numerical reproducibility)

J    = 8  # sample size
Q    = 101   # number of domain nodes
fwhm = 25    # smoothness
val  = val_ttest(J, Q, fwhm, valtype='z', niter=1000)
print( val )  # report simulation results


# optionally use the "plot_results" method for visual details
#    regarding the distribution of outputs
plt.close('all')
plt.figure( figsize=(8,6) )
ax = plt.axes()
val.plot_results(ax)
plt.show()