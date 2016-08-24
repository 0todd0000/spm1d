
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d





### EPS production preliminaries:
fig_width_mm  = 100
fig_height_mm = 80
mm2in = 1/25.4
fig_width  = fig_width_mm*mm2in  	# width in inches
fig_height = fig_height_mm*mm2in    # height in inches
params = {	'backend':'ps', 'axes.labelsize':14,
			'font.size':12, 'text.usetex': False, 'legend.fontsize':12,
			'xtick.labelsize':8, 'ytick.labelsize':8,
			'font.family':'Times New Roman',  #Times
			'lines.linewidth':0.5,
			'patch.linewidth':0.25,
			'figure.figsize': [fig_width,fig_height]}
pyplot.rcParams.update(params)




def here_tstat2(yA, yB):
	nA,nB  = yA.shape[0], yB.shape[0]
	mA,mB  = yA.mean(axis=0), yB.mean(axis=0)
	sA,sB  = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
	s      = np.sqrt(    ((nA-1)*sA*sA + (nB-1)*sB*sB)  /  (nA + nB - 2)     )
	t      = (mA-mB) / ( s *np.sqrt(1.0/nA + 1.0/nB))
	return t



#(0) Load weather data:
weather  = rft1d.data.weather() #dictionay containing geographical locations
### choose two geographical locations:
yA,yB    = weather['Atlantic'], weather['Continental']
### smooth:
yA       = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB       = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')



#(1) Two-sample permutation test (comparing just the two largest groups):
nA,nB    = yA.shape[0], yB.shape[0]  #sample sizes
N        = nA+nB  #total number of responses
### original test statistic
t0       = here_tstat2(yA, yB)
### random label permutations:
np.random.seed(0)
nIter    = 1000
T        = []
y        = np.vstack((yA,yB))  #all responses (unlabeled)
for iii in range(nIter):
	ind      = np.random.permutation(N)
	i0,i1    = ind[:nA], ind[nA:]
	yyA,yyB  = y[i0], y[i1]
	T.append(  here_tstat2(yyA, yyB).max()  )  #t field maximum
### critical threshold:
alpha    = 0.05
tstar    = np.percentile(T, 100*(1-alpha))



#(2) Secondary permutation PDF (for cluster extent)
calc     = rft1d.geom.ClusterMetricCalculator()
k0       = calc.cluster_extents(t0, tstar, interp=True)  #original cluster metrics
nIter    = 1000
K        = []
for iii in range(nIter):
	ind      = np.random.permutation(N)
	i0,i1    = ind[:nA], ind[nA:]
	yyA,yyB  = y[i0], y[i1]
	t        = here_tstat2(yyA, yyB)
	k        = calc.cluster_extents(t, tstar, interp=True)
	K.append( max(k) )
K        = np.array(K)
### probabilities:
Pcluster = [(K>=kk).mean()  for kk in k0]






#(3) Plot:
pyplot.close('all')
ax     = pyplot.axes([0.08,0.15,0.89,0.83])
ax.plot(t0, 'k', lw=3, label='t field')
ax.plot([0,t.size], [tstar]*2, 'r--', label='Critical threshold')
### legend:
ax.legend(loc='upper left')
### cluster p values:
ax.text(10, 2.80,  'p = %.3f'%Pcluster[0], size=10)
ax.text(275, 3.5, 'p = %.3f'%Pcluster[1], size=10)
ax.text(280, 1.8, r'$\alpha$ = %.3f'%alpha, color='r')
### axis labels:
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
pyplot.show()



# pyplot.savefig('fig_weather_3_nonparam.pdf')


