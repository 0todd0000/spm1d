
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x2()
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x3()
y,A,B        = dataset.get_data()



#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spmi       = spm1d.stats.normality.anova2(y, A, B).inference(alpha)
print( spmi )



#(2) Plot
plt.close('all')
plt.figure(figsize=(14,4))
ax = plt.subplot(131);  ax.plot(y.T, 'k', lw=0.5);   ax.set_title('Data')
ax = plt.subplot(132);  ax.plot(spmi.residuals.T, 'k', lw=0.5);   ax.set_title('Residuals')
ax = plt.subplot(133);  spmi.plot(ax=ax);   spmi.plot_threshold_label(ax=ax); ax.set_title('Normality test')
plt.tight_layout()
plt.show()

