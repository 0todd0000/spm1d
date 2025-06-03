
import numpy as np
from . import _snpm
from . mgr import PermutationTestManager
from . permuters import MultiFactorPermuter


def _tstat_ind(y, A):
    A      = np.asarray(A)
    y0,y1  = y[A==0], y[A==1]
    n0,n1  = y0.shape[0], y1.shape[0]
    m0,m1  = y0.mean(axis=0), y1.mean(axis=0)
    s0,s1  = y0.std(ddof=1, axis=0), y1.std(ddof=1, axis=0)
    n      = y.shape[0]
    sp     = np.sqrt(0.5*(s0*s0 + s1*s1))
    t      = (m0-m1) / ( sp * (1/n0 + 1/n1)**0.5 )
    return t



def ttest2(y0, y1):
    n0,n1    = y0.shape[0], y1.shape[0]
    y        = np.vstack([y0,y1])
    A        = np.array(  [0]*n0 + [1]*n1 )
    mgr      = PermutationTestManager(y)
    perm     = MultiFactorPermuter(A)
    mgr.set_permuter( perm )
    mgr.set_teststat_fn( _tstat_ind )
    z        = _tstat_ind(y, A)
    return _snpm.SnPM_T(z, perm)
    