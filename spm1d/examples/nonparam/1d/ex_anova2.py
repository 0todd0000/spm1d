
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x2()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x3()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x3()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x4()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x5()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_4x4()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_4x5()
y,A,B        = dataset.get_data()



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
FFn        = spm1d.stats.nonparam.anova2(y, A, B)
FFni       = FFn.inference(alpha, iterations=500)
print( FFni )



#(2) Compare with parametric result:
FF         = spm1d.stats.anova2(y, A, B, equal_var=True)
FFi        = FF.inference(alpha)
print( FFi )



#(3) Plot results:
plt.close('all')
plt.figure( figsize=(10,6) )
FFni.plot(plot_threshold_label=True, plot_p_values=True, autoset_ylim=True)
### optionally plot parametric thresholds for comparison:
for i,Fi in enumerate(FFi):
	ax = plt.subplot(2,2,i+1)
	ax.axhline( Fi.zstar, color='c', linestyle='--' )
	ax.text(2, Fi.zstar, 'Parametric', color='c')
plt.tight_layout()
plt.show()



