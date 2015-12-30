
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y,A          = dataset.get_data()


#(0a) Create region of interest(ROI):
roi        = np.array([False]*Y.shape[1])
roi[85:]   = True


#(1) Run ANOVA:
alpha        = 0.05
F            = spm1d.stats.anova1(Y, A, equal_var=True, roi=roi)
Fi           = F.inference(alpha, interp=True)
print Fi



#(2) Plot results:
pyplot.close('all')
# F.plot()
Fi.plot()
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
# pyplot.ylim(-1, 500)
pyplot.xlabel('Time (%)', size=20)
pyplot.title(r'Critical threshold at $\alpha$=%.2f:  $F^*$=%.3f' %(alpha, Fi.zstar))
pyplot.show()





