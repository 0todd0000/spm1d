

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


Copyright (C) 2023  Todd Pataky
'''


__version__ = '0.5.0'  # (2023-01-01)


__all__ = ['geom', 'prob', 'plot', 'stats', 'util', 'cfg']

from . import geom
from . import prob
from . import plot
from . import stats
from . import util



from . cfg import cfg