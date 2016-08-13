
import numpy as np
from matplotlib import pyplot
import spm1d



# #(0) Load dataset:
# # dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
# dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
# yB,yA        = dataset.get_data()

yA = np.array([ 47.4, 59.9, 51.0, 55.1, 63.1, 57.0, 49.6, 57.9, 55.8, 52.8, 52.9, 56.0, 44.1, 66.9, 50.6, 54.0, 58.9, 57.4, 57.9, 63.8, 58.4, 49.2, 55.8, 60.0, 60.7, 58.3, 50.4, 58.1, 44.9, 52.8, 55.5, 63.4, 46.7, 59.6, 55.9, 59.3, 54.7, 50.6, 54.0, 57.4, 57.7, 47.8, 57.3, 55.5, 50.7, 60.7, 57.1 ])
yB = np.array([ 64.6, 61.6, 61.0, 49.6, 49.7, 53.0, 57.4, 61.7, 54.7, 53.7, 57.2, 56.5, 46.3, 54.6, 50.8, 65.6, 57.4, 62.6, 52.7, 55.6, 57.1, 57.7, 59.9, 52.8, 52.5, 49.1, 53.9, 62.8, 61.1, 55.2, 55.7, 53.1, 58.2, 61.9, 67.6, 61.3, 58.8, 49.5, 57.4, 55.2, 65.2, 48.5, 47.3, 60.9])



#(1) Compute confidence intervals:
alpha      = 0.05
ci         = spm1d.stats.ci_twosample(yA, yB, alpha, datum='difference', criterion='zero')
print( ci )

# ciA        = spm1d.stats.ci_twosample(yA, yB, alpha, datum='meanA', criterion='meanB')
# ciAB       = spm1d.stats.ci_twosample(yA, yB, alpha, datum='meanA', criterion='tailsAB')
# ciAbad     = spm1d.stats.ci_onesample(yA, alpha)   #incorrect; for demonstration only
# ciBbad     = spm1d.stats.ci_onesample(yB, alpha)   #incorrect; for demonstration only
#

