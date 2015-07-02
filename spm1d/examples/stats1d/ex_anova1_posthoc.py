
import numpy as np
from matplotlib import pyplot
import spm1d






#(0) Load data:
dataset      = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y,A          = dataset.get_data()
Y0,Y1,Y2     = [Y[A==u] for u in np.unique(A)]


#(1) Conduct Post hoc tests:
alpha        = 0.05
nTests       = 3
p_critical   = spm1d.util.p_critical_bonf(alpha, nTests)
### t statistics:
t12   = spm1d.stats.ttest2(Y1, Y2, equal_var=False)
t13   = spm1d.stats.ttest2(Y1, Y3, equal_var=False)
t23   = spm1d.stats.ttest2(Y2, Y3, equal_var=False)
### inference:
t12i  = t12.inference(alpha=p_critical, two_tailed=True)
t13i  = t13.inference(alpha=p_critical, two_tailed=True)
t23i  = t23.inference(alpha=p_critical, two_tailed=True)



#(2) Plot results:
pyplot.close('all')
Fi.plot()
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
pyplot.ylim(-1, 500)
pyplot.xlabel('Time (%)', size=20)
pyplot.title(r'Critical threshold at $\alpha$=%.2f:  $F^*$=%.3f' %(alpha, Fi.zstar))
pyplot.show()





