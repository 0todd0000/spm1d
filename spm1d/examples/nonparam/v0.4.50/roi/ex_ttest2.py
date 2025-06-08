
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import spm1d.stats.nonparam_old


def plot_other_thresholds(ax, spms, colors):
    from spm1d._plot import SPMiPlotter
    plotter0 = SPMiPlotter(snpmi, ax=ax)
    plotter1 = SPMiPlotter(snpmio, ax=ax)
    h0 = plotter0.plot_threshold( color=colors[0])[0][0]
    h1 = plotter1.plot_threshold( color=colors[1])[0][0]
    return h0,h1



# load data
dataset      = spm1d.data.uv1d.t2.SmallSampleLargePosNegEffects()
y0,y1        = dataset.get_data()
# OR create a random dataset:
np.random.seed(0)
n  = 6
y0 = np.random.randn(n,101)
y1 = np.random.randn(n,101) + 2*np.sin( np.linspace(0,10,101) )
y0 = spm1d.util.smooth(y0, 8)
y1 = spm1d.util.smooth(y1, 8)


# define region of interest(ROI):
roi        = np.array( [False]*y0.shape[1] )
roi[70:80] = True


# conduct inference:
two_tailed = True
niter      = -1
alpha      = 0.05
spmi       = spm1d.stats.ttest2(y1, y0, roi=roi).inference(alpha, two_tailed=two_tailed)
snpmi      = spm1d.stats.nonparam.ttest2(y1, y0, roi=roi).inference(alpha, iterations=niter, two_tailed=two_tailed)
snpmio     = spm1d.stats.nonparam_old.ttest2(y1, y0, roi=roi).inference(alpha, iterations=niter, two_tailed=two_tailed)
print( 'Critical thresholds:')
print( f'   Parametric:           {spmi.zstar:.5f}')
print( f'   Nonparametric:        {snpmi.zstar:.5f}')
print( f'   Nonparametric (old):  {snpmio.zstar:.5f}')



# plot:
plt.close('all')
fig,axs = plt.subplots(2, 2, figsize=(8,6), tight_layout=True)
axs[0,0].plot(y0.T, 'k', lw=0.5)
axs[0,0].plot(y1.T, 'c', lw=0.5)
labels = ['SPM', 'SnPM', 'SnPM (Old)']
for ax,spm,label in zip(axs.ravel()[1:], [spmi, snpmi, snpmio], labels):
    spm.plot(ax=ax)
    ax.set_title( label )
    ax.set_ylabel('t-value')
ax = axs[0,1]
h0,h1 = plot_other_thresholds(ax, [snpmi, snpmio], ['c','r'])
ax.legend([h0,h1],['SnPM', 'SnPM (Old)'])
plt.show()

