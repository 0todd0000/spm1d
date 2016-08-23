
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



# #(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
FFn        = spm1d.stats.nonparam.anova2onerm(y, A, B, SUBJ)
FFni       = FFn.inference(alpha, iterations=200)
print( FFni )



#(2) Compare with parametric result:
FF         = spm1d.stats.anova2onerm(y, A, B, SUBJ, equal_var=True)
FFi        = FF.inference(alpha)
print( FFi )



#(3) Plot
pyplot.close('all')
pyplot.figure(figsize=(15,4))
pyplot.get_current_fig_manager().window.move(0, 0)
for i,(Fi,Fni) in enumerate( zip(FFi,FFni) ):
	ax = pyplot.subplot(1,3,i+1)
	Fni.plot(ax=ax)
	Fni.plot_threshold_label(ax=ax, fontsize=8)
	Fni.plot_p_values(ax=ax, size=10)
	ax.axhline( Fi.zstar, color='orange', linestyle='--', label='Parametric threshold')
	if Fi.zstar > Fi.z.max():
		ax.set_ylim(0, Fi.zstar+1)
	if i==0:
		ax.legend(fontsize=10, loc='best')
pyplot.show()




