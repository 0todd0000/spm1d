
import numpy as np
from matplotlib import pyplot
import spm1d


#load dataset:
Y,x          = spm1d.util.get_dataset('speed-grf', 0)  #subject "0"


# specify design matrix:
nCurves      = len(Y)
nFactors     = 4
X            = np.zeros((nCurves,nFactors))
X[:,0]       = x       #speed; the variable of interest
X[:,1]       = 1       #intercept
X[:,2]       = np.linspace(0,1,nCurves)   #linear drift
X[:,3]       = np.sin(np.linspace(0,np.pi,nCurves))  #sinusoidal drift


# specify a contrast vector:
c            = [1,0,0,0]  #we are interested only in speed (not the three other factors)


# run SPM:
alpha        = 0.05
t            = spm1d.stats.glm(Y, X, c)
ti           = t.inference(alpha)


# plot deisgn matrix:
pyplot.close('all')
pyplot.figure(figsize=(8,3))
pyplot.axes((0.05,0.15,0.3,0.8))
t.plot_design(factor_labels=['speed','y0','driftA','driftB'])


# plot SPM results:
ax            = pyplot.axes((0.45,0.15,0.5,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8, bbox=dict(facecolor='w'))
ti.plot_p_values(size=6)
ax.set_xlabel('Time (%)', fontsize=9)
pyplot.setp(ax.get_xticklabels() + ax.get_yticklabels(),fontsize=7)
# pyplot.show()
