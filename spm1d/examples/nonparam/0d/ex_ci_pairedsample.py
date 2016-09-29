
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset = spm1d.data.uv0d.cipaired.FraminghamSystolicBloodPressure()
yA,yB   = dataset.get_data()
print( dataset )
# yB += 1.9



#(1) Compute parametric and non-parametric confidence intervals:
np.random.seed(0)
alpha      = 0.05
mu         = 0
iterations = 1000
ci         = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='meanB')
cinp       = spm1d.stats.nonparam.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='meanB', iterations=iterations)
print( ci )
print( cinp )



#(2) Plot the CIs:
pyplot.close('all')
pyplot.figure(figsize=(8,4))

ax0 = pyplot.subplot(121);  ci.plot(ax0);    ax0.set_title('Parametric', size=10)
ax1 = pyplot.subplot(122);  cinp.plot(ax1);  ax1.set_title('Non-parametric', size=10)
pyplot.suptitle('One-sample CIs')
pyplot.show()
