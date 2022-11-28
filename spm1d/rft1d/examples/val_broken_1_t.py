
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d



#(0) Set parameters:
np.random.seed(0)
nResponses   = 12
nIterations  = 5000
nNodes       = 101
FWHM         = 11.5
### derived parameters:
df           = nResponses-1
sqrtN        = np.sqrt(nResponses)
### generate a field mask:
nodes        = np.array([True]*nNodes) #nothing masked out
nodes[10:25] = False  #this region will be masked out
nodes[50:75] = False




#(1) Generate Gaussian 1D fields, compute test stat:
generator   = rft1d.random.Generator1D(nResponses, nodes, FWHM)
T           = []
for i in range(nIterations):
	y       = generator.generate_sample()
	t       = y.mean(axis=0) / y.std(ddof=1, axis=0) * sqrtN
	T.append( np.nanmax(t) )
T           = np.array(T)




#(2) Survival functions for field maximum:
heights    = np.linspace(2.0, 4, 21)
sf         = np.array(  [ (T>=h).mean()  for h in heights]  )
sfE_full   = rft1d.t.sf(heights, df, nNodes, FWHM)  #theoretical (full)
sfE_broken = rft1d.t.sf(heights, df, nodes, FWHM)   #theoretical (broken)



#(3) Plot results:
pyplot.close('all')
ax         = pyplot.axes()
ax.plot(heights, sfE_full,   'b-', label='Theoretical (full)')
ax.plot(heights, sfE_broken, 'r-', label='Theoretical (broken)')
ax.plot(heights, sf,         'ro', label='Simulated (broken)')
ax.set_xlabel('x', size=16)
ax.set_ylabel('$P (t_\mathrm{max} > x)$', size=20)
ax.legend()
ax.set_title('Broken field validation (t)', size=20)
pyplot.show()

