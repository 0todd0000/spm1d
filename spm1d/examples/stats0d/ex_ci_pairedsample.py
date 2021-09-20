
import numpy as np
import matplotlib.pyplot as plt
import spm1d



#(0) Load dataset:
dataset = spm1d.data.uv0d.cipaired.FraminghamSystolicBloodPressure()
yA,yB   = dataset.get_data()
print( dataset )
# yB += 1.9



#(1) Compute confidence intervals:
alpha   = 0.05
mu      = 0
ci0     = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='difference', mu=None)  # datum: inter-group mean difference  (explicit hypothesis test suppressed using "mu=None")
ci1     = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='difference', mu=mu)    # datum: inter-group mean difference  (hypothesis test regarding a specific inter-group difference "mu=0")
ci2     = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='meanB')    # datum: meanA,  criterion: whether CI reaches meanB
ci3     = spm1d.stats.ci_pairedsample(yA, yB, alpha, datum='meanA', mu='tailB')    # datum: meanA,  criterion:whether CI tails overlap
print( ci0 )
print( ci1 )
print( ci2 )
print( ci3 )



#(2) Plot the CIs:
plt.close('all')
plt.figure(figsize=(8,8))
ax0 = plt.subplot(221);  ci0.plot(ax0);  ax0.set_title('datum="difference", mu=None', size=10)
ax1 = plt.subplot(222);  ci1.plot(ax1);  ax1.set_title('datum="difference", mu=%.5f'%mu, size=10)
ax2 = plt.subplot(223);  ci2.plot(ax2);  ax2.set_title('datum="meanA", mu="meanB"', size=10)
ax3 = plt.subplot(224);  ci3.plot(ax3);  ax3.set_title('datum="meanA", mu="tailB"', size=10)
plt.suptitle('Paired sample CIs')
plt.show()

