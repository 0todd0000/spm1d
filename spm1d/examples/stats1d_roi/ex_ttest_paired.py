
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
YA,YB        = dataset.get_data()  #normal and fast walking


#(0a) Create region of interest(ROI):
roi        = np.array([False]*YA.shape[1])
roi[0:10]  = True




#(1) Conduct t test:
alpha      = 0.05
t          = spm1d.stats.ttest_paired(YA, YB, roi=roi)
ti         = t.inference(alpha, two_tailed=False, interp=True)



#(2) Plot:
plt.close('all')
### plot mean and SD:
plt.figure( figsize=(8, 3.5) )
ax     = plt.axes( (0.1, 0.15, 0.35, 0.8) )
spm1d.plot.plot_mean_sd(YA)
spm1d.plot.plot_mean_sd(YB, linecolor='r', facecolor='r')
spm1d.plot.plot_roi(roi, facecolor='b', alpha=0.3)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Time (%)')
ax.set_ylabel('Plantar arch angle  (deg)')
### plot SPM results:
ax     = plt.axes((0.55,0.15,0.35,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Time (%)')
plt.show()
