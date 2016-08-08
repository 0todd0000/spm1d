
from math import sqrt
import itertools
import numpy as np
from scipy import stats,ndimage
from scipy.io import loadmat
from matplotlib import pyplot
import spm1d



#(0) Load data:
fname      = '/Users/todd/Documents/MATLAB/myLibraries/spm1d/examples/data/random.mat'
y          = loadmat(fname)['Y']
n,df       = y.shape[0], y.size-1
alpha      = 0.05
sqrtN      = sqrt(n)


#(1) Compute original test statistic:
t0         = y.mean(axis=0) / y.std(ddof=1, axis=0) * sqrtN


#(2) Conduct non-parametric test:
### build primary permutation PDF (maximum t value):
LABELS     = list(itertools.product([0,1], repeat=n))  #specify label signs (+ or -)
T          = []
for labels in LABELS:
	signs  = -2*np.array(labels) + 1
	yy     = (y.copy().T*signs).T
	t      = yy.mean(axis=0) / yy.std(ddof=1, axis=0) * sqrtN
	T.append(t.max())
T          = np.array(T)
### compute critical threshold:
tCrit      = np.percentile(T, 100*(1-alpha))
### build secondary permutation PDF (cluster size):
M          = []
for labels in LABELS:
	signs  = -2*np.array(labels) + 1
	yy     = (y.copy().T*signs).T
	t      = yy.mean(axis=0) / yy.std(ddof=1, axis=0) * sqrtN
	### compute maximum cluster size:
	L,nC   = ndimage.label( t > tCrit )
	if nC>0:
		m  = [(L==(i+1)).sum()   for i in range(nC)]
		M.append( max(m)  )
	else:
		M.append(0)
M          = np.array(M)
### compute p values:
L,nC   = ndimage.label( t0 > tCrit )
m0     = np.array([(L==(i+1)).sum()   for i in range(nC)])
p      = (M > m0).mean()


#(3) Compare to parametric inference:
t_para     = spm1d.stats.ttest(y)
t_para_i   = t_para.inference(alpha=0.05, two_tailed=False)


### report results:
print 'Non-parametric t test:'
print '   p=%.5f, tCritical=%.3f' %(p,tCrit)
print
print 'Parametric t test:'
print '   p=%.5f, tCritical=%.3f' %(t_para_i.p[0], t_para_i.zstar)
print






