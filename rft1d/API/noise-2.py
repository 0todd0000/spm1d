import numpy as np
import matplotlib.pyplot as plt
import power1d

y      = power1d.data.weather()['Atlantic']
r      = y - y.mean( axis=0 ) # residuals
snoise = power1d.noise.from_residuals( r ) # scaled noise object

fig,axs = plt.subplots(1, 3, figsize=(10,3), tight_layout=True)
axs[0].plot( y.T )
axs[1].plot( r.T )
snoise.plot( ax=axs[2] )
labels  = 'Original data', 'Residuals', 'Scaled noise model'
[ax.set_title(s) for ax,s in zip(axs,labels)]
plt.show()