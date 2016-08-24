
import numpy as np
import spm1d


#(0) Create data:
yA         = np.array([5.7, 8.4, 6.0, 6.4, 5.5])
yB         = np.array([5.3, 8.2, 5.5, 6.1, 5.6])


#(1) Conduct non-parametric test:
alpha      = 0.05
two_tailed = True
tn         = spm1d.stats.nonparam.ttest_paired(yA, yB)
tni        = tn.inference(alpha, two_tailed=two_tailed)
print( 'Non-parametric results:' )
print(tni)


#(2) Compare to parametric test:
t          = spm1d.stats.ttest_paired(yA, yB)
ti         = t.inference(alpha, two_tailed=two_tailed)
print( 'Parametric results:' )
print( ti )


