
from matplotlib import pyplot
import spm1d



# load dataset:
dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y,A     = dataset.get_data()
Y0      = Y[A==1]
Y1      = Y[A==2]
Y2      = Y[A==3]


# plot:
pyplot.close('all')
spm1d.plot.plot_mean_sd(Y0, linecolor='b', facecolor=(0.7,0.7,1), edgecolor='b', label='Slow')
spm1d.plot.plot_mean_sd(Y1, label='Normal')
spm1d.plot.plot_mean_sd(Y2, linecolor='r', facecolor=(1,0.7,0.7), edgecolor='r', label='Fast')
pyplot.xlim(0, 100)
pyplot.xlabel('Time (%)', size=20)
pyplot.ylabel(r'$\theta$ (deg)', size=20)
pyplot.legend(loc='lower left')
pyplot.show()