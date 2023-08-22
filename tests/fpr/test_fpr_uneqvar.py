
'''
Unit tests for validating the false positive rates (FPR) of spm1d
hypothesis tests.

NOTE!!!  These FPR unit tests are NOT meant to be comprehensive
numeric FPR validations. Instead, they aim to aid development,
to ensure that tweaks to spm1d core code do not affect expected
FPRs. Thus only a relatively narrow range of FPR validations
are implemented below, with pre-selected parameters to ensure
approximate FPR repeatability.

More thorough validation possibilities are available in:
	spm1d.util.val
'''

import numpy as np
from spm1d.util.val.ui import *


def test_ttest2():
	np.random.seed(1)
	val = val_ttest2((12,8), (5,1), niter=1000, valtype='h0', equal_var=False)
	assert val.isvalid

def test_anova1():
	np.random.seed(5)
	val = val_anova1((12,5,5), (5,1,1), niter=1000, valtype='h0', equal_var=False)
	assert val.isvalid

def test_anova1rm():
	np.random.seed(13)
	val = val_anova1rm(8, (5,1,1), niter=1000, valtype='h0', equal_var=False)
	assert val.isvalid

# def test_anova2():
# 	np.random.seed(0)
# 	val = val_anova2([[8,8],[8,8]], [(1,1),(1,1)], niter=1000, valtype='z') #, equal_var=True)
# 	for isv in val.isvalid:
# 		assert isv


def test_ttest2_1d():
	np.random.seed(1)
	val = val_ttest2((12,8), (5,1), Q=101, fwhm=23, niter=1000, valtype='h0', equal_var=False)
	assert val.isvalid

def test_anova1_1d():
	np.random.seed(5)
	val = val_anova1((12,5,5), (5,1,1), Q=101, fwhm=23, niter=1000, valtype='h0', equal_var=False)
	assert val.isvalid

def test_anova1rm_1d():
	np.random.seed(14)
	val = val_anova1rm(8, (5,1,1), Q=101, fwhm=23, niter=1000, valtype='h0', equal_var=False)
	assert val.isvalid





# seed = 21
# print(seed)
# np.random.seed(seed)
# val = val_anova1rm(8, (5,1,1), Q=101, fwhm=23, niter=1000, valtype='h0', equal_var=False)
# print(val)
