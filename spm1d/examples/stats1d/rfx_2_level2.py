import os
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


#second-level SPM analysis:  (between-subject random effects)
alpha         = 0.05
t             = spm1d.stats.ttest(BETA)
ti            = t.inference(alpha, two_tailed=True)


#plot:
plt.close('all')
ti.plot()
ti.plot_threshold_label(fontsize=12)
ti.plot_p_values()
plt.xlabel('Time (% stance)', size=16)
plt.tight_layout()
plt.show()