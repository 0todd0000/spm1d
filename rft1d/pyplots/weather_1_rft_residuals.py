
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
import rft1d




#(0) Load weather data:
weather  = rft1d.data.weather() #dictionay containing geographical locations
### choose two geographical locations:
yA,yB    = weather['Atlantic'], weather['Continental']
### smooth:
yA       = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB       = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')




#(1) Two-sample t statistic (comparing just the two largest groups):
nA,nB    = yA.shape[0], yB.shape[0]  #sample sizes
mA,mB    = yA.mean(axis=0), yB.mean(axis=0)  #means
sA,sB    = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)  #standard deviations
s        = np.sqrt(    ((nA-1)*sA*sA + (nB-1)*sB*sB)  /  (nA + nB - 2)     )  #pooled standard deviation
t        = (mA-mB) / ( s *np.sqrt(1.0/nA + 1.0/nB))  #t field




#(2) Compute residuals:
rA,rB    = yA-mA, yB-mB  #residuals
r        = np.vstack([rA,rB])
FWHM     = rft1d.geom.estimate_fwhm(r)





#(3) Plot:
pyplot.close('all')
ax     = pyplot.axes()
hA     = ax.plot(rA.T, 'r')
hB     = ax.plot(rB.T, 'b')
hA[0].set_label('Atlantic')
hB[0].set_label('Continental')
ax.legend(loc='upper center')
### axis labels:
ax.set_xlabel('Day', size=16)
ax.set_ylabel('Temperature difference from mean', size=16)
ax.set_title('Model residuals', size=16)
# pyplot.show()



