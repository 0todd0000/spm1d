
import numpy as np
from matplotlib import pyplot
import spm1d




#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x2()
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x3()
y,A,B        = dataset.get_data()



#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.anova2(y, A, B).inference(alpha)
print( spmi )



#(2) Plot
pyplot.close('all')
pyplot.figure(figsize=(14,4))
ax = pyplot.subplot(131);  ax.plot(y.T, 'k', lw=0.5);   ax.set_title('Data')
ax = pyplot.subplot(132);  ax.plot(spmi.residuals.T, 'k', lw=0.5);   ax.set_title('Residuals')
ax = pyplot.subplot(133);  spmi.plot(ax=ax);   spmi.plot_threshold_label(ax=ax); ax.set_title('Normality test')
pyplot.show()

