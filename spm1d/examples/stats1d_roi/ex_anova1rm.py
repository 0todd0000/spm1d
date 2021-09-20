

import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova1rm.SpeedGRFcategoricalRM()
Y,A,SUBJ     = dataset.get_data()


#(0a) Create region of interest(ROI):
roi          = np.array([False]*Y.shape[1])
roi[70:]     = True



#(1) Run ANOVA:
alpha        = 0.05
equal_var    = True
F            = spm1d.stats.anova1(Y, A, equal_var, roi=roi)
Frm          = spm1d.stats.anova1rm(Y, A, SUBJ, equal_var, roi=roi)
Fi           = F.inference(alpha)
Firm         = Frm.inference(alpha)




#(2) Plot:
plt.close('all')
plt.figure( figsize=(8, 3.5) )
ax0     = plt.axes( (0.1, 0.15, 0.35, 0.8) )
ax1     = plt.axes((0.55,0.15,0.35,0.8))
### plot mean subject trajectories:
ax0.plot(Y[A==0].T, 'b')
ax0.plot(Y[A==1].T, 'k')
ax0.plot(Y[A==2].T, 'r')
### plot SPM results:
Firm.plot(ax=ax1, color='r', facecolor=(0.8,0.3,0.3), label='Within-subjects analysis')
Fi.plot(ax=ax1, label='Between-subjects analysis')
ax1.legend(fontsize=8)
plt.show()





