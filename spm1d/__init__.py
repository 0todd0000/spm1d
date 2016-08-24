

'''
spm1D: A Python package for 1D Statistical Parametric Mapping

Useful references include:

[1] Statistical Parametric Mapping: The Analysis of Functional Brain Images
Karl Friston, John Ashburner, Stefan Kiebel, Thomas Nichols (Editors)
Academic Press, 2006

[2] Wellcome Trust Centre for Neuroimaging SPM homepage:
www.fil.ion.ucl.ac.uk/spm/

[3] Pataky TC (2016). RFT1D: Smooth one-dimensional random field upcrossing
probabilities in Python, Journal of Statistical Software, in press.


Copyright (C) 2016  Todd Pataky
Version: 0.3.2.5 (2016/06/27)
'''


__version__ = '0.3.3.X (2016/XX/XX)'


__all__ = ['data', 'io', 'plot', 'rft1d', 'stats', 'util']

from . import data
from . import io
from . import plot
from . import rft1d
from . import stats
from . import util

