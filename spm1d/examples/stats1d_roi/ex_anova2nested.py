
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_2x2()
Y,A,B        = dataset.get_data()


#(0a) Create region of interest(ROI):
roi        = np.array([False]*Y.shape[1])
roi[40:55] = True



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2nested(Y, A, B, equal_var=True, roi=roi)
FFi          = [F.inference(alpha, interp=True)   for F in FF]


#(2) Plot results:
pyplot.close('all')
pyplot.subplot(221);  FFi[0].plot();  pyplot.title('Main effect A')
pyplot.subplot(222);  FFi[1].plot();  pyplot.title('Main effect B')
pyplot.show()





