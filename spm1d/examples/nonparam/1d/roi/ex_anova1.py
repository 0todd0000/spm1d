
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load dataset:
dataset    = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
# dataset    = spm1d.data.uv1d.anova1.Weather()
y,A        = dataset.get_data()

#(0a) Create region of interest(ROI):
roi        = np.array( [False]*y.shape[1] )
roi[15:75] = True


#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpm       = spm1d.stats.nonparam.anova1(y, A, roi=roi)
snpmi      = snpm.inference(alpha, iterations=200)
print( snpmi )




#(2) Compare with parametric result:
spm        = spm1d.stats.anova1(y, A, equal_var=True, roi=roi)
spmi       = spm.inference(alpha)
print( spmi )




#(3) Plot
plt.close('all')
plt.figure(figsize=(10,4))

ax0 = plt.subplot(121)
ax1 = plt.subplot(122)
labels = 'Parametric', 'Non-parametric'
for ax,zi,label in zip([ax0,ax1], [spmi,snpmi], labels):
	zi.plot(ax=ax)
	zi.plot_threshold_label(ax=ax, fontsize=8)
	zi.plot_p_values(ax=ax, size=10)
	ax.set_title( label )
plt.tight_layout()
plt.show()

