import numpy as np
from matplotlib import pyplot
import spm1d

dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x2()
Y,A,B        = dataset.get_data()

FF           = spm1d.stats.anova2(Y, A, B, equal_var=True)
FFi          = FF.inference(0.05)

FFi.plot(plot_threshold_label=True, plot_p_values=True, autoset_ylim=True)