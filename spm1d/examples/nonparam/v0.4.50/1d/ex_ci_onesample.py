
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import spm1d.stats.nonparam_old  # version of nonparam before spm1d v0.4.50


def plot_ci_lines(ax, obj, **kwargs):
    h0 = ax.plot(obj.ci[0], **kwargs)[0]
    h1 = ax.plot(obj.ci[1], **kwargs)[0]
    return h0

# load dataset:
dataset    = spm1d.data.uv1d.t1.Random()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
y,mu       = dataset.get_data()

# OR create a random dataset:
np.random.seed(3)
n          = 6
y          = np.random.randn(n,101) + 2*np.sin( np.linspace(0,10,101) )
y          = spm1d.util.smooth(y, 8)
mu         = 0



# calculate parametric and non-parametric CIs:
np.random.seed(0)
alpha      = 0.05
mu         = 0
iterations = -1
ci         = spm1d.stats.ci_onesample(y, alpha, mu=mu)
np.random.seed(0)
cinp       = spm1d.stats.nonparam.ci_onesample(y, alpha, mu=mu, iterations=iterations)
np.random.seed(0)
cinpo      = spm1d.stats.nonparam_old.ci_onesample(y, alpha, mu=mu, iterations=iterations)



# plot:
plt.close('all')
plt.figure(figsize=(6,4))
ax = plt.axes()
ci.plot(ax)
h0 = plot_ci_lines(ax, cinp, color='c', lw=5)
h1 = plot_ci_lines(ax, cinpo, color='r', lw=2)
ax.legend([h0,h1], ['Nonparam', 'Nonparam (old)'])
plt.tight_layout()
plt.show()



