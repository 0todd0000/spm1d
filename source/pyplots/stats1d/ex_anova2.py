
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load data:
dataset      = spm1d.data.uv1d.anova2.Besier2009kneeflexion()
Y,A,B        = dataset.get_data()  #A:foot, B:speed
print dataset



#(1) ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2(Y, A, B, equal_var=False)
FFi          = [F.inference(0.05)   for F in FF]



#(2) Plot:
pyplot.close('all')
pyplot.figure(figsize=(10,3))
ax0     = pyplot.subplot(131)
ax1     = pyplot.subplot(132)
ax2     = pyplot.subplot(133)
### plot SPM results:
FFi[0].plot(ax=ax0);  ax0.set_title('Main effect: GENDER')
FFi[1].plot(ax=ax1);  ax1.set_title('Main effect: PAIN')
FFi[2].plot(ax=ax2);  ax2.set_title('Interaction effect')
pyplot.setp([ax0,ax1,ax2], ylim=(0, 15))
# pyplot.show()




