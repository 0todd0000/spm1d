
import matplotlib.pyplot as plt
import spm1d


#(0) Load dataset:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
# dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
y0,y1        = dataset.YA, dataset.YB



#(1) Conduct equal variance test:
f,fcrit    = spm1d.stats.eqvartest( y0, y1, alpha=0.05, alt='greater' )


#(2) Plot:
plt.close('all')
fig,AX = plt.subplots( 1, 3, figsize=(10,2.5) )
ax0,ax1,ax2 = AX.flatten()
ax0.plot(y0.T, 'k')
ax0.plot(y1.T, 'r')
ax1.plot(y0.std(axis=0, ddof=1), 'k')
ax1.plot(y1.std(axis=0, ddof=1), 'r')
ax2.plot( f )
ax2.axhline( fcrit, color='r', ls='--' )
ax0.set_title('Dataset')
ax1.set_title('Standard deviations')
ax2.set_title('SPM results')
plt.tight_layout()
plt.show()