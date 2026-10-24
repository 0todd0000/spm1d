
import numpy as np
from matplotlib import pyplot
import spm1d



# load dataset:
Y,A,B     = spm1d.util.get_dataset('Dorn2012')


# run ANOVA:
alpha     = 0.05
equal_var = True
FF        = spm1d.stats.anova2(Y, A, B, model='full', equal_var=equal_var)
FFi       = [F.inference(alpha)  for F in FF]


# run post hoc tests: (only Factor B reaches significance)
Y1        = Y[B==0]
Y2        = Y[B==1]
Y3        = Y[B==2]
Y4        = Y[B==3]
# test statistics:
t12       = spm1d.stats.ttest2(Y1, Y2, equal_var=equal_var)
t13       = spm1d.stats.ttest2(Y1, Y3, equal_var=equal_var)
t14       = spm1d.stats.ttest2(Y1, Y4, equal_var=equal_var)
t23       = spm1d.stats.ttest2(Y2, Y3, equal_var=equal_var)
t24       = spm1d.stats.ttest2(Y2, Y4, equal_var=equal_var)
t34       = spm1d.stats.ttest2(Y3, Y4, equal_var=equal_var)
# inference:
nTests    = 6
p_crit    = spm1d.util.p_critical_bonf(alpha, nTests)
t12i      = t12.inference(p_crit, two_tailed=True)
t13i      = t13.inference(p_crit, two_tailed=True)
t14i      = t14.inference(p_crit, two_tailed=True)
t23i      = t23.inference(p_crit, two_tailed=True)
t24i      = t24.inference(p_crit, two_tailed=True)
t34i      = t34.inference(p_crit, two_tailed=True)




# plot:
pyplot.close('all')
t12i.plot(color='k', facecolor='k')
t13i.plot(color='0.5', facecolor='0.5')
t14i.plot(color='0.85', facecolor='0.85')
t23i.plot(color='r', facecolor='r')
t24i.plot(color=[1,0.7,0.7], facecolor=[1,0.7,0.7])
t34i.plot(color='b', facecolor='b')
pyplot.xlim(0, 100)
pyplot.ylim(-15, 15)
pyplot.legend(['1 vs. 2', '1 vs. 3', '1 vs. 4', '2 vs. 3', '2 vs. 4', '3 vs. 4'], fontsize=12)
# pyplot.show()



