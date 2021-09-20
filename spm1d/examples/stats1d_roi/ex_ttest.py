
import numpy as np
import matplotlib.pyplot as plt
import spm1d


#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
Y,mu       = dataset.get_data()


#(0a) Create region of interest(ROI):
roi        = np.array([False]*Y.shape[1])
roi[70:80] = True



#(1) Conduct t test:
alpha      = 0.05
t          = spm1d.stats.ttest(Y, mu, roi=roi)
ti         = t.inference(alpha, two_tailed=False, interp=True)


#(2) Plot:
plt.close('all')
plt.figure( figsize=(8, 3.5) )
### plot mean and SD:
ax     = plt.axes( (0.1, 0.15, 0.35, 0.8) )
spm1d.plot.plot_mean_sd(Y, roi=roi)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Measurement domain (%)')
ax.set_ylabel('Dependent Variable')
### plot SPM results:
ax     = plt.axes((0.55,0.15,0.35,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])	
ax.set_xlabel('Measurement domain (%)')
plt.show()