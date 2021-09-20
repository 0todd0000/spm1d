
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load a dataset containing a circular field:
dataset  = spm1d.data.uv1d.anova1.Weather()
Y,A      = dataset.get_data()
yA,yB    = Y[A==0], Y[A==2]  #Atlantic and Contintental regions



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
two_tailed = False
circular   = True
snpm       = spm1d.stats.nonparam.ttest2(yA, yB)
snpmi      = snpm.inference(alpha, two_tailed=two_tailed, iterations=1000, circular=circular)
print( snpmi )




#(2) Compare with parametric result:
spm        = spm1d.stats.ttest2(yA, yB)
spmi       = spm.inference(alpha, two_tailed=two_tailed, circular=circular)
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


