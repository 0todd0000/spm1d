
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova3.SPM1D_ANOVA3_2x2x2()
# dataset      = spm1d.data.uv1d.anova3.SPM1D_ANOVA3_2x3x4()
Y,A,B,C      = dataset.get_data()



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova3(Y, A, B, C, equal_var=True)
FFi          = FF.inference(0.05)
print( FFi )



#(2) Plot results:
plt.close('all')
FFi.plot(plot_threshold_label=True, plot_p_values=True, autoset_ylim=True)
plt.show()


