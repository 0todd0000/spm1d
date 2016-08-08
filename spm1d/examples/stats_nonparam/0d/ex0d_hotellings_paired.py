
import numpy as np
import scipy.stats
import spm1d
import spm1d



#(0) Load dataset:
dataset = spm1d.data.mv0d.hotellings_paired.NCSSBeforeAfter()
# dataset = spm1d.data.mv0d.hotellings_paired.RSXLHotellingsPaired()
yA,yB   = dataset.get_data()
# yA,yB   = [y[:10]  for y in [yA,yB]]


#(1) Conduct non-parametric test:
np.random.seed(10)
alpha      = 0.05
T2         = spm1d.stats.nonparam.hotellings_paired(yA, yB)
T2i        = T2.inference(alpha, iterations=1000)


# from matplotlib import pyplot
# pyplot.close('all')
# pyplot.figure(figsize=(8,6))
# pyplot.get_current_fig_manager().window.move(0, 0)
# ax = pyplot.axes()
# Z  = T2i.permuter.Z
# ax.hist( Z, range=(0,25) )
# pyplot.show()
#


#(3) Compare to parametric inference:
T2param    = spm1d.stats.hotellings_paired(yA, yB)
T2parami   = T2param.inference(0.05)
zparam     = T2parami.z
pparam     = T2parami.p



### report results:
print 'Non-parametric test:'
print '   T2=%.3f, p=%.5f' %(T2i.z, T2i.p)
print
print 'Parametric test:'
print '   T2=%.3f, p=%.5f' %(zparam, pparam)
print

