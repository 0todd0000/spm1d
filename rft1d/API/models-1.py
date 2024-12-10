import numpy as np
import matplotlib.pyplot as plt
import power1d

y        = power1d.data.weather()['Atlantic']
model    = power1d.models.datasample_from_array( y )

plt.close('all')
fig,axs = plt.subplots(1, 3, figsize=(10,3), tight_layout=True)
axs[0].plot( y.T )
np.random.seed(0)
model.random()
model.plot( ax=axs[1])
model.random()
model.plot( ax=axs[2] )
labels  = 'Original data', 'DataSample model', 'DataSample model (new noise)'
[ax.set_title(s) for ax,s in zip(axs,labels)]
plt.show()