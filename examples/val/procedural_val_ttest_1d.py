
'''
Example procedural validation of spm1d hypothesis tests.

This script uses spm1d.stats.ttest and random 1D data as an example.

A valid hypothesis testing procedure will achieve a false positive
rate (FPR) of alpha (usually 0.05) over a large number of datasets.
Usually at least 10,000 random datasets are required for numerical
stability, but here 1000 are used in favor of fast execution.

Note that probability calculations associated with 1D are
relatively slow, so in favor of fast execution probability
calculations are bypassed for each dataset. Instead the
critical t-value ("tc" below) is calculated before datasets
are iteratively generated. Then each dataset's maximum t-value
is compared to the critical threshold to make a null hypothesis
rejection decision. This approach is considerably faster than
calculating probability values for each dataset because spm1d
by default calculates several different probabilities (e.g.
cluster-level probabilities) which are not directly necessary
for FPR validation.

This script is meant only to demonstrate key aspects of numerical
validation. More thorough validation possibilities are available
in spm1d.util.val and in the "tests" directory of this repository.
'''

import numpy as np
import rft1d
import spm1d



np.random.seed(3)  # random number generator seed (for numerical reproducibility)

J       = 8     # sample size
Q       = 101   # number of domain nodes
fwhm    = 25    # smoothness
alpha   = 0.05  # Type I error rate
tc      = rft1d.t.isf(alpha, J-1, Q, fwhm) # critical threshold
niter   = 1000  # number of iterations (i.e., random datasets)
tmax    = []    # maximum t-values from each dataset
for i in range(niter):
	y   = rft1d.randn1d(J, Q, fwhm)  # smooth Gaussian random fields
	spm = spm1d.stats.ttest(y, 0)
	tmax.append( spm.z.max() )
fpr     = (np.array(tmax) > tc).mean()  # false positive rate


print( f'Expected false positive rate:  {alpha}' )
print( f'Actual false positive rate:    {fpr:.5f}' )

