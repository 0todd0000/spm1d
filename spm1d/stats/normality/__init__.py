
'''
Normality tests for 1D data 
'''

# Copyright (C) 2016  Todd Pataky

from . import k2,sw

def dagostinoK2(x):
	return k2.residuals(x)

def shapirowilk(x):
	return sw.residuals(x)





residuals    = k2.residuals

anova1       = k2.anova1
anova1rm     = k2.anova1rm

anova2       = k2.anova2
anova2nested = k2.anova2nested
anova2onerm  = k2.anova2onerm
anova2rm     = k2.anova2rm

anova3       = k2.anova3
anova3nested = k2.anova3nested
anova3onerm  = k2.anova3onerm
anova3tworm  = k2.anova3tworm
anova3rm     = k2.anova3rm

regress      = k2.regress

ttest        = k2.ttest
ttest_paired = k2.ttest_paired
ttest2       = k2.ttest2

