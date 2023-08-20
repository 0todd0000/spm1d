
# validate FPR for ttest

# import sys
import numpy as np
# from scipy import stats
import matplotlib.pyplot as plt
import spm1d



# from spm1d.util.val import FPRValidator

from spm1d.util.val.ui import *

np.random.seed(0)



# val = val_ttest(8, valtype='h0', niter=1000, progress_bar=True)  # ttest (0D)
# val = val_ttest(8, Q=101, fwhm=20, valtype='z', niter=1000)  # ttest (1D)

# val = val_ttest2((8, 8), valtype='h0', niter=1000)
val = val_ttest2((8, 8), Q=101, fwhm=20, valtype='z', niter=1000)





print( val )


# two-sample t test
# np.random.seed(0)
# val = val_ttest(8, valtype='h0', niter=1000)
# print( val )


# plt.close('all')
# plt.figure()
# plt.get_current_fig_manager().window.move(0, 0)
# ax = plt.axes()
# val.plot_results(ax=ax)
# plt.show()



# # two-sample t test
# def ttest2(y, A):
# 	u  = np.unique(A)
# 	y0 = y[A==u[0]]
# 	y1 = y[A==u[1]]
# 	return spm1d.stats.ttest2(y0, y1)
#
#
# np.random.seed(0)
# J0,J1 = 8, 12
# A     = np.array([0]*J0 + [1]*J1)
# rng   = lambda: np.random.randn(J0 + J1)
# fn    = lambda y: ttest2(y, A)
# u     = stats.t.isf(0.05, J0+J1-2)
# val   = FPRValidator(fn, rng, valtype='z', u=u)
# spm = val.sim_single()
# val.sim( niter=1000 )
# print( val )
# plt.close('all')
# plt.figure()
# plt.get_current_fig_manager().window.move(0, 0)
# ax = plt.axes()
# val.plot_results(ax=ax)
# plt.show()




# # one-sample t test (1D)
# np.random.seed(2)
# val = val_ttest(8, Q=101, fwhm=20, valtype='z', niter=1000)
# print( val )


# import rft1d
# np.random.seed(1)
# J,Q,W = 8, 101, 20
# rng   = lambda: rft1d.randn1d(J, Q, W)
# fn    = lambda y: spm1d.stats.ttest(y, 0)
# u     = rft1d.t.isf(0.05, J-1, Q, W)
# val   = FPRValidator(fn, rng, valtype='z', u=u)
# # spm   = val.sim_single()
# val.sim( niter=5000 )
# print( val )
# plt.close('all')
# plt.figure()
# plt.get_current_fig_manager().window.move(0, 0)
# ax = plt.axes()
# val.plot_results(ax=ax)
# plt.show()

