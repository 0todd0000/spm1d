
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
yA,yB        = dataset.get_data()  #normal and fast walking





#(1) Compute confidence intervals:
np.random.seed(0)
alpha      = 0.05
iterations = -1
ci         = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='meanB')
cinp       = spm1d.stats.nonparam.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='meanB', iterations=iterations)
print( ci )
print( cinp )



#(2) Plot the CIs:
pyplot.close('all')
pyplot.figure(figsize=(10,4))

### plot parametric CI:
ax = pyplot.subplot(121)
ci.plot(ax)
ax.set_title('Parametric CI', size=10)
### plot parametric CI:
ax = pyplot.subplot(122)
cinp.plot(ax)
ax.set_title('Non-parametric CI', size=10)
pyplot.suptitle('Paired-sample CIs')
pyplot.show()

