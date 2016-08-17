
from math import sqrt
import itertools
import numpy as np
from scipy import stats
import spm1d
from matplotlib import pyplot



def hotellings2(yA, yB):
	JA,JB     = yA.shape[0], yB.shape[0]
	yA,yB     = np.matrix(yA), np.matrix(yB)
	mA,mB     = yA.mean(axis=0), yB.mean(axis=0)  #means
	WA,WB     = np.cov(yA.T), np.cov(yB.T)
	W         = ((JA-1)*WA + (JB-1)*WB) / (JA+JB-2)
	T2        = (JA*JB)/float(JA+JB)  * (mB-mA) * np.linalg.inv(W) * (mB-mA).T
	return float(T2)


#(0) Load dataset:
#(0) Load dataset:
dataset = spm1d.data.mv0d.hotellings2.RSXLHotellings2()
# dataset = spm1d.data.mv0d.hotellings2.HELPHomeless()
yA,yB   = dataset.get_data()
# y       = y[:5]


#(1) Compute original test statistic:
# signs   = np.ones(y.shape)
z0      = hotellings2(yA, yB)
print z0




#
#
#
#
# #(2) Conduct non-parametric test:
# nResponses,nComponents = y.shape
# nTotal     = y.size
# # nIter      = -1
# nIter      = 1000
# if nIter == -1:
# 	LABELS     = list(  itertools.product([0,1], repeat=nTotal)  )  #specify label signs (+ or -)
# 	Z          = []
# 	for labels in LABELS:
# 		signs  = (-2*np.array(labels) + 1).reshape( y.shape )
# 		z      = hotellings(y, mu, signs)
# 		Z.append( z )
# else:
# 	Z          = []
# 	for i in range(nIter):
# 		labels = np.random.binomial(1, 0.5, nTotal)
# 		signs  = -2*np.array(labels) + 1
# 		signs  = signs.reshape( y.shape )
# 		yy     = signs * y.copy()
# 		z      = hotellings(yy)
# 		Z.append( z )
#
# Z          = np.array(Z)
#
# print(Z.min(), Z.max())
#
# pyplot.close('all')
# pyplot.figure(figsize=(8,6))
# pyplot.get_current_fig_manager().window.move(0, 0)
# ax = pyplot.axes()
# ax.hist( Z, range(0,20) )
# pyplot.show()
#
#
# ### conduct inference
# p          = np.mean( Z > z0 )
# # zstar      = np.percentile(Z, 100*(1-alpha))
#
#
# #(3) Compare to parametric inference:
# T2         = spm1d.stats.hotellings(y, mu)
# T2i        = T2.inference(0.05)
# zparam     = T2i.z
# pparam     = T2i.p
#
#
#
# ### report results:
# print 'Non-parametric test:'
# print '   T2=%.3f, p=%.5f' %(z0, p)
# print
# print 'Parametric test:'
# print '   T2=%.3f, p=%.5f' %(zparam, pparam)
# print


