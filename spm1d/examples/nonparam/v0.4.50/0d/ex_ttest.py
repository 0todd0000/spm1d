
import numpy as np
import spm1d
import spm1d.stats.nonparam_old



# create data:
dataset = spm1d.data.uv0d.t1.RSWeightReduction()
dataset = spm1d.data.uv0d.t1.ColumbiaSalmonella()
y,mu    = dataset.get_data()
# print( dataset )


# conduct parametric and nonparametric tests:
np.random.seed(0)
alpha      = 0.05
two_tailed = True
niter      = -1
ti         = spm1d.stats.ttest(y, mu).inference(alpha, two_tailed=two_tailed)
np.random.seed(0)
tni        = spm1d.stats.nonparam.ttest(y, mu).inference(alpha, two_tailed=two_tailed, iterations=niter)
np.random.seed(0)
tnio       = spm1d.stats.nonparam_old.ttest(y, mu).inference(alpha, two_tailed=two_tailed, iterations=niter)


print(ti)
print(tni)
print(tnio)
print()
print( 'Critical thresholds:')
print( f'   Parametric:           {ti.zstar:.5f}')
print( f'   Nonparametric:        {tni.zstar}')
print( f'   Nonparametric (old):  {tnio.zstar}')


