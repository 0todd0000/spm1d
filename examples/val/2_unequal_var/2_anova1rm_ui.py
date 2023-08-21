
'''

(this is the same as ttest2_0d_proc.py but uses spm1d.util.val.ui
for more convenient validation scripting.)

Demonstration of validation of hypothesis testing results for
cases of unequal group variance.

This script uses spm1d.stats.ttest2 and random 0D as an example.

A valid hypothesis testing procedure will achieve a false positive
rate (FPR) of alpha (usually 0.05) over a large number of datasets.
Usually at least 10,000 random datasets are required for numerical
stability, but here 1000 are used in favor of fast execution.

Below the first validation attempt fails because equal variance
is assumed through equal_var=True.  The second validation attempt
succeeds, anecdotally demonstrating robustness to unequal variance.

This script is meant only to demonstrate key aspects of numerical
validation. More thorough validation possibilities are available
in spm1d.util.val and in the "tests" directory of this repository.
'''

import numpy as np
from spm1d.util.val.ui import val_anova1rm



# # 0D case
# np.random.seed(1)  # random number generator seed (for numerical reproducibility)
# J    = 12          # sample size (number of participants)
# ss   = 5, 1, 1     # standard deviations
# val0 = val_anova1rm(J, ss, niter=1000, equal_var=True)
# val1 = val_anova1rm(J, ss, niter=1000, equal_var=False)
# print( f'FPR (equal_var=True):   {val0.fpr}'  )
# print( f'FPR (equal_var=False):  {val1.fpr}'  )



# 1D case
np.random.seed(10) # random number generator seed (for numerical reproducibility)
J    = 8          # sample size (number of participants)
ss   = 5, 1, 1     # standard deviations
val0 = val_anova1rm(J, ss, Q=101, fwhm=10, niter=1000, equal_var=True)
val1 = val_anova1rm(J, ss, Q=101, fwhm=10, niter=1000, equal_var=False)
print( f'FPR (equal_var=True):   {val0.fpr}'  )
print( f'FPR (equal_var=False):  {val1.fpr}'  )