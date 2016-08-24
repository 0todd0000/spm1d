
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d



#(0) Set parameters:
np.random.seed(1)
nResponsesA   = 8
nResponsesB   = 13
nComponents   = 3
nIterations   = 5000  #approximately 20000 iterations required for convergence
W0            = np.eye(nComponents)
### derived parameters:
nTotal        = nResponsesA + nResponsesB
df            = nComponents, float(nTotal-2)


#(1) Generate random data and compute test statistic:
T2            = []
JA,JB         = nResponsesA, nResponsesB
for i in range(nIterations):
	yA        = np.random.multivariate_normal(np.zeros(nComponents), W0, JA)
	yB        = np.random.multivariate_normal(np.zeros(nComponents), W0, JB)
	yA,yB     = np.matrix(yA), np.matrix(yB)
	mA,mB     = yA.mean(axis=0), yB.mean(axis=0)  #means
	WA,WB     = np.cov(yA.T), np.cov(yB.T)
	W         = ((JA-1)*WA + (JB-1)*WB) / (JA+JB-2)
	t2        = (JA*JB)/float(JA+JB)  * (mB-mA) * np.linalg.inv(W) * (mB-mA).T
	T2.append(float(t2))
T2            = np.asarray(T2)


#(2) Compute survival function:
heights       = np.linspace(4, 20, 21)
sf            = np.array(  [ (T2>h).mean()  for h in heights]  )
sfE           = rft1d.T2.sf0d(heights, df)


#(3) Plot results:
pyplot.close('all')
ax            = pyplot.axes()
ax.plot(heights, sf, 'o', label='Simulated')
ax.plot(heights, sfE, '-', label='Theoretical')
ax.set_xlabel('x', size=16)
ax.set_ylabel('P (T $^2$ > x)', size=16)
ax.legend()
ax.set_title("Two-sample Hotelling's T2 validation (0D)", size=20)
pyplot.show()

