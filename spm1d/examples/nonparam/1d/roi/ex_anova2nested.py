
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_2x2()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_2x3()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_3x3()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_3x4()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_3x5()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_4x4()
# dataset      = spm1d.data.uv1d.anova2nested.SPM1D_ANOVA2NESTED_4x5()
y,A,B        = dataset.get_data()

#(0a) Create region of interest(ROI):
roi        = np.array( [False]*y.shape[1] )
roi[25:45] = True



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
FFn        = spm1d.stats.nonparam.anova2nested(y, A, B, roi=roi)
FFni       = FFn.inference(alpha, iterations=500)
print( FFni )



#(2) Compare with parametric result:
FF         = spm1d.stats.anova2nested(y, A, B, equal_var=True, roi=roi)
FFi        = FF.inference(alpha)
print( FFi )



#(3) Plot
plt.close('all')
plt.figure(figsize=(12,4))

for i,(Fi,Fni) in enumerate( zip(FFi,FFni) ):
	ax = plt.subplot(1,3,i+1)
	Fni.plot(ax=ax)
	Fni.plot_threshold_label(ax=ax, fontsize=8)
	Fni.plot_p_values(ax=ax, size=10)
	ax.axhline( Fi.zstar, color='orange', linestyle='--', label='Parametric threshold')
	if (Fi.zstar > Fi.z.max()) and (Fi.zstar>Fni.zstar):
		ax.set_ylim(0, Fi.zstar+1)
	if i==0:
		ax.legend(fontsize=10, loc='best')
	ax.set_title( Fni.effect )
plt.tight_layout()
plt.show()




