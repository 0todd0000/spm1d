
from math import sqrt
import itertools
import numpy as np
from scipy import stats



#(0) Create data and specify parameters:
y          = np.array([0.4, 0.2, 0.5, 0.3, -0.1])
n,df       = y.size, y.size-1
alpha      = 0.05
sqrtN      = sqrt(n)


#(1) Compute original test statistic:
t0         = y.mean() / y.std(ddof=1) * sqrtN


#(2) Conduct non-parametric test:
### build permutation PDF:
LABELS     = list(itertools.product([0,1], repeat=n))  #specify label signs (+ or -)
T          = []
for labels in LABELS:
	signs  = -2*np.array(labels) + 1
	yy     = y.copy()*signs
	t      = yy.mean() / yy.std(ddof=1) * sqrtN
	T.append(t)
T          = np.array(T)
### conduct inference
p          = np.mean( T>t0 )
tCrit      = np.percentile(T, 100*(1-alpha))


#(3) Compare to parametric inference:
p_para     = stats.t.sf(t0, df)
tCrit_para = stats.t.isf(alpha, df)



### report results:
print( 'Non-parametric test:' )
print( '   t=%.3f, p=%.5f, tCritical=%.3f' %(t0,p,tCrit) ) 
print
print( 'Parametric test:' )
print( '   t=%.3f, p=%.5f, tCritical=%.3f' %(t0,p_para,tCrit_para) ) 
print

