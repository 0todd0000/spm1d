
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

# import pytest
import numpy as np
from spm1d.util.val.ui import *


# def test_ttest():
# 	np.random.seed(0)
# 	val = val_ttest(8, niter=1000, valtype='z')
# 	assert val.isvalid
#
# def test_ttest_paired():
# 	np.random.seed(5)
# 	val = val_ttest_paired(12, niter=1000, valtype='z')
# 	assert val.isvalid
#
# def test_ttest2():
# 	np.random.seed(6)
# 	val = val_ttest2((8,11), niter=1000, valtype='z', equal_var=True)
# 	assert val.isvalid
#
# def test_regress():
# 	np.random.seed(9)
# 	val = val_regress(10, niter=1000, valtype='z')
# 	assert val.isvalid
#
# def test_anova1():
# 	np.random.seed(12)
# 	val = val_anova1((8,5,7), (1,1,1), niter=1000, valtype='z', equal_var=True)
# 	assert val.isvalid
#
# def test_anova1rm():
# 	np.random.seed(13)
# 	val = val_anova1rm(9, (1,1,1), niter=1000, valtype='z', equal_var=True)
# 	assert val.isvalid

def test_anova2():
	np.random.seed(0)
	val = val_anova2([[8,8],[8,8]], [(1,1),(1,1)], niter=1000, valtype='z') #, equal_var=True)
	assert val.isvalid_omnibus



# np.random.seed(0)
# val = val_anova2([[8,8],[8,8]], [(1,1),(1,1)], niter=1000, valtype='z') #, equal_var=True)
# print(val)
