
from math import sqrt
import itertools
import numpy as np
import scipy.stats


def tstat_regress(y, x):
	y      = np.asarray(y, dtype=float)
	n      = y.size
	X      = np.ones((n,2))
	X[:,0] = x
	### assemble data:
	Y      = np.matrix(y).T
	X      = np.matrix(X)
	c      = np.matrix([1,0]).T
	### solve the GLM:
	b      = np.linalg.pinv(X)*Y            #parameters
	eij    = Y - X*b                        #residuals
	R      = eij.T*eij                      #residuals sum of squares
	df     = n - 2                          #degrees of freedom
	sigma2 = float(R)/df                  #variance
	### compute t statistic
	t = np.array(c.T*b).flatten()  /   np.sqrt(sigma2*float(c.T*(np.linalg.inv(X.T*X))*c))
	return float(t)
	

#(0) Create data:
# 'http://www.real-statistics.com/regression/hypothesis-testing-significance-regression-line-slope/'
x    = np.array([5, 23, 25, 48, 17, 8, 4, 26, 11, 19, 14, 35, 29, 4, 23])
y    = np.array([80, 78, 60, 53, 85, 84, 73, 79, 81, 75, 68, 72, 58, 92, 65])

x    = np.array([5,  23, 25, 48, 17, 8])
y    = np.array([80, 78, 60, 53, 85, 84])



#(1) Compute original test statistic:
t0         = tstat_regress(y, x)
print t0



# #(2) Conduct non-parametric test:
# ### build permutation PDF:
# nIter  = 1000
# n      = y.size
# Z          = []
# for i in range(nIter):
# 	ind    = np.random.permutation(n)
# 	xx     = x[ind]
# 	t      = tstat_regress(y, xx)
# 	Z.append(t)
# Z          = np.array(Z)
# ### conduct inference
# p          = np.mean( T>t0 )
# tCrit      = np.percentile(T, 100*(1-alpha))


#(2) Conduct non-parametric test:
nIter  = 1000
n      = y.size
perms  = list(itertools.permutations(range(n), n))
Z          = []
for ind in perms:
	xx     = x[ list(ind) ]
	t      = tstat_regress(y, xx)
	Z.append(t)
Z          = np.array(Z)

### conduct inference
alpha      = 0.05
B          = Z>t0 if t0>0 else Z<t0
p          = np.mean( B )
tCrit      = np.percentile(Z, 100*(1-alpha))


print t0, p



# from matplotlib import pyplot
#
# pyplot.close('all')
# pyplot.figure(figsize=(8,6))
# pyplot.get_current_fig_manager().window.move(0, 0)
# ax = pyplot.axes()
# ax.hist( Z )
# pyplot.show()





results    = scipy.stats.linregress(y, x)
r          = results.rvalue
t          = r * ((y.size-2)/(1-r*r) )**0.5

# print results
print t, 0.5*results.pvalue



# ### build permutation PDF:
# LABELS     = list(itertools.product([0,1], repeat=n))  #specify label signs (+ or -)
# T          = []
# for labels in LABELS:
# 	signs  = -2*np.array(labels) + 1
# 	yy     = y.copy()*signs
# 	t      = yy.mean() / yy.std(ddof=1) * sqrtN
# 	T.append(t)
# T          = np.array(T)
#
#
# #(3) Compare to parametric inference:
# p_para     = stats.t.sf(t0, df)
# tCrit_para = stats.t.isf(alpha, df)
#
#
#
# ### report results:
# print 'Non-parametric test:'
# print '   t=%.3f, p=%.5f, tCritical=%.3f' %(t0,p,tCrit)
# print
# print 'Parametric test:'
# print '   t=%.3f, p=%.5f, tCritical=%.3f' %(t0,p_para,tCrit_para)
# print


