
from matplotlib import pyplot
import spm1d


#(0) Load dataset:
# dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
Y,mu       = dataset.get_data()


#(1) Conduct t test:
alpha      = 0.05
t          = spm1d.stats.ttest(Y, mu)
ti         = t.inference(alpha, two_tailed=False, interp=True, circular=True)
print( ti )



#(2) Plot:
pyplot.close('all')
### plot mean and SD:
pyplot.figure( figsize=(8, 3.5) )
ax     = pyplot.axes( (0.1, 0.15, 0.35, 0.8) )
spm1d.plot.plot_mean_sd(Y)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Measurement domain (%)')
ax.set_ylabel('Dependent Variable')
### plot SPM results:
ax     = pyplot.axes((0.55,0.15,0.35,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Measurement domain (%)')
pyplot.show()