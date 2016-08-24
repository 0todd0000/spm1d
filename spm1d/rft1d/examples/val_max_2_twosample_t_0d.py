
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot



#(0) Set parameters:
np.random.seed(0)
nResponsesA   = 5
nResponsesB   = 5
nIterations   = 5000
### derived parameters:
nA,nB         = nResponsesA, nResponsesB
df            = nA + nB - 2


#(1) Generate Gaussian data and compute test statistic:
T             = []
for i in range(nIterations):
	yA,yB     = np.random.randn(nResponsesA), np.random.randn(nResponsesB)
	mA,mB     = yA.mean(), yB.mean()
	sA,sB     = yA.std(ddof=1), yB.std(ddof=1)
	s         = sqrt(    ((nA-1)*sA*sA + (nB-1)*sB*sB)  /  df     )
	t         = (mA-mB) / ( s *sqrt(1.0/nA + 1.0/nB))
	T.append(t)
T             = np.asarray(T)


#(2) Survival functions:
heights       = np.linspace(1, 4, 21)
sf            = np.array(  [ (T>h).mean()  for h in heights]  )
sfE           = stats.t.sf(heights, df) #theoretical
sfN           = stats.norm.sf(heights)  #standard normal (for comparison)


#(3) Plot results:
pyplot.close('all')
ax            = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.plot(heights, sfN, 'r-', label='Standard normal')
ax.set_xlabel('$u$', size=20)
ax.set_ylabel('$P (t > u)$', size=20)
ax.legend()
ax.set_title('Two-sample t validation (0D)', size=20)
pyplot.show()



