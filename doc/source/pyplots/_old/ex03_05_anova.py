import os
import numpy as np
from matplotlib import pyplot
import spm1d


subj         = 0   #subject number


# load walking speeds:
fname        = './data/ex_grf_speeds_cond.npy'
COND         = np.load(fname)[:,subj]   #conditions (1:slow, 2:normal, 3:fast)


# load GRF data:
fname        = './data/ex_grf_subj%03d.h5'%subj
Y            = spm1d.io.load(fname)
Y1,Y2,Y3     = Y[COND==1], Y[COND==2], Y[COND==3]


# conduct one-way ANOVA:
alpha        = 0.05
spm          = spm1d.stats.anova1( (Y1,Y2,Y3), equal_var=False )
spmi         = spm.inference(alpha)



# plot results:
spmi.plot()
spmi.plot_threshold_label(bbox=dict(facecolor='w'))
pyplot.ylim(-1, 500)
pyplot.xlabel('Time (%)', size=20)
pyplot.title(r'Critical threshold at $\alpha$=%.2f:  $F^*$=%.3f' %(alpha, spmi.zstar))