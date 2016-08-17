
import numpy as np
import scipy.stats
import spm1d

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
y          = np.array([0.4, 0.2, 0.5, 0.3, -0.1])
mu         = 0
# y,mu       = -y, -mu


#(1) Conduct non-parametric test:
alpha      = 0.05
two_tailed = True
t          = spm1d.stats.nonparam.ttest(y, mu)
ti         = t.inference(alpha, two_tailed=two_tailed)
print(ti)


#(2) Compare to parametric test:
results    = scipy.stats.ttest_1samp(y, mu)
tparam     = results.statistic
pparam     = get_scipy_pvalue(results, two_tailed )


#(3) Print results:
print
print( 'Non-parametric results:' )
print( '   t=%.3f, p=%.5f' %(ti.z, ti.p) )
print
print( 'Parametric results:' )
print( '   t=%.3f, p=%.5f' %(tparam, pparam) )
print


