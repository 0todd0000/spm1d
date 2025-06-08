

import numpy as np
import matplotlib.pyplot as plt
import spm1d
import spm1d.stats.nonparam_old  # version of nonparam before spm1d v0.4.50


def plot_ci_lines(ax, obj, **kwargs):
    h0 = ax.plot(obj.ciA[0], **kwargs)[0]
    h1 = ax.plot(obj.ciA[1], **kwargs)[0]
    return h0

# load dataset:
# dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
y0,y1        = dataset.get_data()  #normal and fast walking



# calculate parametric and non-parametric CIs:
np.random.seed(0)
alpha      = 0.05
mu         = 0
iterations = -1
ci         = spm1d.stats.ci_pairedsample(y0, y1, alpha, datum='meanA', mu='meanB')
np.random.seed(0)
cinp       = spm1d.stats.nonparam.ci_pairedsample(y0, y1, alpha, datum='meanA', mu='meanB', iterations=iterations)
np.random.seed(0)
cinpo      = spm1d.stats.nonparam_old.ci_pairedsample(y0, y1, alpha, datum='meanA', mu='meanB', iterations=iterations)



# plot:
plt.close('all')
plt.figure(figsize=(6,4))
ax = plt.axes()
ci.plot(ax)
h0 = ax.lines[1]
h1 = plot_ci_lines(ax, cinp, color='c', lw=5)
h2 = plot_ci_lines(ax, cinpo, color='r', lw=2)
ax.legend([h0,h1,h2], ['Criterion', 'Nonparam CI', 'Nonparam CI (old)'])
plt.tight_layout()
plt.show()



