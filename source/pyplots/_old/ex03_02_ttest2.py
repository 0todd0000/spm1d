
from matplotlib import pyplot
import spm1d


# load Matlab data:
fname        = './data/ex_kinematics.mat'
Y            = spm1d.io.loadmat(fname)   #30 curves, 100 nodesY0 = Y[10:20]   #normal walking (second 10 curves)
Y0           = Y[10:20]   #normal walking (second 10 curves)
Y1           = Y[20:]     #fast walking (final 10 curves)



#conduct SPM analysis:
alpha        = 0.05
spm          = spm1d.stats.ttest2(Y0, Y1, equal_var=True)
spmi         = spm.inference(alpha, two_tailed=True)


#plot means:
pyplot.figure(figsize=(8,3.5))
ax           = pyplot.axes((0.1,0.15,0.35,0.8))
spm1d.plot.plot_mean_sd(Y0, label='Normal')
spm1d.plot.plot_mean_sd(Y1, linecolor='r',facecolor=(1,0.7,0.7), edgecolor='r', label='Fast')
ax.set_xlabel('Time (%)')
ax.set_ylabel(r'$\Delta\theta$  (MF-MT)',fontsize=12)
ax.legend( loc='lower left', fontsize=9 )

#plot SPM results:
ax           = pyplot.axes((0.55,0.15,0.35,0.8))
spmi.plot()
spmi.plot_threshold_label(fontsize=8)
ax.text(75, 4.7, r'p = %.3f' %spmi.p[0], size=9)
ax.set_xlabel('Time (%)')

