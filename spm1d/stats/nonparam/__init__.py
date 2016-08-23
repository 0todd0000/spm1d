

'''
spm1dNP: A Python package for 1D Statistical non-Parametric Mapping
'''

__version__ = '0.X (2014/06/21)'


__all__ = ['stats']


import metrics, permuters, calculators, stats, _snpm

from stats import anova1,anova1rm,   anova2,anova2nested,anova2onerm,anova2rm,   anova3,anova3nested,anova3onerm, anova3tworm, anova3rm
from stats import regress, ttest, ttest_paired, ttest2
from stats import cca, hotellings, hotellings_paired, hotellings2, manova1
from ci import ci_onesample, ci_pairedsample, ci_twosample

