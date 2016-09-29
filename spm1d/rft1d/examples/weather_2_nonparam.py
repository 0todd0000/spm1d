
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d





def here_tstat2(yA, yB):
	nA,nB  = yA.shape[0], yB.shape[0]
	mA,mB  = yA.mean(axis=0), yB.mean(axis=0)
	sA,sB  = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
	s      = np.sqrt(    ((nA-1)*sA*sA + (nB-1)*sB*sB)  /  (nA + nB - 2)     )
	t      = (mA-mB) / ( s *np.sqrt(1.0/nA + 1.0/nB))
	return t



#(0) Load weather data:
weather  = rft1d.data.weather() #dictionay containing geographical locations
### choose two geographical locations:
yA,yB    = weather['Atlantic'], weather['Continental']
### smooth:
yA       = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB       = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')



#(1) Two-sample permutation test (comparing just the two largest groups):
nA,nB    = yA.shape[0], yB.shape[0]  #sample sizes
N        = nA+nB  #total number of responses
### original test statistic
t0       = here_tstat2(yA, yB)
### random label permutations:
np.random.seed(0)
nIter    = 1000
T        = []
y        = np.vstack((yA,yB))  #all responses (unlabeled)
for iii in range(nIter):
	ind      = np.random.permutation(N)
	i0,i1    = ind[:nA], ind[nA:]
	yyA,yyB  = y[i0], y[i1]
	T.append(  here_tstat2(yyA, yyB).max()  )  #t field maximum
### critical threshold:
alpha    = 0.05
tstar    = np.percentile(T, 100*(1-alpha))



#(2) Secondary permutation PDF (for cluster extent)
calc     = rft1d.geom.ClusterMetricCalculator()
k0       = calc.cluster_extents(t0, tstar, interp=True)  #original cluster metrics
nIter    = 1000
K        = []
for iii in range(nIter):
	ind      = np.random.permutation(N)
	i0,i1    = ind[:nA], ind[nA:]
	yyA,yyB  = y[i0], y[i1]
	t        = here_tstat2(yyA, yyB)
	k        = calc.cluster_extents(t, tstar, interp=True)
	K.append( max(k) )
K        = np.array(K)
### probabilities:
Pcluster = [(K>=kk).mean()  for kk in k0]



#(3) Plot:
pyplot.close('all')
ax     = pyplot.axes()
ax.plot(t0, 'k', lw=3, label='t field')
ax.plot([0,t.size], [tstar]*2, 'r--', label='Critical threshold')
### legend:
ax.legend(loc='upper left')
### cluster p values:
ax.text(10, 3.0,  'p = %.3f'%Pcluster[0])
ax.text(300, 3.6, 'p = %.3f'%Pcluster[1])
ax.text(280, 2.1, r'$\alpha$ = %.3f'%alpha, color='r')
### axis labels:
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
ax.set_title('Non-parametric RFT-like inference of weather dataset', size=20)
pyplot.show()
