
from math import sqrt
import itertools
import numpy as np
from scipy import stats
import spm1d
from matplotlib import pyplot



def hotellings(y, mu=None, signs=None):
	y       = np.asarray(y, dtype=float)
	nResponses,nComponents = y.shape
	yy      = y if mu is None else (y - mu)
	yy      = yy if signs is None else (signs * yy)
	m       = np.matrix( yy.mean(axis=0) )  #estimated mean
	W       = np.matrix( np.cov(yy.T, ddof=1) )  #estimated covariance
	T2      = nResponses * m * np.linalg.inv(W) * m.T
	return float(T2)


#(0) Load dataset:
# dataset = spm1d.data.mv0d.hotellings1.RSXLHotellings1()
dataset = spm1d.data.mv0d.hotellings1.Sweat()
y,mu    = dataset.Y, dataset.mu
y       = y[:5]


#(1) Compute original test statistic:
signs   = np.ones(y.shape)
z0      = hotellings(y, mu, signs)





#(2) Conduct non-parametric test:
nResponses,nComponents = y.shape
nTotal     = y.size
# nIter      = -1
nIter      = 1000
if nIter == -1:
	LABELS     = list(  itertools.product([0,1], repeat=nTotal)  )  #specify label signs (+ or -)
	Z          = []
	for labels in LABELS:
		signs  = (-2*np.array(labels) + 1).reshape( y.shape )
		z      = hotellings(y, mu, signs)
		Z.append( z )
else:
	Z          = []
	for i in range(nIter):
		labels = np.random.binomial(1, 0.5, nTotal)
		signs  = -2*np.array(labels) + 1
		signs  = signs.reshape( y.shape )
		yy     = signs * y.copy()
		z      = hotellings(yy)
		Z.append( z )

Z          = np.array(Z)

print(Z.min(), Z.max())

pyplot.close('all')
pyplot.figure(figsize=(8,6))
pyplot.get_current_fig_manager().window.move(0, 0)
ax = pyplot.axes()
ax.hist( Z, range(0,20) )
pyplot.show()


### conduct inference
p          = np.mean( Z > z0 )
# zstar      = np.percentile(Z, 100*(1-alpha))


#(3) Compare to parametric inference:
T2         = spm1d.stats.hotellings(y, mu)
T2i        = T2.inference(0.05)
zparam     = T2i.z
pparam     = T2i.p



### report results:
print 'Non-parametric test:'
print '   T2=%.3f, p=%.5f' %(z0, p)
print
print 'Parametric test:'
print '   T2=%.3f, p=%.5f' %(zparam, pparam)
print


