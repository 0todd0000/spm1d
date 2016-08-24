
import numpy as np
import spm1d



#(0) Create data:
# 'http://www.real-statistics.com/regression/hypothesis-testing-significance-regression-line-slope/'
x    = np.array([5, 23, 25, 48, 17, 8, 4, 26, 11, 19, 14, 35, 29, 4, 23], dtype=float)
y    = np.array([80, 78, 60, 53, 85, 84, 73, 79, 81, 75, 68, 72, 58, 92, 65], dtype=float)




#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
two_tailed = True
tn         = spm1d.stats.nonparam.regress(y, x)
tni        = tn.inference(alpha, two_tailed=two_tailed, iterations=1000)
print( 'Non-parametric results:' )
print( tni )



#(2) Compare to parametric test:
t          = spm1d.stats.regress(y, x)
ti         = t.inference(alpha, two_tailed=two_tailed)
print( 'Parametric results:' )
print( ti )


