
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.manova1.Dorn2012()
Y,A          = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(0a) Create region of interest(ROI):
roi        = np.array([False]*Y.shape[1])
roi[60:90] = True



#(1) Conduct test:
alpha        = 0.05
X2           = spm1d.stats.manova1(Y, A, roi=roi)
X2i          = X2.inference(0.05)
print( X2i )


#(2) Plot:
plt.close('all')
X2i.plot()
X2i.plot_p_values()
plt.show()


