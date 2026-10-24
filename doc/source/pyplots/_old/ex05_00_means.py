
import numpy as np
from matplotlib import pyplot
import spm1d



# compute within-speed means for each subject:
nSubj         = 10
Y1,Y2,Y3      = [], [], []
for subj in range(nSubj):
    ### load GRF data:
    y1,y2,y3  = spm1d.util.get_dataset('speed-grf-categorical', subj)
    ### append to curve lists:
    Y1.append(  y1.mean(axis=0)  )
    Y2.append(  y2.mean(axis=0)  )
    Y3.append(  y3.mean(axis=0)  )
Y1,Y2,Y3      = np.asarray(Y1), np.asarray(Y2), np.asarray(Y3)


# plot:
pyplot.close('all')
h1 = pyplot.plot(Y1.T, color='b')
h2 = pyplot.plot(Y2.T, color='k')
h3 = pyplot.plot(Y3.T, color='r')
h1[0].set_label('Slow')
h2[0].set_label('Normal')
h3[0].set_label('Fast')
pyplot.legend(loc='lower center', fontsize=12)
pyplot.xlabel('Time (% stance)')
pyplot.ylabel('GRF (BW)')
# pyplot.show()
