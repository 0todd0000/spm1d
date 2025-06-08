
import numpy as np
import spm1d
import spm1d.stats.nonparam_old



# create data:
### Dataset 1  (non-normally distributed)
y0         = np.array([5.7, 8.4, 6.0, 6.4, 5.5])
y1         = np.array([5.3, 8.2, 5.5, 6.1, 5.6])
### Dataset2 (normally distributed)
y0         = np.array([ 1.764,  0.400,  0.978,  2.240,  1.867, -0.977])
y1         = np.array([ 0.950, -0.151, -0.103,  0.410,  0.144,  1.454])


# conduct parametric and nonparametric tests:
np.random.seed(0)
alpha      = 0.05
two_tailed = True
niter      = -1 
ti         = spm1d.stats.ttest2(y1, y0).inference(alpha, two_tailed=two_tailed)
np.random.seed(0)
tni        = spm1d.stats.nonparam.ttest2(y1, y0).inference(alpha, two_tailed=two_tailed, iterations=niter)
np.random.seed(0)
tnio       = spm1d.stats.nonparam_old.ttest2(y1, y0).inference(alpha, two_tailed=two_tailed, iterations=niter)


print(ti)
print(tni)
print(tnio)
print()
print( 'Critical thresholds:')
print( f'   Parametric:           {ti.zstar:.5f}')
print( f'   Nonparametric:        {tni.zstar}')
print( f'   Nonparametric (old):  {tnio.zstar}')


