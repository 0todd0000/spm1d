
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load dataset:
# dataset    = spm1d.data.uv1d.t1.Random()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()
# y  *= -1



#(1) Conduct non-parametric test:
alpha      = 0.05
two_tailed = False
t          = spm1d.stats.nonparam.ttest(y, mu)
ti         = t.inference(alpha, two_tailed=two_tailed, iterations=-1)
print ti
print ti.clusters



#(2) Compare with parametric result:
tparam     = spm1d.stats.ttest(y, mu)
tiparam    = tparam.inference(alpha, two_tailed=two_tailed)



#(3) Plot
pyplot.close('all')
pyplot.figure(figsize=(12,4))
pyplot.get_current_fig_manager().window.move(0, 0)
ax = pyplot.subplot(121);  tiparam.plot(ax=ax)
ax = pyplot.subplot(122);  ti.plot(ax=ax)
pyplot.show()


