
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



# ATTEMPT 1:  equal variance assumed   (  equal_var=True  )

np.random.seed(100)
niter = 1000
JJ    = 12, 5
ss    = 5, 1
alpha = 0.05
p     = []
for i in range(niter):
	y0,y1 = [s * np.random.randn(J) for s,J in zip(ss,JJ)]
	spm   = spm1d.stats.ttest2(y0, y1, equal_var=True).inference(alpha)
	p.append( spm.p )
fpr   = (np.array(p) < alpha).mean()  # false positive rate

print( 'ATTEMPT 1:  equal variance assumed')
print( f'   Expected false positive rate:  {alpha}' )
print( f'   Actual false positive rate:    {fpr:.5f}' )
print()



# ATTEMPT 2:  equal variance NOT assumed   (  equal_var=False  )

np.random.seed(100)
p     = []
for i in range(niter):
	y0,y1 = [s * np.random.randn(J) for s,J in zip(ss,JJ)]
	spm   = spm1d.stats.ttest2(y0, y1, equal_var=False).inference(alpha)
	p.append( spm.p )
fpr   = (np.array(p) < alpha).mean()  # false positive rate

print( 'ATTEMPT 2:  equal variance NOT assumed')
print( f'   Expected false positive rate:  {alpha}' )
print( f'   Actual false positive rate:    {fpr:.5f}' )


