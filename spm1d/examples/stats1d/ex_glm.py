
import numpy as np
import matplotlib.pyplot as plt
import spm1d


#(0) Load dataset:
dataset    = spm1d.data.uv1d.regress.SpeedGRF()
Y,x        = dataset.get_data()
# specify design matrix:
nCurves    = x.size
nFactors   = 4
X          = np.zeros((nCurves,nFactors))
X[:,0]     = x       #speed; the variable of interest
X[:,1]     = 1       #intercept
X[:,2]     = np.linspace(0,1,nCurves)   #linear drift
X[:,3]     = np.sin(np.linspace(0,np.pi,nCurves))  #sinusoidal drift
# specify a contrast vector:
c          = [1,0,0,0]  #speed (not the three other factors)



#(1) Conduct general linear test:
alpha      = 0.05
t          = spm1d.stats.glm(Y, X, c)
ti         = t.inference(alpha, two_tailed=False, interp=True)



#(2) Plot:
plt.close('all')
ax     = plt.axes()
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Time (%)')
plt.show()