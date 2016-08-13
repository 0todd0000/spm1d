
import numpy as np
from matplotlib import pyplot
import spm1d



#(0) Load dataset:
# dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
yB,yA        = dataset.get_data()



#(1) Compute confidence intervals:
alpha      = 0.05
ci         = spm1d.stats.ci_twosample(yA, yB, alpha, datum='difference', criterion='zero')
ciA        = spm1d.stats.ci_twosample(yA, yB, alpha, datum='meanA', criterion='meanB')
ciAB       = spm1d.stats.ci_twosample(yA, yB, alpha, datum='meanA', criterion='tailsAB')
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
spmi   = spm1d.stats.ttest2(yA, yB).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_threshold_label()
ax.set_title('Hypothesis test')
ax.text(0.3, 0.1, 'Datum: zero\nCriterion:  $t ^*$', transform=ax.transAxes, bbox=dict(color='w', alpha=0.8))


### plot confidence interval for mean paired difference:
ax     = pyplot.subplot(233)
ci.plot(ax=ax)
ax.set_title('CI for mean difference')
ax.text(0.3, 0.1, 'Datum="difference"\nCriterion="zero"', transform=ax.transAxes, bbox=dict(color='w', alpha=0.8))


### plot confidence interval (datum=mean, criterion=mean):
ax     = pyplot.subplot(234)
ciA.plot(ax=ax)
# ax.plot(  yB.mean(axis=0), color='r', lw=3 )
ax.set_title('Group A CI (criterion: Group B mean)')
ax.text(0.3, 0.1, 'Datum="meanA"\nCriterion="meanB"', transform=ax.transAxes, bbox=dict(color='w', alpha=0.8))


### plot confidence interval (tail criterion)
ax     = pyplot.subplot(235)
ciAB.plot(ax=ax, linecolors=['k', 'r'], facecolors=['0.8', 'r'], edgecolors=['k','r'], alphas=[0.5,0.5])
ax.set_title('CIs (criterion: tail)')
ax.text(0.3, 0.1, 'Datum="meanA"\nCriterion="tailsAB"', transform=ax.transAxes, bbox=dict(color='w', alpha=0.8))


### plot confidence intervals for means (incorrect):
ax     = pyplot.subplot(236)
ciAbad.plot(ax=ax)
ciBbad.plot(ax=ax, linecolor='r', facecolor='r', edgecolor='r')
ax.set_title('Separate CIs for Groups A and B')
ax.text(0.3, 0.1, 'Incorrect approach!!', size=14, color='g', transform=ax.transAxes, bbox=dict(color='w', alpha=0.8))


pyplot.show()