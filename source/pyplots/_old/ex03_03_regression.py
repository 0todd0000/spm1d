
print
print

import numpy as np
from matplotlib import pyplot
import spm1d


subj         = 0   #subject number


# load walking speeds:
fnameX0      = './data/ex_grf_speeds_cond.npy'
fnameX1      = './data/ex_grf_speeds.npy'
COND         = np.load(fnameX0)[:,subj]   #conditions (1:slow, 2:normal, 3:fast)
SPEED        = np.load(fnameX1)[:,subj]   #speed (m/s)  (measured)
# load GRF data:
fnameY       = './data/ex_grf_subj%03d.h5' %subj
Y            = spm1d.io.load(fnameY)



#conduct SPM analysis:
alpha        = 0.05
spm          = spm1d.stats.regress(Y, SPEED)
spmi         = spm.inference(alpha)


#plot maximum GRF:
pyplot.close('all')
pyplot.figure(figsize=(12,3))
ax           = pyplot.axes((0.05,0.15,0.27,0.8))
ax.plot(SPEED, Y.max(axis=1), '.')
ax.set_xlabel('Time (% stance)', fontsize=9)
ax.set_ylabel('Maximum GRF  (BW)', fontsize=9)
pyplot.setp(ax.get_xticklabels() + ax.get_xticklabels(), fontsize=7)


#plot mean curves:
ax           = pyplot.axes((0.38,0.15,0.27,0.8))
YA,YB,YC     = Y[COND==1], Y[COND==2], Y[COND==3]
spm1d.plot.plot_mean_sd(YA, linecolor='b', facecolor=(0.7,0.7,1), edgecolor='b', label='Slow')
spm1d.plot.plot_mean_sd(YB, label='Normal')
spm1d.plot.plot_mean_sd(YC, linecolor='r', facecolor=(1,0.7,0.7), edgecolor='r', label='Slow')
ax.set_xlabel('Time (% stance)', fontsize=9)
ax.set_ylabel('GRF  (BW)', fontsize=9)
ax.legend(  loc='lower center', fontsize=7 )
pyplot.setp(ax.get_xticklabels() + ax.get_xticklabels(), fontsize=7)


#plot SPM results:
ax           = pyplot.axes((0.72,0.15,0.27,0.8))
spmi.plot()
spmi.plot_threshold_label(fontsize=8)
ax.set_xlabel('Time (%)', fontsize=9)
pyplot.setp(ax.get_xticklabels() + ax.get_xticklabels(), fontsize=7)



