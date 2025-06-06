
import numpy as np
from . import _snpm
from . mgr import PermutationTestManager


def _spm_object(STAT, z, mgr):
    if STAT=='T':
        return _snpm.SnPM_T(z, mgr) if (mgr.dim==1) else _snpm.SnPM0D_T(z, mgr)




def regress(y, x, roi=None):
    from . permuters import RegressionPermuter
    from . calculators import CalculatorRegress0D, CalculatorRegress1D
    n        = y.shape[0]
    mgr      = PermutationTestManager(y)
    perm     = RegressionPermuter(n)
    calc     = CalculatorRegress1D(x) if mgr.dim==1 else CalculatorRegress0D(x)
    mgr.set_permuter( perm )
    mgr.set_calculator( calc )
    z        = calc.teststat(y, list(range(n)))
    return _spm_object('T', z, mgr)
    
def ttest(y, mu=None, roi=None):
    from . permuters import SingleSamplePermuter
    from . calculators import CalculatorTtest
    n        = y.shape[0]
    mgr      = PermutationTestManager(y)
    perm     = SingleSamplePermuter(n)
    calc     = CalculatorTtest(n, mu)
    mgr.set_permuter( perm )
    mgr.set_calculator( calc )
    z        = calc.teststat(y, np.ones(n))
    return _spm_object('T', z, mgr)

def ttest_paired(yA, yB, roi=None):
    return ttest(yA-yB, 0, roi=roi)

def ttest2(y0, y1, roi=None):
    from . permuters import MultiFactorPermuter
    from . calculators import CalculatorTtest2
    n0,n1    = y0.shape[0], y1.shape[0]
    y        = np.hstack([y0.T, y1.T]).T
    A        = np.array(  [0]*n0 + [1]*n1 )
    mgr      = PermutationTestManager(y)
    perm     = MultiFactorPermuter(A)
    calc     = CalculatorTtest2(n0, n1)
    mgr.set_permuter( perm )
    mgr.set_calculator( calc )
    z        = calc.teststat(y, A)
    return _spm_object('T', z, mgr)