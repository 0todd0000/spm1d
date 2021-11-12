
import numpy as np
import spm1d



#(0) Load dataset:
# dataset = spm1d.data.mv0d.hotellings1.RSXLHotellings1()
dataset = spm1d.data.mv0d.hotellings1.Sweat()
y,mu    = dataset.Y, dataset.mu
# y       = y[:10]


#(1) Conduct non-parametric test:
np.random.seed(10)
alpha      = 0.05
T2         = spm1d.stats.nonparam.hotellings(y, mu)
T2i        = T2.inference(alpha, iterations=1000)


#(2) Compare to parametric result:
T2param    = spm1d.stats.hotellings(y, mu)
T2parami   = T2param.inference(alpha)
zparam     = T2parami.z
pparam     = T2parami.p



### report results:
print( 'Non-parametric test:' )
print( '   T2=%.3f, p=%.5f' %(T2i.z, T2i.p) ) 
print
print( 'Parametric test:' )
print( '   T2=%.3f, p=%.5f' %(zparam, pparam) ) 
print


