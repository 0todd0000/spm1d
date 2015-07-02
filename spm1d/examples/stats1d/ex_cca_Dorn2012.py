
import os
from matplotlib import pyplot
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.cca.Dorn2012()
Y,x          = dataset.get_data()  #A:slow, B:fast
print dataset



#(1) Conduct test:
alpha        = 0.05
X2           = spm1d.stats.cca(Y, x)
X2i          = X2.inference(0.05)



#(2) Plot:
pyplot.close('all')
X2i.plot()
X2i.plot_p_values()
pyplot.show()


