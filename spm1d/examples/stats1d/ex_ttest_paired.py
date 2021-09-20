
import matplotlib.pyplot as plt
import spm1d



#(0) Load data:
dataset    = spm1d.data.uv1d.t2.PlantarArchAngle()
YA,YB      = dataset.get_data()  #normal and fast walking



#(1) Conduct t test:
spm        = spm1d.stats.ttest_paired(YA, YB)
spmi       = spm.inference(0.05, two_tailed=False, interp=True)
print( spmi )



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
spmi.plot()
spmi.plot_threshold_label(fontsize=8)
spmi.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Time (%)')
plt.tight_layout()
plt.show()
