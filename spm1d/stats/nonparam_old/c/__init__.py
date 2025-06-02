'''
A common API for spm1d.stats.nonparam functions, with a constant, common argument structure:

	spm1d.stats.nonparam.c.TESTNAME(y, x)

where:

	y : vertically stacked dependent variable array
	x : independent variable / group array

This alternative API is currently meant mainly for internal testing.
'''

import numpy as np


from .. import ttest, regress, anova1
from .. import hotellings, cca, manova1


def anova1rm(y, x, **kwargs):
    from .. import anova1rm as f
    return f(y, *x.T, **kwargs)
def anova2(y, x, **kwargs):
    from .. import anova2 as f
    return f(y, *x.T, **kwargs)
def anova2nested(y, x, **kwargs):
    from .. import anova2nested  as f
    return f(y, *x.T, **kwargs)
def anova2onerm(y, x, **kwargs):
    from .. import anova2onerm as f
    return f(y, *x.T, **kwargs)
def anova2rm(y, x, **kwargs):
    from .. import anova2rm as f
    return f(y, *x.T, **kwargs)
def anova3(y, x, **kwargs):
    from .. import anova3 as f
    return f(y, *x.T, **kwargs)
def anova3nested(y, x, **kwargs):
    from .. import anova3nested as f
    return f(y, *x.T, **kwargs)
def anova3onerm(y, x, **kwargs):
    from .. import anova3onerm as f
    return f(y, *x.T, **kwargs)
def anova3rm(y, x, **kwargs):
    from .. import anova3rm as f
    return f(y, *x.T, **kwargs)
def anova3tworm(y, x, **kwargs):
    from .. import anova3tworm as f
    return f(y, *x.T, **kwargs)



def hotellings2(y, x, **kwargs):
    from .. import hotellings2
    ux = np.unique(x)
    y0 = y[x==ux[0]]
    y1 = y[x==ux[1]]
    return hotellings2(y0, y1, **kwargs)

def hotellings_paired(y, x, **kwargs):
    from .. import hotellings_paired
    ux = np.unique(x)
    y0 = y[x==ux[0]]
    y1 = y[x==ux[1]]
    return hotellings_paired(y0, y1, **kwargs)

def ttest2(y, x, **kwargs):
    from .. import ttest2
    ux = np.unique(x)
    y0 = y[x==ux[0]]
    y1 = y[x==ux[1]]
    return ttest2(y0, y1, **kwargs)

def ttest_paired(y, x, **kwargs):
    from .. import ttest_paired
    ux = np.unique(x)
    y0 = y[x==ux[0]]
    y1 = y[x==ux[1]]
    return ttest(y0 - y1, 0, **kwargs)