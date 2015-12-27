
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.hotellings_paired.Pataky2014cop()
YA,YB        = dataset.get_data()  #A:slow, B:fast
print dataset



#(0a) Create region of interest(ROI):
roi        = np.array([False]*YA.shape[1])
roi[50:80] = True



#(1) Conduct test:
alpha        = 0.05
T2           = spm1d.stats.hotellings_paired(YA, YB, roi=roi)
T2i          = T2.inference(0.05)



#(2) Plot:
pyplot.close('all')
ax0     = pyplot.subplot(221)
ax1     = pyplot.subplot(222)
ax3     = pyplot.subplot(224)
## plot SPM results:
ax0.plot(YA[:,:,0].T, 'k', label='slow')
ax0.plot(YB[:,:,0].T, 'r', label='fast')
ax1.plot(YA[:,:,1].T, 'k')
ax1.plot(YB[:,:,1].T, 'r')
T2i.plot(ax=ax3)
pyplot.show()


