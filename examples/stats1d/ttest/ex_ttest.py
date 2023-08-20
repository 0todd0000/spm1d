
import os
import numpy as np
from matplotlib import pyplot as plt
import spm1d


dir0   = os.path.dirname(__file__)
fpath0 = os.path.join( dir0 , 'data', 'SimulatedPataky2015a.csv' )
fpath1 = os.path.join( dir0 , 'data', 'SimulatedPataky2015b.csv' )
y0     = np.loadtxt(fpath0, delimiter=',', dtype=float)
y1     = np.loadtxt(fpath1, delimiter=',', dtype=float)


t0     = spm1d.stats.ttest(y0, mu=0).inference(0.05, method='rft', dirn=1)
t1     = spm1d.stats.ttest(y1, mu=0).inference(0.05, method='rft', dirn=1)


plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(9,4))
t0.plot( ax=axs[0] )
t1.plot( ax=axs[1] )
plt.setp(axs, ylim=(-1.5, 4.5) )
[ax.set_title( os.path.split(f)[-1])  for ax,f in zip(axs, [fpath0,fpath1])]
[ax.set_xlabel('Domain position (%)')  for ax in axs]
axs[1].set_ylabel(None)
plt.tight_layout()
plt.show()


