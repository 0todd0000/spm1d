
'''
Normality tests for 1D data 
'''

# Copyright (C) 2016  Todd Pataky

from . import k2,sw

def dagostinoK2(x):
	return k2.residuals(x)

def shapirowilk(x):
	return sw.residuals(x)