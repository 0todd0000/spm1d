
import numpy as np
import matplotlib.pyplot as plt
import spm1d



# compute within-speed means for each subject:
nSubj        = 10
Y1,Y2,Y3     = [], [], []
for subj in range(10):
	### load data:
	dataset  = spm1d.data.uv1d.anova1.SpeedGRFcategorical(subj=subj)
	Y,A      = dataset.get_data()
	### compute means for each of the three conditions:
	y1,y2,y3 = Y[A==1], Y[A==2], Y[A==3] 
	Y1.append(  y1.mean(axis=0)  )
	Y2.append(  y2.mean(axis=0)  )
	Y3.append(  y3.mean(axis=0)  )
Y1,Y2,Y3     = np.asarray(Y1), np.asarray(Y2), np.asarray(Y3)


# plot:
plt.close('all')
h1 = plt.plot(Y1.T, color='b')
h2 = plt.plot(Y2.T, color='k')
h3 = plt.plot(Y3.T, color='r')
h1[0].set_label('Slow')
h2[0].set_label('Normal')
h3[0].set_label('Fast')
plt.legend(loc='lower center', fontsize=12)
plt.xlabel('Time (% stance)')
plt.ylabel('GRF (BW)')
plt.tight_layout()
plt.show()
