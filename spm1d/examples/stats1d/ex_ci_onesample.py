
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()



#(1) Compute confidence interval:
ci         = spm1d.stats.ci_onesample(y)
print( ci )



#(2) Plot:
pyplot.close('all')
pyplot.figure(figsize=(6,4))
pyplot.get_current_fig_manager().window.move(0, 0)
ax     = pyplot.axes()
ci.plot(ax=ax)
spm1d.plot.plot_errorcloud(y.mean(axis=0), y.std(axis=0, ddof=1), ax=ax, facecolor='r', edgecolor='r', alpha=0.5, autoset_ylim=True)
pyplot.show()