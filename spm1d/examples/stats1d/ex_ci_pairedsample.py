
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
yA,yB        = dataset.get_data()  #normal and fast walking





#(1) Compute confidence intervals:
alpha      = 0.05
ci         = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='difference', criterion='zero')
ciA        = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', criterion='meanB')
ciAB       = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', criterion='tailsAB')
ciAbad     = spm1d.stats.ci_onesample(yA, alpha)   #incorrect; for demonstration only
ciBbad     = spm1d.stats.ci_onesample(yB, alpha)   #incorrect; for demonstration only



#(2) Plot:
pyplot.close('all')
pyplot.figure(figsize=(14,7))
pyplot.get_current_fig_manager().window.move(0, 0)


### plot means and standard deviations:
ax     = pyplot.subplot(231)
spm1d.plot.plot_mean_sd(yA)
spm1d.plot.plot_mean_sd(yB, linecolor='r', facecolor='r', edgecolor='r')
ax.set_title('Means and SDs')


### plot hypothesis test results:
ax     = pyplot.subplot(232)
spmi   = spm1d.stats.ttest_paired(yA, yB).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_threshold_label()
ax.set_title('Hypothesis test')
ax.text(0.6, 0.2, 'Datum: zero\nCriterion:  $t ^*$', transform=ax.transAxes)


### plot confidence interval for mean paired difference:
ax     = pyplot.subplot(233)
ci.plot(ax=ax)
ax.set_title('CI for mean paired difference')
ax.text(0.1, 0.8, 'Datum="difference"\nCriterion="zero"', transform=ax.transAxes)


### plot confidence interval (datum=mean, criterion=mean):
ax     = pyplot.subplot(234)
ciA.plot(ax=ax)
ax.set_title('Paired CI (criterion: mean)')
ax.text(0.1, 0.5, 'Datum="meanA"\nCriterion="meanB"', transform=ax.transAxes)


### plot confidence interval (tail criterion)
ax     = pyplot.subplot(235)
ciAB.plot(ax=ax, linecolors=['k', 'r'], facecolors=['0.8', 'r'], edgecolors=['k','r'], alphas=[0.5,0.5])
ax.set_title('Paired CIs (criterion: tail)')
ax.text(0.1, 0.5, 'Datum="meanA"\nCriterion="tailsAB"', transform=ax.transAxes)


### plot confidence intervals for means (incorrect):
ax     = pyplot.subplot(236)
ciAbad.plot(ax=ax)
ciBbad.plot(ax=ax, linecolor='r', facecolor='r', edgecolor='r')
ax.set_title('Separate CIs for Groups A and B')
ax.text(0.5, 0.3, 'Incorrect approach!!', size=14, color='g', transform=ax.transAxes, ha='center')


pyplot.show()



