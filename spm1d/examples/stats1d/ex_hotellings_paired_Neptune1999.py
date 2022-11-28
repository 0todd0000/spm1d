
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.hotellings_paired.Neptune1999kneekin()
YA,YB        = dataset.get_data()  #A:foot, B:speed
print( dataset )



#(1) Conduct test:
alpha        = 0.05
T2           = spm1d.stats.hotellings_paired(YA, YB)
T2i          = T2.inference(0.05)



#(2) Plot:
plt.close('all')
ax0     = plt.subplot(221)
ax1     = plt.subplot(222)
ax2     = plt.subplot(223)
ax3     = plt.subplot(224)
### plot SPM results:
h=ax0.plot(YA[:,:,0].T, 'k'); h[0].set_label('side-shuffle')
h=ax0.plot(YB[:,:,0].T, 'r'); h[0].set_label('v-cut')
ax1.plot(YA[:,:,1].T, 'k')
ax1.plot(YB[:,:,1].T, 'r')
ax2.plot(YA[:,:,2].T, 'k')
ax2.plot(YB[:,:,2].T, 'r')
T2i.plot(ax=ax3)
ax0.legend(fontsize=9)
plt.show()


