
import numpy as np
from matplotlib import pyplot
import spm1d


# load dataset:
Y0,Y1,Y2     = spm1d.util.get_dataset('speed-grf-categorical', 0)


# conduct one-way ANOVA:
alpha        = 0.05
F            = spm1d.stats.anova1( (Y0,Y1,Y2) )
Fi           = F.inference(alpha)


# plot results:
pyplot.close('all')
Fi.plot()
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
pyplot.ylim(-1, 500)
pyplot.xlabel('Time (%)', size=20)
pyplot.title(r'Critical threshold at $\alpha$=%.2f:  $F^*$=%.3f' %(alpha, Fi.zstar))
# pyplot.show()