
import numpy as np
import matplotlib.pyplot as plt
import spm1d



# load dataset:
dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y,A     = dataset.get_data()
Y0      = Y[A==1]
Y1      = Y[A==2]
Y2      = Y[A==3]



# specify an arbitrary datum and an arbitrary error trajectory:
datum    = Y1.mean(axis=0)
err      = np.linspace(0.1, 2.5, datum.size)**2


# plot:
plt.close('all')
plt.plot(datum, 'b', lw=3)
spm1d.plot.plot_errorcloud(datum, err, facecolor='r', edgecolor='r')
plt.show()