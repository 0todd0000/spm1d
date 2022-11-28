
'''
This script presents simple, non-thorough validations of the
"spm1d.stats.eqvartest" procedure.
'''

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import spm1d
rft1d = spm1d.rft1d



#(0) Run for a single dataset (1D):
np.random.seed(0)
J0,J1,Q,W   = 8, 12, 101, 20
y0,y1       = rft1d.randn1d(J0, Q, W), rft1d.randn1d(J1, Q, W)
f,fcrit     = spm1d.stats.eqvartest(y0, y1, alt="greater", alpha=0.05)
### plot:
plt.close('all')
fig,AX = plt.subplots( 1, 3, figsize=(10,2.5) )
ax0,ax1,ax2 = AX.flatten()
ax0.plot(y0.T, 'k')
ax0.plot(y1.T, 'r')
ax1.plot(y0.std(axis=0, ddof=1), 'k')
ax1.plot(y1.std(axis=0, ddof=1), 'r')
ax2.plot( f )
ax2.axhline( fcrit, color='r', ls='--' )
ax0.set_title('Dataset')
ax1.set_title('Standard deviations')
ax2.set_title('SPM results')
plt.tight_layout()
plt.show()




#(1) Validate false positive rate (simple, non-thorough validation)
np.random.seed(0)
J0,J1,Q,W    = 8, 12, 101, 20
niter        = 20
alpha        = 0.05
fp           = []
for i in range(niter):
	y0,y1    = rft1d.randn1d(J0, Q, W), rft1d.randn1d(J1, Q, W)
	f,fcrit  = spm1d.stats.eqvartest(y0, y1, alt="greater", alpha=alpha)
	fp.append( f.max() > fcrit )
fpr          = np.mean(fp)
print('False positive rate expected: %0.3f, actual: %0.3f' %(alpha,fpr))




#(2) Validate survival function ("greater" case;  unequal sample sizes OK)
np.random.seed(0)
J0,J1,Q,W    = 8, 12, 101, 20
niter        = 1000
fmax         = []
for i in range(niter):
	y0,y1    = rft1d.randn1d(J0, Q, W), rft1d.randn1d(J1, Q, W)
	f,_      = spm1d.stats.eqvartest(y0, y1, alt="greater", alpha=None)
	fmax.append( f.max() )
# survival functions:
fmax         = np.array(fmax)
df           = J0-1, J1-1
u            = np.linspace(2, 15, 21)
sf           = np.array(  [ (fmax>uu).mean()  for uu in u]  )
sfE          = rft1d.f.sf(u, df, Q, W)  #theoretical
### plot survival functions:
plt.figure()
ax = plt.axes()
ax.plot(u, sf,   'bo',  label='Simulated')
ax.plot(u, sfE,  'b-',  label='Theoretical')
ax.legend()
ax.set_xlabel('$u$', size=14)
ax.set_ylabel('$P (F_\mathrm{max} > u)$', size=14)
ax.set_title('Survival functions (alt="greater")', size=16)
plt.show()




#(3) Validate survival function ("unequal" case;  must use equal sample sizes)
np.random.seed(0)
J,Q,W        = 8, 101, 20
niter        = 1000
fmax         = []
for i in range(niter):
	y0,y1    = rft1d.randn1d(J, Q, W), rft1d.randn1d(J, Q, W)
	f,_      = spm1d.stats.eqvartest(y0, y1, alt="unequal", alpha=None)
	fmax.append( f.max() )
# survival functions:
fmax         = np.array(fmax)
df           = J-1, J-1
u            = np.linspace(6, 20, 21)
sf           = np.array(  [ (fmax>uu).mean()  for uu in u]  )
sfE          = 2*rft1d.f.sf(u, df, Q, W)  #theoretical
### plot survival functions:
plt.figure()
ax = plt.axes()
ax.plot(u, sf,   'bo',  label='Simulated')
ax.plot(u, sfE,  'b-',  label='Theoretical')
ax.legend()
ax.set_xlabel('$u$', size=14)
ax.set_ylabel('$P (F_\mathrm{max} > u)$', size=14)
ax.set_title('Survival functions (alt="unequal")', size=16)
plt.show()


