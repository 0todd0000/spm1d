
from math import sqrt
import numpy as np
from scipy import stats,ndimage
from scipy.io import loadmat
from matplotlib import pyplot
import spm1d



#(0) Load data:
fname      = '/Users/todd/Documents/MATLAB/myLibraries/spm1d/examples/data/ex_kinematics.mat'
y          = loadmat(fname)['Y']
yA,yB      = y[10:20], y[20:]
nA,nB      = yA.shape[0], yB.shape[0]
df         = nA + nB - 2
alpha      = 0.05



#(1) Compute original test statistic:
mA,mB  = yA.mean(axis=0), yB.mean(axis=0)
sA,sB  = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
s      = np.sqrt(    ((nA-1)*sA*sA + (nB-1)*sB*sB)  /  (nA + nB - 2)     )
t0     = (mA-mB) / ( s *sqrt(1.0/nA + 1.0/nB))


#(2) Conduct non-parametric test:
np.random.seed(0)
### build primary permutation PDF (maximum t value):
N          = nA + nB
y          = np.vstack([yA,yB])
nIterations = 1000
T          = []
for i in range(nIterations):
	groupA = np.random.permutation(N)[:nA]
	labels = np.zeros(N)
	labels[groupA] = 1
	yyA    = y[labels==1]
	yyB    = y[labels==0]
	### compute test stat:
	mA,mB  = yyA.mean(axis=0), yyB.mean(axis=0)
	sA,sB  = yyA.std(ddof=1, axis=0), yyB.std(ddof=1, axis=0)
	s      = np.sqrt(    ((nA-1)*sA*sA + (nB-1)*sB*sB)  /  (nA + nB - 2)     )
	t      = (mA-mB) / ( s *sqrt(1.0/nA + 1.0/nB))
	T.append(t.max())
T          = np.array(T)
### conduct inference
tCrit      = np.percentile(T, 100*(1-alpha))
### build secondary permutation PDF (cluster size):
M          = []
for i in range(nIterations):
	groupA = np.random.permutation(N)[:nA]
	labels = np.zeros(N)
	labels[groupA] = 1
	yyA    = y[labels==1]
	yyB    = y[labels==0]
	### compute test stat:
	mA,mB  = yyA.mean(axis=0), yyB.mean(axis=0)
	sA,sB  = yyA.std(ddof=1, axis=0), yyB.std(ddof=1, axis=0)
	s      = np.sqrt(    ((nA-1)*sA*sA + (nB-1)*sB*sB)  /  (nA + nB - 2)     )
	t      = (mA-mB) / ( s *sqrt(1.0/nA + 1.0/nB))
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
t_para     = spm1d.stats.ttest2(yA, yB)
t_para_i   = t_para.inference(alpha=0.05, two_tailed=False)


### report results:
print 'Non-parametric t test:'
print '   p=%.5f, tCritical=%.3f' %(p,tCrit)
print
print 'Parametric t test:'
print '   p=%.5f, tCritical=%.3f' %(t_para_i.p[0], t_para_i.zstar)
print






