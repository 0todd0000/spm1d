
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()



#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.ttest(y-mu).inference(alpha)
print( spmi )



#(2) Plot
plt.close('all')
plt.figure(figsize=(14,4))
ax = plt.subplot(131);  ax.plot(y.T, 'k', lw=0.5);   ax.set_title('Data')
ax = plt.subplot(132);  ax.plot(spmi.residuals.T, 'k', lw=0.5);   ax.set_title('Residuals')
ax = plt.subplot(133);  spmi.plot(ax=ax);   spmi.plot_threshold_label(ax=ax); ax.set_title('Normality test')
plt.tight_layout()
plt.show()


