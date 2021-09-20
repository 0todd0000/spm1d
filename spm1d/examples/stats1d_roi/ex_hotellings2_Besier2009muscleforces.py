
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.hotellings2.Besier2009muscleforces()
YA,YB        = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(0a) Create region of interest(ROI):
roi        = np.array([False]*YA.shape[1])
roi[70:]   = True



#(1) Conduct test:
alpha        = 0.05
T2           = spm1d.stats.hotellings2(YA, YB, roi=roi)
T2i          = T2.inference(0.05)
print( T2i )


#(2) Plot:
plt.close('all')
T2i.plot()
plt.show()


