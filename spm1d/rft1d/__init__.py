'''
rft1d was previously released as a separate package.
It is now integrated with spm1d, and is currently nearly identical to the separately downloadable rft1d pacakge.

Future plans include:

- integrate rft1d examples and data into spm1d examples
- merge the ./rft1d/geom.py functionality with the spm1d cluster functionality
- maintain the separate rft1d as a standalone package for users who want light-weight RFT probability calculations
'''


__version__  = '0.1.4 spm1d'   #(2016.10.01)

from . import data, distributions, geom, prob, random

randn1d      = random.randn1d
multirandn1d = random.multirandn1d

chi2         = distributions.chi2
f            = distributions.f
norm         = distributions.norm
t            = distributions.t
T2           = distributions.T2
