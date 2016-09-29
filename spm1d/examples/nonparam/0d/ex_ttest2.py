
import numpy as np
import spm1d



#(0) Create data:
### Dataset 1  (non-normally distributed)
yA         = np.array([5.7, 8.4, 6.0, 6.4, 5.5])
yB         = np.array([5.3, 8.2, 5.5, 6.1, 5.6])
### Dataset2 (normally distributed)
yA         = np.array([ 1.764,  0.400,  0.978,  2.240,  1.867, -0.977])
yB         = np.array([ 0.950, -0.151, -0.103,  0.410,  0.144,  1.454])



#(1) Conduct non-parametric test:
alpha      = 0.05
two_tailed = True
tn         = spm1d.stats.nonparam.ttest2(yA, yB)
tni        = tn.inference(alpha, two_tailed=two_tailed)
print( 'Non-parametric results:' )
print(tni)



#(2) Compare to parametric test:
t          = spm1d.stats.ttest2(yA, yB)
ti         = t.inference(alpha, two_tailed=two_tailed)
print( 'Parametric results:' )
print( ti )


