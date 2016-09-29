
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()




#(1) Compare parametric and non-parametric CIs:
np.random.seed(0)
alpha      = 0.05
mu         = 0
iterations = -1
ci         = spm1d.stats.ci_onesample(y, alpha, mu=mu)
cinp       = spm1d.stats.nonparam.ci_onesample(y, alpha, mu=mu, iterations=iterations)
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
pyplot.suptitle('One-sample CIs')
pyplot.show()



