
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()



#(1) Compute confidence interval:
alpha      = 0.05
ci         = spm1d.stats.ci_onesample(y, alpha)
print( ci )



#(2) Plot:
pyplot.close('all')
pyplot.figure(figsize=(10,6))
pyplot.get_current_fig_manager().window.move(0, 0)


### plot means and standard deviations:
ax     = pyplot.subplot(221)
spm1d.plot.plot_mean_sd(y)
ax.axhline(0, color='k', linestyle='--')
ax.set_title('Mean and SD')


### plot hypothesis test results:
ax     = pyplot.subplot(222)
spmi   = spm1d.stats.ttest(y, mu).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_threshold_label()
ax.set_title('Hypothesis test')
# ax.text(0.6, 0.2, 'Datum: zero\nCriterion:  $t ^*$', transform=ax.transAxes)


### plot confidence interval:
ax     = pyplot.subplot(223)
ci.plot(ax=ax)
ax.set_title('Confidence Interval')
ax.text(0.1, 0.8, 'Datum="difference"\nCriterion="zero"', transform=ax.transAxes)


pyplot.show()