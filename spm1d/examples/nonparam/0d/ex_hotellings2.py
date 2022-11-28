
import numpy as np
import spm1d



#(0) Load dataset:
# dataset = spm1d.data.mv0d.hotellings2.RSXLHotellings2()
dataset = spm1d.data.mv0d.hotellings2.HELPHomeless()
yA,yB   = dataset.get_data()
# yA,yB   = [y[:10]  for y in [yA,yB]]



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
T2         = spm1d.stats.nonparam.hotellings2(yA, yB)
T2i        = T2.inference(alpha, iterations=1000)


#(2) Compare to parametric inference:
T2param    = spm1d.stats.hotellings2(yA, yB)
T2parami   = T2param.inference(0.05)
zparam     = T2parami.z
pparam     = T2parami.p



### report results:
print( 'Non-parametric test:' )
print( '   T2=%.3f, p=%.5f' %(T2i.z, T2i.p) ) 
print
print( 'Parametric test:' )
print( '   T2=%.3f, p=%.5f' %(zparam, pparam) ) 
print

