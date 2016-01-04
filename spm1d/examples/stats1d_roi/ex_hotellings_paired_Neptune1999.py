
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.hotellings_paired.Neptune1999kneekin()
YA,YB        = dataset.get_data()  #A:foot, B:speed
print dataset



#(0a) Create region of interest(ROI):
roi        = np.array([False]*YA.shape[1])
roi[20:50] = True



#(1) Conduct test:
alpha        = 0.05
T2           = spm1d.stats.hotellings_paired(YA, YB, roi=roi)
T2i          = T2.inference(0.05)
print(T2i)



#(2) Plot:
pyplot.close('all')
ax0     = pyplot.subplot(221)
ax1     = pyplot.subplot(222)
ax2     = pyplot.subplot(223)
ax3     = pyplot.subplot(224)
### plot SPM results:
h=ax0.plot(YA[:,:,0].T, 'k'); h[0].set_label('side-shuffle')
h=ax0.plot(YB[:,:,0].T, 'r'); h[0].set_label('v-cut')
ax1.plot(YA[:,:,1].T, 'k')
ax1.plot(YB[:,:,1].T, 'r')
ax2.plot(YA[:,:,2].T, 'k')
ax2.plot(YB[:,:,2].T, 'r')
T2i.plot(ax=ax3)
ax0.legend(fontsize=9)
pyplot.show()


