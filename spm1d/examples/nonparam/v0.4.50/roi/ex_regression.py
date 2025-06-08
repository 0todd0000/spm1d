
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
dataset    = spm1d.data.uv1d.regress.SimulatedPataky2015c()
dataset    = spm1d.data.uv1d.regress.SpeedGRF()
y,x        = dataset.get_data()
# reduce sample size to check differences between new and old nonparam inference
# n          = 7
# y,x        = y[:n], x[:n]



# define region of interest(ROI):
roi        = np.array( [False]*y.shape[1] )
roi[10:30] = True
roi[40:60] = True
roi[70:90] = True



# conduct inference:
two_tailed = True
force      = True
niter      = 1000
alpha      = 0.05
spmi       = spm1d.stats.regress(y, x, roi=roi).inference(alpha, two_tailed=two_tailed)
snpmi      = spm1d.stats.nonparam.regress(y, x, roi=roi).inference(alpha, iterations=niter, two_tailed=two_tailed, force_iterations=force)
snpmio     = spm1d.stats.nonparam_old.regress(y, x, roi=roi).inference(alpha, iterations=niter, two_tailed=two_tailed, force_iterations=force)
print( 'Critical thresholds:')
print( f'   Parametric:           {spmi.zstar:.5f}')
print( f'   Nonparametric:        {snpmi.zstar:.5f}')
print( f'   Nonparametric (old):  {snpmio.zstar:.5f}')



# plot:
plt.close('all')
fig,axs = plt.subplots(2, 2, figsize=(8,6), tight_layout=True)
axs[0,0].plot(y.T, 'k', lw=0.5)
labels = ['SPM', 'SnPM', 'SnPM (Old)']
for ax,spm,label in zip(axs.ravel()[1:], [spmi, snpmi, snpmio], labels):
    spm.plot(ax=ax)
    ax.set_title( label )
    ax.set_ylabel('t-value')
ax = axs[0,1]
h0,h1 = plot_other_thresholds(ax, [snpmi, snpmio], ['c','r'])
ax.legend([h0,h1],['SnPM', 'SnPM (Old)'])
plt.show()


