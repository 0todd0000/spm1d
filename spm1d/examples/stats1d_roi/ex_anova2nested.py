
import numpy as np
import matplotlib.pyplot as plt
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
plt.close('all')
plt.subplot(221);  FFi[0].plot();  plt.title('Main effect A')
plt.subplot(222);  FFi[1].plot();  plt.title('Main effect B')
plt.show()





