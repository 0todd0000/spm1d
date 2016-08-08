
import numpy as np
import scipy.stats
import spm1dNP



def get_scipy_pvalue(results, two_tailed=False):
	'''
	Convert p value from scipy.stats (which yields two-tailed p values)
	to a one-tailed value (if necessary).
	'''
	z,p   =  results.statistic, results.pvalue
	if not two_tailed:
		p = 0.5 * p
		if (z < 0):
			p = 1 - p
	return p
	
	
#(0) Create data:
### Dataset 1  (non-normally distributed)
yA         = np.array([5.7, 8.4, 6.0, 6.4, 5.5])
yB         = np.array([5.3, 8.2, 5.5, 6.1, 5.6])
### Dataset2 (normally distributed)
yA         = np.array([ 1.764,  0.400,  0.978,  2.240,  1.867, -0.977])
yB         = np.array([ 0.950, -0.151, -0.103,  0.410,  0.144,  1.454])
yA,yB      = yB, yA


#(1) Conduct non-parametric test:
alpha      = 0.05
two_tailed = True
t          = spm1dNP.ttest2(yA, yB)
ti         = t.inference(alpha, two_tailed=two_tailed)
print(ti)



#(2) Compare to parametric inference:
results    = scipy.stats.ttest_ind(yA, yB)
tparam     = results.statistic
pparam     = get_scipy_pvalue( results, two_tailed )



#(3) Compare to parametric test:
print
print( 'Non-parametric results:' )
print( '   t=%.3f, p=%.5f' %(ti.z, ti.p) )
print
print( 'Parametric results:' )
print( '   t=%.3f, p=%.5f' %(tparam, pparam) )
print


