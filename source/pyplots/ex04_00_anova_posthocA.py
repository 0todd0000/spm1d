
import numpy as np
from matplotlib import pyplot
import spm1d


# load dataset:
subj         = 0   #subject number
Y1,Y2,Y3     = spm1d.util.get_dataset('speed-grf-categorical', 0)


# conduct one-way ANOVA:
alpha        = 0.05
equal_var    = False
F            = spm1d.stats.anova1( (Y1,Y2,Y3), equal_var=equal_var )
Fi           = F.inference(alpha)


# conduct post hoc tests:
t12    = spm1d.stats.ttest2(Y1, Y2, equal_var=False)
t13    = spm1d.stats.ttest2(Y1, Y3, equal_var=False)
t23    = spm1d.stats.ttest2(Y2, Y3, equal_var=False)

# inference:
nTests     = 3
p_critical = spm1d.util.p_critical_bonf(alpha, nTests)
t12i       = t12.inference(alpha=p_critical, two_tailed=True)
t13i       = t13.inference(alpha=p_critical, two_tailed=True)
t23i       = t23.inference(alpha=p_critical, two_tailed=True)



# plot results:
pyplot.close('all')
pyplot.figure(figsize=(4,3))
ax         = pyplot.axes([0.15,0.15,0.8,0.8])
t23i.plot()
pyplot.setp(ax, xlim=(70, 100), ylim=(-6, 1))
ax.text(80, -2, 'Group 2 vs. Group 3')



