
import numpy as np
import matplotlib.pyplot as plt
import spm1d






#first-level SPM analysis: (within-subject effects)
nSubj         = 10
BETA          = []  #regression slopes
for subj in range(nSubj):
	dataset   = spm1d.data.uv1d.regress.SpeedGRF(subj=subj)
	Y,x       = dataset.get_data()
	t         = spm1d.stats.regress(Y, x) #conduct linear regression
	BETA.append( t.beta[0] )  #retrieve the regression slope
BETA          = np.array(BETA)


#plot:
plt.close('all')
ax            = plt.axes( (0.15, 0.15, 0.8, 0.8) )
plt.plot(BETA.T, color='k')
ax.axhline(y=0, color='k', linewidth=1, linestyle=':')
ax.set_xlabel('Time (% stance)')
ax.set_ylabel(r'$\beta_0$   $(BW / ms^{-1})$')
plt.tight_layout()
plt.show()

