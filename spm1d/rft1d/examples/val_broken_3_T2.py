
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d

def here_hotellingsT2(y):
	N       = y.shape[0]
	m       = np.matrix(  y.mean(axis=0) )
	T2      = []
	for ii,mm in enumerate(m):
		W   = np.matrix( np.cov(y[:,ii,:].T, ddof=1) )  #estimated covariance
		t2  = N * mm * np.linalg.inv(W) * mm.T
		T2.append(  float(t2)  )
	return np.asarray(T2)


	
	

#(0) Set parameters:
np.random.seed(0)
nResponses      = 25
nNodes          = 101
nComponents     = 2
nIterations     = 200   #raise this to at least 500 for convergence
FWHM            = 12.0
W0              = np.eye(nComponents)
### derived parameters:
df              = nComponents, nResponses-1   #p,m
### generate a field mask:
nodes           = np.array([True]*nNodes) #nothing masked out
nodes[10:30]    = False  #this region will be masked out
nodes[60:85]    = False




#(1) Generate Gaussian 1D fields, compute test stat:
generator   = rft1d.random.GeneratorMulti1D(nResponses, nodes, nComponents, FWHM, W0)
T2          = []
for i in range(nIterations):
	y       = generator.generate_sample()
	t2      = here_hotellingsT2(y)
	T2.append( np.nanmax(t2) )
T2          = np.array(T2)




#(2) Survival functions for field maximum:
heights    = np.linspace(8.0, 15, 21)
sf         = np.array(  [ (T2>=h).mean()  for h in heights]  )
sfE_full   = rft1d.T2.sf(heights, df, nNodes, FWHM)  #theoretical (full)
sfE_broken = rft1d.T2.sf(heights, df, nodes, FWHM)   #theoretical (broken)



#(3) Plot results:
pyplot.close('all')
ax         = pyplot.axes()
ax.plot(heights, sfE_full,   'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf,         'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (T^2_\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation ($T^2$)', size=20)
pyplot.show()

