
from math import log
import itertools
import numpy as np
import spm1d


def cca(y, x):
	N          = y.shape[0]
	X,Y        = np.matrix(x.T).T, np.matrix(y)
	Z          = np.matrix(np.ones(N)).T
	Rz         = np.eye(N) - Z*np.linalg.inv(Z.T*Z)*Z.T
	XStar      = Rz * X
	YStar      = Rz * Y
	p,r        = 1.0, 1.0   #nContrasts, nNuisanceFactors
	m          = N - p - r
	H          = YStar.T * XStar  *  np.linalg.inv( XStar.T * XStar  )  * XStar.T * YStar / p
	W          = YStar.T  * (np.eye(N)  -  XStar*np.linalg.inv(XStar.T*XStar)*XStar.T) * YStar  / m
	#estimate maximum canonical correlation:
	F          = np.linalg.inv(W)*H
	ff         = np.linalg.eigvals(  F  )
	fmax       = float( np.real(ff.max()) )
	r2max      = fmax * p  / (m + fmax*p)
	rmax       = (r2max)**0.5
	### compute test statistic:
	m          = y.shape[1]
	x2         = -(N-1-0.5*(m+2)) * log(  (1-rmax**2) )
	# df         = m
	return x2
	

#(0) Load dataset:
dataset = spm1d.data.mv0d.cca.FitnessClub()
dataset = spm1d.data.mv0d.cca.StackExchange()
y,x     = dataset.Y, dataset.x
# y,x     = [a[:7]  for a in [y,x]]      
# x      *= -1
print dataset



#(1) Compute original test statistic:
z0         = cca(y, x)
print z0



#(2) Conduct non-parametric test:
alpha  = 0.05
### build permutation PDF:
nIter  = 1000
n      = x.size
Z          = []
for i in range(nIter):
	ind    = np.random.permutation(n)
	z      = cca(y, x[ind])
	Z.append(z)
Z          = np.array(Z)
### conduct inference
p          = np.mean( Z > z0 )
zstar      = np.percentile(Z, 100*(1-alpha))


# #(2) Conduct non-parametric test:
# nIter  = 1000
# n      = y.size
# perms  = list(itertools.permutations(range(n), n))
# Z          = []
# for ind in perms:
# 	xx     = x[ list(ind) ]
# 	t      = tstat_regress(y, xx)
# 	Z.append(t)
# Z          = np.array(Z)
#
# ### conduct inference
# alpha      = 0.05
# B          = Z>t0 if t0>0 else Z<t0
# p          = np.mean( B )
# tCrit      = np.percentile(Z, 100*(1-alpha))
#
#
# print t0, p



# from matplotlib import pyplot
#
# pyplot.close('all')
# pyplot.figure(figsize=(8,6))
# pyplot.get_current_fig_manager().window.move(0, 0)
# ax = pyplot.axes()
# ax.hist( Z )
# pyplot.show()
#


#(3) Compare to parametric inference:
X2param    = spm1d.stats.cca(y, x)
X2parami   = X2param.inference(0.05)
zparam     = X2parami.z
pparam     = X2parami.p



### report results:
print 'Non-parametric t test:'
print '   X2=%.3f, p=%.5f' %(z0, p)
print
print 'Parametric t test:'
print '   X2=%.3f, p=%.5f' %(zparam, pparam)
print


