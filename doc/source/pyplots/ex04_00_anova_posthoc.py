
import numpy as np
from matplotlib import pyplot
import spm1d


# load dataset:
Y1,Y2,Y3     = spm1d.util.get_dataset('speed-grf-categorical', 0)


# conduct one-way ANOVA:
alpha        = 0.05
equal_var    = False
F            = spm1d.stats.anova1( (Y1,Y2,Y3), equal_var=equal_var )
Fi           = F.inference(alpha)


# conduct post hoc tests:
t12          = spm1d.stats.ttest2(Y1, Y2, equal_var=equal_var)
t13          = spm1d.stats.ttest2(Y1, Y3, equal_var=equal_var)
t23          = spm1d.stats.ttest2(Y2, Y3, equal_var=equal_var)


# inference:
nTests       = 3
p_critical   = spm1d.util.p_critical_bonf(alpha, nTests)
t12i         = t12.inference(alpha=p_critical, two_tailed=True)
t13i         = t13.inference(alpha=p_critical, two_tailed=True)
t23i         = t23.inference(alpha=p_critical, two_tailed=True)


# plot results:
pyplot.close('all')
pyplot.figure(figsize=(12,3))
ax0          = pyplot.axes((0.05,0.15,0.27,0.8))
ax1          = pyplot.axes((0.38,0.15,0.27,0.8))
ax2          = pyplot.axes((0.72,0.15,0.27,0.8))
t12i.plot(ax=ax0)
t13i.plot(ax=ax1)
t23i.plot(ax=ax2)
pyplot.setp([ax0,ax1,ax2], ylim=(-35,35))
ax0.text(25, -29, 'Group 1 vs. Group 2')
ax1.text(25, -29, 'Group 1 vs. Group 3')
ax2.text(25, -29, 'Group 2 vs. Group 3')
# pyplot.show()