
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv1d.regress.SimulatedPataky2015c()
# dataset    = spm1d.data.uv1d.regress.SpeedGRF()
Y,x        = dataset.get_data()



#(1) Conduct regression:
alpha      = 0.05
t          = spm1d.stats.regress(Y, x)
ti         = t.inference(alpha, two_tailed=False, interp=True)



#(2) Plot:
pyplot.close('all')
ax     = pyplot.axes()
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Time (%)')
pyplot.show()


