
from matplotlib import pyplot
import spm1d


# load dataset:
Y0,Y1,Y2     = spm1d.util.get_dataset('speed-kinematics-categorical')


#conduct SPM analysis:
alpha        = 0.05
t            = spm1d.stats.ttest_paired(Y1, Y2)
ti           = t.inference(alpha, two_tailed=True)


#plot means:
pyplot.close('all')
pyplot.figure(figsize=(8,3.5))
ax           = pyplot.axes((0.1,0.15,0.35,0.8))
spm1d.plot.plot_mean_sd(Y0, label='Normal')
spm1d.plot.plot_mean_sd(Y1, linecolor='r',facecolor=(1,0.7,0.7), edgecolor='r', label='Fast')
ax.set_xlabel('Time (%)')
ax.set_ylabel(r'$\Delta\theta$  (MF-MT)',fontsize=12)
ax.legend( loc='lower left', fontsize=9 )


#plot SPM results:
ax           = pyplot.axes((0.55,0.15,0.35,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ax.text(75, 4.7, r'p = %.3f' %ti.p[0], size=9)
ax.set_xlabel('Time (%)')
# pyplot.show()


