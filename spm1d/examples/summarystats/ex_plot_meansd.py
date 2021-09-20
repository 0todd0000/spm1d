
import matplotlib.pyplot as plt
import spm1d



# load dataset:
dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y,A     = dataset.get_data()
Y0      = Y[A==1]
Y1      = Y[A==2]
Y2      = Y[A==3]


# plot:
plt.close('all')
spm1d.plot.plot_mean_sd(Y0, linecolor='b', facecolor=(0.7,0.7,1), edgecolor='b', label='Slow')
spm1d.plot.plot_mean_sd(Y1, label='Normal')
spm1d.plot.plot_mean_sd(Y2, linecolor='r', facecolor=(1,0.7,0.7), edgecolor='r', label='Fast')
plt.xlim(0, 100)
plt.xlabel('Time (%)', size=20)
plt.ylabel('VGRF  (BW)', size=20)
plt.legend(loc='lower left')
plt.show()