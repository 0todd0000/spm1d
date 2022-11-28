
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x2()
Y,A,B        = dataset.get_data()


#(0a) Create region of interest(ROI):
roi        = np.array([False]*Y.shape[1])
roi[60:80] = True



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2(Y, A, B, equal_var=True, roi=roi)
FFi          = [F.inference(alpha)   for F in FF]


#(2) Plot results:
plt.close('all')
plt.subplot(221);  FFi[0].plot();  plt.title('Main effect A')
plt.subplot(222);  FFi[1].plot();  plt.title('Main effect B')
plt.subplot(223);  FFi[2].plot();  plt.title('Interaction effect AB')
plt.show()





