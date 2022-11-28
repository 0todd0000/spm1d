
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load dataset:
# dataset      = spm1d.data.mv1d.hotellings_paired.Neptune1999kneekin()
dataset      = spm1d.data.mv1d.hotellings_paired.Pataky2014cop()
yA,yB        = dataset.get_data()  #A:slow, B:fast
y            = yA - yB
mu           = 0

#(0a) Create region of interest(ROI):
roi        = np.array( [False]*yA.shape[1] )
roi[70:80] = True


#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpm       = spm1d.stats.nonparam.hotellings(y, mu, roi=roi)
snpmi      = snpm.inference(alpha, iterations=100)
print( snpmi )




#(2) Compare with parametric result:
spm        = spm1d.stats.hotellings(y, mu, roi=roi)
spmi       = spm.inference(alpha)
print( spmi )




#(3) Plot
plt.close('all')
plt.figure(figsize=(12,4))

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


