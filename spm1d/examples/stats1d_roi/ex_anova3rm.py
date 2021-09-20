
import numpy as np
import matplotlib.pyplot as plt
import spm1d




#(0) Load data:
dataset      = spm1d.data.uv1d.anova3rm.SPM1D_ANOVA3RM_2x2x2()
Y,A,B,C,SUBJ = dataset.get_data()



#(0a) Create region of interest(ROI):
roi        = np.array([False]*Y.shape[1])
roi[40:75] = True


#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova3rm(Y, A, B, C, SUBJ, equal_var=True, roi=roi)
FFi          = [F.inference(alpha)   for F in FF]


#(2) Plot results:
plt.close('all')
plt.figure(figsize=(12,8))
titles       = ['Main effect A',
               'Main effect B',
               'Main effect C',
               'Interaction AB',
               'Interaction AC',
               'Interaction BC',
               'Interaction ABC',
]
for i,Fi in enumerate(FFi):
	ax = plt.subplot(3,3,i+1)
	Fi.plot()
	ax.text(0.1, 0.85, titles[i], transform=ax.transAxes)
plt.tight_layout()
plt.show()





