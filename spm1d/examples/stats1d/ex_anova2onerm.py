
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_2x2()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_2x3()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_3x3()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_3x4()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_3x5()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_4x4()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_4x5()
Y,A,B,SUBJ   = dataset.get_data()



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2onerm(Y, A, B, SUBJ, equal_var=True)
FFi          = FF.inference(0.05)
print( FFi )



#(2) Plot results:
plt.close('all')
FFi.plot(plot_threshold_label=True, plot_p_values=True)
plt.show()



