
import numpy as np
from matplotlib import pyplot
import spm1d

#generate random data:
Y      = spm1d.util.get_dataset('random')


#conduct t test:
alpha  = 0.05
t      = spm1d.stats.ttest(Y)
ti     = t.inference(alpha, two_tailed=False)


#plot mean:
pyplot.close('all')
pyplot.figure( figsize=(8, 3.5) )
ax     = pyplot.axes( (0.1, 0.15, 0.35, 0.8) )
spm1d.plot.plot_mean_sd(Y)
ax.set_ylim(-1, 1)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Measurement domain (%)')
ax.set_ylabel('Dependent Variable')


#plot SPM results:
ax     = pyplot.axes((0.55,0.15,0.35,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
# ax.text(15, 4.05, r'p = %.3f' %spmi.p[0], size=9)  #you can alternatively use text to manually plot p values
ax.set_ylim(0, 4.5)
ax.set_xlabel('Measurement domain (%)')
# pyplot.show()