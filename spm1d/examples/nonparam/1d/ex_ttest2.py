
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
# dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
yB,yA        = dataset.get_data()  #normal and fast walking



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
two_tailed = True
snpm       = spm1d.stats.nonparam.ttest2(yA, yB)
snpmi      = snpm.inference(alpha, two_tailed=two_tailed, iterations=500)
print( snpmi )
print( snpmi.clusters )



#(2) Compare with parametric result:
spm        = spm1d.stats.ttest2(yA, yB)
spmi       = spm.inference(alpha, two_tailed=two_tailed)
print( spmi )
print( snpmi.clusters )



#(3) Plot
pyplot.close('all')
pyplot.figure(figsize=(12,4))

ax0 = pyplot.subplot(121)
ax1 = pyplot.subplot(122)
labels = 'Parametric', 'Non-parametric'
for ax,zi,label in zip([ax0,ax1], [spmi,snpmi], labels):
	zi.plot(ax=ax)
	zi.plot_threshold_label(ax=ax, fontsize=8)
	zi.plot_p_values(ax=ax, size=10)
	ax.set_title( label )
pyplot.show()


