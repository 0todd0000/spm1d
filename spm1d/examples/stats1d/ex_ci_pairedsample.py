
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
yA,yB        = dataset.get_data()  #normal and fast walking





#(1) Compute confidence intervals:
alpha      = 0.05
ci0        = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='difference', mu=0)
ci1        = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='meanB')
ci2        = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='tailB')
print( ci0 )
print( ci1 )
print( ci2 )
### compute incorrect CIs for demonstration:
ciA_bad    = spm1d.stats.ci_onesample(yA, alpha)
ciB_bad    = spm1d.stats.ci_onesample(yB, alpha)




#(2) Plot:
plt.close('all')
plt.figure(figsize=(14,7))



### plot means and standard deviations:
ax     = plt.subplot(231)
spm1d.plot.plot_mean_sd(yA)
spm1d.plot.plot_mean_sd(yB, linecolor='r', facecolor='r', edgecolor='r')
spm1d.plot.legend_manual(ax, labels=['Group A', 'Group B', 'Mean', 'SD'], colors=['0.3', 'r', 'k','0.85'], linestyles=['-']*4, linewidths=[10, 10, 3, 10], loc='lower left', fontsize=10)
ax.set_title('Means and SDs')



### plot hypothesis test results:
ax     = plt.subplot(232)
spmi   = spm1d.stats.ttest_paired(yA, yB).inference(alpha, two_tailed=True)
spmi.plot(ax=ax)
spmi.plot_threshold_label()
ax.set_title('Hypothesis test')
ax.text(0.6, 0.2, 'Datum: zero\nCriterion:  $t ^*$', transform=ax.transAxes)




### plot confidence interval for mean paired difference:
ax     = plt.subplot(233)
ci0.plot(ax=ax)
ax.set_title('CI  (possibility 1)')
ax.text(0.1, 0.8, 'Datum: difference\nCriterion: mu=0', transform=ax.transAxes)



### plot confidence interval for mean paired difference:
ax     = plt.subplot(234)
ci1.plot(ax=ax)
ax.set_title('CI  (possibility 2)')
ax.text(0.1, 0.4, 'Datum: meanA\nCriterion: meanB', transform=ax.transAxes)


### plot confidence interval for mean paired difference:
ax     = plt.subplot(235)
ci2.plot(ax=ax)
ax.set_title('CI  (possibility 3)')
ax.text(0.1, 0.4, 'Datum: meanA\nCriterion: tailsAB', transform=ax.transAxes)


### plot CIs computed separately for the means (INCORRECT!!!)
ax     = plt.subplot(236)
ciA_bad.plot(ax=ax)
ciB_bad.plot(ax=ax, linecolor='r', facecolor='r', edgecolor='r', alpha=0.3)
ax.set_title('CIs computed separately for each group', size=10)
ax.text(0.1, 0.4, 'INCORRECT!!!', transform=ax.transAxes)





plt.show()



