

import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.mv1d.cca.Dorn2012()
Y,x          = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(1) Conduct test:
alpha        = 0.05
X2           = spm1d.stats.cca(Y, x)
X2i          = X2.inference(0.05)
print(X2i)


#(2) Plot:
plt.close('all')
X2i.plot()
X2i.plot_p_values()
plt.show()


