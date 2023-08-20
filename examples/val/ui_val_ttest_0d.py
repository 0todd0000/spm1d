
'''
Example spm1d.util.val.ui-based validation of spm1d procedures.

This script uses spm1d.stats.ttest and random 0D data as an example.

This UI-based validation is the highest-level validation procedure
available in spm1d.

A valid hypothesis testing procedure will achieve a false positive
rate (FPR) of the specified alpha (usually 0.05) over a large
number of datasets. Usually at least 10,000 random datasets are
required for numerical stability, but here 1000 are used in favor
of fast execution.

This script is meant only to demonstrate key aspects of numerical
validation. More thorough validation possibilities are available
in spm1d.util.val and in the "tests" directory of this repository.
'''

import numpy as np
from spm1d.util.val.ui import val_ttest



np.random.seed(0)  # random number generator seed (for numerical reproducibility)
J   = 8  # sample size
val = val_ttest(J, niter=1000)
print( val )  # report simulation results

