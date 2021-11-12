
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
# dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
YA,YB        = dataset.get_data()



#(1) Conduct t test:
alpha      = 0.05
t          = spm1d.stats.ttest2(YB, YA, equal_var=True)
ti         = t.inference(alpha, two_tailed=True, interp=True)
print( ti )



#(2) Plot:
plt.close('all')
### plot mean and SD:
fig,AX = plt.subplots( 1, 2, figsize=(8, 3.5) )
ax     = AX[0]
plt.sca(ax)
spm1d.plot.plot_mean_sd(YA)
spm1d.plot.plot_mean_sd(YB, linecolor='r', facecolor='r')
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Time (%)')
ax.set_ylabel('Plantar arch angle  (deg)')
### plot SPM results:
ax     = AX[1]
plt.sca(ax)
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offset_all_clusters=(0,0.9))
ax.set_xlabel('Time (%)')
plt.tight_layout()
plt.show()
