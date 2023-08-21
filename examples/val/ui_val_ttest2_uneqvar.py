
'''
Example procedural validation of spm1d hypothesis tests.

This script uses spm1d.stats.ttest2 and random 0D data with
unequal group variances as an example.

A valid hypothesis testing procedure will achieve a false positive
rate (FPR) of alpha (usually 0.05) over a large number of datasets.
Usually at least 10,000 random datasets are required for numerical
stability, but here 1000 are used in favor of fast execution.

Below the first validation attempt fails because equal variance
is assumed through equal_var=True.  The second validation attempt
succeeds, anecodatally demonstrating spm1d's capabilities for
handling unequal variance.

This script is meant only to demonstrate key aspects of numerical
validation. More thorough validation possibilities are available
in spm1d.util.val and in the "tests" directory of this repository.
'''

import numpy as np
import spm1d
from spm1d.util.val.ui import val_ttest2



np.random.seed(1)  # random number generator seed (for numerical reproducibility)
JJ   = 12, 5  # sample sizes
ss   = 5, 1   # standard deviations
val0 = val_ttest2(JJ, ss, niter=5000, equal_var=True)
val1 = val_ttest2(JJ, ss, niter=5000, equal_var=False)

print( val0.fpr )  # report FPR
print( val1.fpr )  # report FPR

