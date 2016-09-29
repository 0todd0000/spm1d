
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot



#(0) Set parameters:
np.random.seed(0)
nResponses    = 6
nIterations   = 10000
### derived parameters:
df            = nResponses - 1
sqrtN         = sqrt(nResponses)


#(1) Generate Gaussian data and compute test statistic:
T             = []
for i in range(nIterations):
	y         = np.random.randn(nResponses)
	t         = y.mean() / y.std(ddof=1) * sqrtN
	T.append(t)
T             = np.asarray(T)


#(2) Survival functions:
heights       = np.linspace(0, 5, 21)
sf            = np.array(  [ (T>h).mean()  for h in heights]  )
sfE           = stats.t.sf(heights, df)
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
ax.set_title('One-sample t validation (0D)', size=20)
pyplot.show()



