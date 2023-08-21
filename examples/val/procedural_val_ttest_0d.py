
'''
Example procedural validation of spm1d hypothesis tests.

This script uses spm1d.stats.ttest and random 0D data as an example.

A valid hypothesis testing procedure will achieve a false positive
rate (FPR) of alpha (usually 0.05) over a large number of datasets.
Usually at least 10,000 random datasets are required for numerical
stability, but here 1000 are used in favor of fast execution.

This script is meant only to demonstrate key aspects of numerical
validation. More thorough validation possibilities are available
in spm1d.util.val and in the "tests" directory of this repository.
'''

import numpy as np
import spm1d



np.random.seed(0)  # random number generator seed (for numerical reproducibility)

J       = 8     # sample size
alpha   = 0.05  # Type I error rate
niter   = 1000  # number of iterations (i.e., random datasets)
p       = []    # p-values from tests
for i in range(niter):
	y   = np.random.randn( J )   # random (normal) dataset
	spm = spm1d.stats.ttest(y, 0).inference(alpha)
	p.append( spm.p )
fpr     = (np.array(p) < alpha).mean()  # false positive rate

print( f'Expected false positive rate:  {alpha}' )
print( f'Actual false positive rate:    {fpr:.5f}' )

