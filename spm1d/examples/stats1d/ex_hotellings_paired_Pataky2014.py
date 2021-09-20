
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.hotellings_paired.Pataky2014cop()
YA,YB        = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(1) Conduct test:
alpha        = 0.05
T2           = spm1d.stats.hotellings_paired(YA, YB)
T2i          = T2.inference(0.05)
print(T2i)


#(2) Plot:
plt.close('all')
ax0     = plt.subplot(221)
ax1     = plt.subplot(222)
ax3     = plt.subplot(224)
## plot SPM results:
ax0.plot(YA[:,:,0].T, 'k', label='slow')
ax0.plot(YB[:,:,0].T, 'r', label='fast')
ax1.plot(YA[:,:,1].T, 'k')
ax1.plot(YB[:,:,1].T, 'r')
T2i.plot(ax=ax3)
plt.show()


