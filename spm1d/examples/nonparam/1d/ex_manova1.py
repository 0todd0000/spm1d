
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load data:
dataset      = spm1d.data.mv1d.manova1.Dorn2012()
y,A          = dataset.get_data()  #A:slow, B:fast
# print( dataset )
'''
The parametric and non-parametric results will disagree
if the dataset is quite small relative to the number of
vector components. Artificially doubling the data size
as follows will cause closer agreement between parametric
and non-parametric results:

import numpy as np
y,A          = np.vstack([y,y]), np.hstack([A,A])
'''



#(1) Conduct non-parametric test:
np.random.seed(0)
X2n     = spm1d.stats.nonparam.manova1(y, A)
X2ni    = X2n.inference(alpha=0.05, iterations=200)
print( 'Non-parametric test:')
print( X2ni)



#(2) Compare to parametric test:
alpha        = 0.05
X2           = spm1d.stats.manova1(y, A)
X2i          = X2.inference(0.05)



#(3) Plot
pyplot.close('all')
pyplot.figure(figsize=(12,4))

ax0 = pyplot.subplot(121)
ax1 = pyplot.subplot(122)
labels = 'Parametric', 'Non-parametric'
for ax,zi,label in zip([ax0,ax1], [X2i,X2ni], labels):
	zi.plot(ax=ax)
	zi.plot_threshold_label(ax=ax, fontsize=8)
	zi.plot_p_values(ax=ax, size=10)
	ax.set_title( label )
pyplot.show()
