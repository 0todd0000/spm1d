
import numpy as np
import scipy.stats
import spm1d



def get_scipy_pvalue(results, two_tailed=False):
	'''
	Convert p value from scipy.stats (which yields two-tailed p values)
	to a one-tailed value (if necessary).
	'''
	z,p   =  results.rvalue, results.pvalue
	if not two_tailed:
		p = 0.5 * p
		if (z < 0):
			p = 1 - p
	return p



#(0) Create data:
# 'http://www.real-statistics.com/regression/hypothesis-testing-significance-regression-line-slope/'
x    = np.array([5, 23, 25, 48, 17, 8, 4, 26, 11, 19, 14, 35, 29, 4, 23], dtype=float)
y    = np.array([80, 78, 60, 53, 85, 84, 73, 79, 81, 75, 68, 72, 58, 92, 65], dtype=float)

# x,y  = [a[3:11]  for a in [x,y]]

# x    = np.array([5,  23, 25, 48, 17, 8])
# y    = np.array([80, 78, 60, 53, 85, 84])
y   *= -1



### test high-level function:
#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
two_tailed = False
t          = spm1d.stats.nonparam.regress(y, x)
# ti         = t.inference(alpha, two_tailed=two_tailed, iterations=-1, force_iterations=True)
ti         = t.inference(alpha, two_tailed=two_tailed, iterations=1000)
print(ti)



from matplotlib import pyplot
pyplot.close('all')
pyplot.figure(figsize=(8,6))
pyplot.get_current_fig_manager().window.move(0, 0)
ax = pyplot.axes()
ax.hist( ti.permuter.Z )
pyplot.show()


### compare:
#(2) Compare to parametric test:
results    = scipy.stats.linregress(y, x)
r          = results.rvalue
tparam     = r * ((y.size-2)/(1-r*r) )**0.5
pparam     = get_scipy_pvalue( results, two_tailed )


print
print( 'Non-parametric results:' )
print( '   t=%.3f, p=%.5f' %(ti.z, ti.p) )
print
print( 'Parametric results:' )
print( '   t=%.3f, p=%.5f' %(tparam, pparam) )
print


