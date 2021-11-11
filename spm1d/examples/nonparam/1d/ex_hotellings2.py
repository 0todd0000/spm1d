
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.mv1d.hotellings2.Besier2009muscleforces()
yA,yB        = dataset.get_data()  #A:slow, B:fast



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpm       = spm1d.stats.nonparam.hotellings2(yA, yB)
snpmi      = snpm.inference(alpha, iterations=1000)
print( snpmi )




#(2) Compare with parametric result:
spm        = spm1d.stats.hotellings2(yA, yB)
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


