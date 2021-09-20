
import matplotlib.pyplot as plt
import spm1d


#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random()
dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015a()
# dataset    = spm1d.data.uv1d.t1.SimulatedPataky2015b()
Y,mu       = dataset.get_data()


#(1) Conduct t test:
alpha      = 0.05
t          = spm1d.stats.ttest(Y, mu)
ti         = t.inference(alpha, two_tailed=False, interp=True)




#(2) Plot:
plt.close('all')
### plot mean and SD:
fig,AX = plt.subplots( 1, 2, figsize=(8, 3.5) )
ax     = AX[0]
plt.sca(ax)
spm1d.plot.plot_mean_sd(Y)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Measurement domain (%)')
ax.set_ylabel('Dependent Variable')
### plot SPM results:
ax     = AX[1]
plt.sca(ax)
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Measurement domain (%)')
plt.tight_layout()
plt.show()