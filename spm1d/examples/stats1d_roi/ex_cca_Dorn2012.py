
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.mv1d.cca.Dorn2012()
Y,x          = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(0a) Create region of interest(ROI):
roi        = np.array([False]*Y.shape[1])
roi[20:50] = True
roi[60:90] = True



#(1) Conduct test:
alpha        = 0.05
X2           = spm1d.stats.cca(Y, x, roi=roi)
X2i          = X2.inference(0.05)
print( X2i )


#(2) Plot:
plt.close('all')
# X2.plot()
X2i.plot()
X2i.plot_p_values()
plt.show()


