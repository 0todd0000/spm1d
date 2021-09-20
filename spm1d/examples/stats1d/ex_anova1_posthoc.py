
import numpy as np
import matplotlib.pyplot as plt
import spm1d






#(0) Load data:
dataset      = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y,A          = dataset.get_data()
Y1,Y2,Y3     = [Y[A==u] for u in np.unique(A)]


#(1) Conduct main test:
F            = spm1d.stats.anova1(Y, A, equal_var=True)
Fi           = F.inference(0.05)


#(2) Conduct Post hoc tests:
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
plt.close('all')
plt.subplot(221)
Fi.plot()
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
plt.ylim(-1, 500)
plt.title('Main test')

plt.subplot(222);  t12i.plot();  plt.title('Posthoc:  1 vs. 2');  plt.ylim(-40, 40)
plt.subplot(223);  t23i.plot();  plt.title('Posthoc:  2 vs. 3');  plt.ylim(-40, 40)
plt.subplot(224);  t13i.plot();  plt.title('Posthoc:  1 vs. 3');  plt.ylim(-40, 40)


plt.show()





