
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




#(2) Estimate field smoothness:
rA,rB    = yA-mA, yB-mB  #residuals
r        = np.vstack([rA,rB])
FWHM     = rft1d.geom.estimate_fwhm(r)



#(3) Critical threshold (classical hypothesis testing):
alpha    = 0.05
df       = nA + nB - 2  #degrees of freedom
Q        = yA.shape[1]  #number of nodes (field length = Q-1)
tstar    = rft1d.t.isf(alpha, df, Q, FWHM) #inverse survival function



#(4) Get upcrossing metrics:
calc      = rft1d.geom.ClusterMetricCalculator()
k         = calc.cluster_extents(t, tstar, interp=True)
k_resels  = [kk/FWHM for kk in k]
nClusters = len(k)



#(5) Probabilities:
rftcalc  = rft1d.prob.RFTCalculator(STAT='T', df=(1,df), nodes=Q, FWHM=FWHM)
Pset     = rftcalc.p.set(nClusters, min(k_resels), tstar)
Pcluster = [rftcalc.p.cluster(kk, tstar)   for kk in k_resels]




#(6) Plot:
pyplot.close('all')
ax     = pyplot.axes([0.08,0.15,0.89,0.83])
ax.plot(t, 'k', lw=3, label='t field')
ax.plot([0,Q], [tstar]*2, 'r--', label='Critical threshold')
### legend:
ax.legend(loc='upper left')
### cluster p values:
ax.text(10, 2.80,  'p = %.3f'%Pcluster[0], size=10)
ax.text(275, 3.5, 'p = %.3f'%Pcluster[1], size=10)
ax.text(280, 2.1, r'$\alpha$ = %.3f'%alpha, color='r')
### axis labels:
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
pyplot.show()



# pyplot.savefig('fig_weather_1_rft.pdf')


