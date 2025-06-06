
import numpy as np
import spm1d
import spm1d.stats.nonparam_old



# create data:
# 'http://www.real-statistics.com/regression/hypothesis-testing-significance-regression-line-slope/'
x    = np.array([5, 23, 25, 48, 17, 8, 4, 26, 11, 19, 14, 35, 29, 4, 23], dtype=float)
y    = np.array([80, 78, 60, 53, 85, 84, 73, 79, 81, 75, 68, 72, 58, 92, 65], dtype=float)


# conduct parametric and nonparametric tests:
np.random.seed(0)
alpha      = 0.05
two_tailed = True
niter      = 1000
ti         = spm1d.stats.regress(y, x).inference(alpha, two_tailed=two_tailed)
np.random.seed(0)
tni        = spm1d.stats.nonparam.regress(y, x).inference(alpha, two_tailed=two_tailed, iterations=niter)
np.random.seed(0)
tnio       = spm1d.stats.nonparam_old.regress(y, x).inference(alpha, two_tailed=two_tailed, iterations=niter)


print(ti)
print(tni)
print(tnio)
print()
print( 'Critical thresholds:')
print( f'   Parametric:           {ti.zstar:.5f}')
print( f'   Nonparametric:        {tni.zstar}')
print( f'   Nonparametric (old):  {tnio.zstar}')


