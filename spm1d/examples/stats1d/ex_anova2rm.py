
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova2rm.SPM1D_ANOVA2RM_2x2()
# dataset      = spm1d.data.uv1d.anova2rm.SPM1D_ANOVA2RM_2x3()
# dataset      = spm1d.data.uv1d.anova2rm.SPM1D_ANOVA2RM_3x3()
# dataset      = spm1d.data.uv1d.anova2rm.SPM1D_ANOVA2RM_3x4()
# dataset      = spm1d.data.uv1d.anova2rm.SPM1D_ANOVA2RM_3x5()
# dataset      = spm1d.data.uv1d.anova2rm.SPM1D_ANOVA2RM_4x4()
# dataset      = spm1d.data.uv1d.anova2rm.SPM1D_ANOVA2RM_4x5()
Y,A,B,SUBJ   = dataset.get_data()



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2rm(Y, A, B, SUBJ, equal_var=True)
FFi          = [F.inference(alpha)   for F in FF]


#(2) Plot results:
pyplot.close('all')
pyplot.subplot(221);  FFi[0].plot();  pyplot.title('Main effect A')
pyplot.subplot(222);  FFi[1].plot();  pyplot.title('Main effect B')
pyplot.subplot(223);  FFi[2].plot();  pyplot.title('Interaction effect AB')
pyplot.show()





