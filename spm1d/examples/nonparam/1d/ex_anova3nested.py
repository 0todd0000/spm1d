
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load dataset:
# dataset      = spm1d.data.uv1d.anova3nested.SPM1D_ANOVA3NESTED_2x2x2()
dataset      = spm1d.data.uv1d.anova3nested.SPM1D_ANOVA3NESTED_2x4x2()
y,A,B,C      = dataset.get_data()


#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
FFn        = spm1d.stats.nonparam.anova3nested(y, A, B, C)
FFni       = FFn.inference(alpha, iterations=200)
print( FFni )



#(2) Compare with parametric result:
FF         = spm1d.stats.anova3nested(y, A, B, C, equal_var=True)
FFi        = FF.inference(alpha)
print( FFi )



#(3) Plot
pyplot.close('all')
pyplot.figure(figsize=(15,10))

for i,(Fi,Fni) in enumerate( zip(FFi,FFni) ):
	ax = pyplot.subplot(3,3,i+1)
	Fni.plot(ax=ax)
	Fni.plot_threshold_label(ax=ax, fontsize=8)
	Fni.plot_p_values(ax=ax, size=10)
	ax.axhline( Fi.zstar, color='orange', linestyle='--', label='Parametric threshold')
	if (Fi.zstar > Fi.z.max()) and (Fi.zstar>Fni.zstar):
		ax.set_ylim(0, Fi.zstar+1)
	if i==0:
		ax.legend(fontsize=10, loc='best')
	ax.set_title( Fni.effect )
pyplot.show()



#(3) Plot results:
pyplot.close('all')
FFni.plot(plot_threshold_label=False, plot_p_values=True, autoset_ylim=True)
### optionally plot parametric thresholds for comparison:
for i,Fi in enumerate(FFi):
	ax = pyplot.subplot(3,3,i+1)
	ax.axhline( Fi.zstar, color='c', linestyle='--' )
	ax.text(2, Fi.zstar, 'Parametric', color='c')
pyplot.show()
