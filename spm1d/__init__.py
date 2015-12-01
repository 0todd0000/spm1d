

'''
spm1D: A Python package for 1D Statistical Parametric Mapping

Useful references include:

[1] Statistical Parametric Mapping: The Analysis of Functional Brain Images
Karl Friston, John Ashburner, Stefan Kiebel, Thomas Nichols (Editors)
Academic Press, 2006

[2] Wellcome Trust Centre for Neuroimaging SPM homepage:
www.fil.ion.ucl.ac.uk/spm/

[3] Pataky TC (2010). Generalized n-dimensional field analysis using
statistical parametric mapping. Journal of Biomechanics.


Copyright (C) 2015  Todd Pataky
Version: 0.3.1.4 (2015/10/16)
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *


__version__ = '0.3.1.4 (2015/10/16)'


__all__ = ['io', 'plot', 'stats', 'util']


from . import data, io, plot, stats, util



