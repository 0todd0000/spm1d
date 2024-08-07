

'''
Geometry module

.. warning:: This module is minimal and serves only future compatibility purposes.

'''

# Copyright (C) 2024  Todd Pataky
# updated (2024/08/08) todd




def estimate_fwhm(R):
    '''
    Estimate field smoothness (FWHM) from a set of random fields or a set of residuals.
    
    Adapted from rft1d.geom.estimate_fwhm
    
    '''
    from math import log
    import numpy as np
    ssq    = (R**2).sum(axis=0)
    ### gradient estimate
    dy,dx  = np.gradient(R)
    v      = (dx**2).sum(axis=0)
    # normalize:
    eps    = np.finfo(float).eps
    v     /= (ssq + eps)
    # ignore zero-variance nodes:
    i      = np.isnan(v)
    v      = v[np.logical_not(i)]
    # global FWHM estimate:
    reselsPerNode = np.sqrt(v / (4*log(2)))
    efwhm         = 1 / reselsPerNode.mean()
    return efwhm

