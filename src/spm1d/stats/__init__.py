'''
Statistics module.

This module contains functions for conducting classical hypothesis testing on a set of 1D continua.

For all tests the dependent variable **Y** must be a NumPy array, with dimensions::

* J :  number of observations
* Q :  number of field nodes
* I :  number of vector components

Specifically:

* Univariate 0D tests:  **Y** should be ( J x 1 )
* Multivariate 0D tests:  **Y** should be ( J x I )
* Univariate 1D tests:  **Y** should be ( J x Q )
* Multivariate 1D tests:  **Y** should be ( J x Q x I )

'''

# Copyright (C) 2023  Todd Pataky



from . import _spmcls

# from . import glmc

# from . import prob
# from . import core
from . t import ttest, ttest_paired, ttest2, regress  # , glm
# from . ci import ci_onesample, ci_pairedsample, ci_twosample

from . f import anova1,anova1rm,anova2
from . glmc.ui import glm

# from . anova import anova2#,anova2nested,anova2rm,anova2onerm
# # from . anova import anova3,anova3nested,anova3rm,anova3tworm,anova3onerm


# from . mv import cca, hotellings, hotellings_paired, hotellings2, manova1
# # from . hotellings import hotellings, hotellings_paired, hotellings2
# # from . cca import cca
# # from . manova import manova1
# from . var import eqvartest
# #
# from . import nonparam
# # from . import normality
#
# # testnames = ['ttest']

_testnames = [s for s in dir()  if not s.startswith('_')]
