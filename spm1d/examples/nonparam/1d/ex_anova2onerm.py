
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_2x2()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_2x3()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_3x3()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_3x4()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_3x5()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_4x4()
# dataset      = spm1d.data.uv1d.anova2onerm.SPM1D_ANOVA2ONERM_4x5()
y,A,B,SUBJ   = dataset.get_data()



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
FFn        = spm1d.stats.nonparam.anova2onerm(y, A, B, SUBJ)
FFni       = FFn.inference(alpha, iterations=200)
print( FFni )



#(2) Compare with parametric result:
FF         = spm1d.stats.anova2onerm(y, A, B, SUBJ, equal_var=True)
FFi        = FF.inference(alpha)
print( FFi )



#(3) Plot results:
pyplot.close('all')
FFni.plot(plot_threshold_label=True, plot_p_values=True, autoset_ylim=True)
### optionally plot parametric thresholds for comparison:
for i,Fi in enumerate(FFi):
	ax = pyplot.subplot(2,2,i+1)
	ax.axhline( Fi.zstar, color='c', linestyle='--' )
	ax.text(2, Fi.zstar, 'Parametric', color='c')
pyplot.show()


