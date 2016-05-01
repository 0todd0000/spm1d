
import numpy as np
from matplotlib import pyplot
import spm1d


# load dataset:
subj         = 0
Y,x          = spm1d.util.get_dataset('speed-grf', subj)  #data to be tested
Y0,Y1,Y2     = spm1d.util.get_dataset('speed-grf-categorical', subj) #data for plotting categorical means


#conduct SPM analysis:
alpha        = 0.05
t            = spm1d.stats.regress(Y, x)
ti           = t.inference(alpha)


#plot maximum GRF:
pyplot.close('all')
pyplot.figure(figsize=(12,3))
ax           = pyplot.axes((0.05,0.15,0.27,0.8))
ax.plot(x, Y.max(axis=1), '.')
ax.set_xlabel('Time (% stance)', fontsize=9)
ax.set_ylabel('Maximum GRF  (BW)', fontsize=9)
pyplot.setp(ax.get_xticklabels() + ax.get_xticklabels(), fontsize=7)


#plot mean curves:
ax           = pyplot.axes((0.38,0.15,0.27,0.8))
spm1d.plot.plot_mean_sd(Y0, linecolor='b', facecolor=(0.7,0.7,1), edgecolor='b', label='Slow')
spm1d.plot.plot_mean_sd(Y1, label='Normal')
spm1d.plot.plot_mean_sd(Y2, linecolor='r', facecolor=(1,0.7,0.7), edgecolor='r', label='Fast')
ax.set_xlabel('Time (% stance)', fontsize=9)
ax.set_ylabel('GRF  (BW)', fontsize=9)
ax.legend(  loc='lower center', fontsize=7 )
pyplot.setp(ax.get_xticklabels() + ax.get_xticklabels(), fontsize=7)


#plot SPM results:
ax           = pyplot.axes((0.72,0.15,0.27,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8, bbox=dict(facecolor='w'))
ti.plot_p_values(size=6)
ax.set_xlabel('Time (%)', fontsize=9)
pyplot.setp(ax.get_xticklabels() + ax.get_xticklabels(), fontsize=7)
# pyplot.show()

