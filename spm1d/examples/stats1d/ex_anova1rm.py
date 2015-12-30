

import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova1rm.SpeedGRFcategoricalRM()
Y,A,SUBJ     = dataset.get_data()




#(1) Run ANOVA:
alpha        = 0.05
equal_var    = True
F            = spm1d.stats.anova1(Y, A, equal_var)
Frm          = spm1d.stats.anova1rm(Y, A, SUBJ, equal_var)
Fi           = F.inference(alpha)
Firm         = Frm.inference(alpha)




#(2) Plot:
pyplot.close('all')
pyplot.figure( figsize=(8, 3.5) )
ax0     = pyplot.axes( (0.1, 0.15, 0.35, 0.8) )
ax1     = pyplot.axes((0.55,0.15,0.35,0.8))
### plot mean subject trajectories:
ax0.plot(Y[A==0].T, 'b')
ax0.plot(Y[A==1].T, 'k')
ax0.plot(Y[A==2].T, 'r')
### plot SPM results:
Firm.plot(ax=ax1, color='r', thresh_color='r', facecolor=(0.8,0.3,0.3), label='Within-subjects analysis')
Fi.plot(ax=ax1, label='Between-subjects analysis')
ax1.legend(fontsize=8)
pyplot.show()





