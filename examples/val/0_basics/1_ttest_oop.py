
'''
Example object-oriented programming (OOP) validation of spm1d
hypothesis tests.

This script uses spm1d.stats.ttest and random 0D data as an example.

A valid hypothesis testing procedure will achieve a false positive
rate (FPR) of alpha (usually 0.05) over a large number of datasets.
Usually at least 10,000 random datasets are required for numerical
stability, but here 1000 are used in favor of fast execution.

This script is meant only to demonstrate key aspects of numerical
validation. More thorough validation possibilities are available
in spm1d.util.val and in the "tests" directory of this repository.

Below the following key objects are used:

- "fn": a lambda version of the spm1d.stats function to be
validated; this function must accept just one input argument (the 
dependent variable)

- "rng": a random number generator that generates one new random
dataset each time it is called; this function must accept zero
input arguments

- "val": an instance of the FPRValidator class; performs
simulation execution and FPR calculation; the results are deemed
"valid" if the actual FPR is within "tol" of alpha
'''

import numpy as np
import spm1d
from spm1d.util.val import FPRValidator




np.random.seed(0)  # random number generator seed (for numerical reproducibility)

J       = 8  # sample size
fn      = lambda y: spm1d.stats.ttest(y, 0) # see notes above
rng     = lambda: np.random.randn( J )  # see notes above
val     = FPRValidator(fn, rng, alpha=0.05, tol=0.005)  # see notes above
val.sim( niter=1000 )  # simulate 1000 random datasets

print( val )  # report simulation results

