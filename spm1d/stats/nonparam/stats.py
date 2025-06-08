
import numpy as np
from . mgr import get_perm_mgr


'''
anova1rm and higher-order designs can not yet be implemented
because spm1d v0.4.X requires design balance

mv procedures are unaffected by two-sample bug
'''

from .. nonparam_old import anova1rm

from .. nonparam_old import anova2
from .. nonparam_old import anova2nested
from .. nonparam_old import anova2onerm
from .. nonparam_old import anova2rm

from .. nonparam_old import anova3
from .. nonparam_old import anova3nested
from .. nonparam_old import anova3onerm
from .. nonparam_old import anova3tworm
from .. nonparam_old import anova3rm

from .. nonparam_old import cca
from .. nonparam_old import hotellings
from .. nonparam_old import hotellings_paired
from .. nonparam_old import hotellings2
from .. nonparam_old import manova1



# --------- NEW PROCEDURES ---------



def _spm_object(STAT, z, mgr):
    if STAT=='T':
        from . _snpm import SnPM_T, SnPM0D_T
        snpm = SnPM_T(z, mgr) if (mgr.dim==1) else SnPM0D_T(z, mgr)
    elif STAT=='F':
        if isinstance(z, list):
            from . _snpmlist import SnPMFList, SnPMFList0D
            n    = mgr.nfactors
            snpm = SnPMFList(z, mgr, nFactors=n) if (mgr.dim==1) else SnPMFList0D(z, mgr, nFactors=n)
        else:
            from . _snpm import SnPM_F, SnPM0D_F
            snpm = SnPM_F(z, mgr) if (mgr.dim==1) else SnPM0D_F(z, mgr)
    return snpm




def anova1(y, A, roi=None):
    from . permuters import MultiFactorPermuter
    from . calculators import CalculatorANOVA1
    mgr      = get_perm_mgr(y, mv=False, roi=roi)
    perm     = MultiFactorPermuter(A)
    calc     = CalculatorANOVA1(A)
    mgr.set_permuter( perm )
    mgr.set_calculator( calc )
    z        = calc.teststat(mgr.y, A)  # use mgr.y bacause it may be masked via roi
    return _spm_object('F', z, mgr)


# def anova1rm(y, A, S, roi=None):
#     from .. nonparam_old import anova1rm as anova1rm_old
#     return anova1rm_old(y, A, S, roi=roi)
#
#     # from . permuters import MultiFactorPermuter
#     # from . calculators import CalculatorANOVA1rm
#     # mgr      = get_perm_mgr(y, mv=False, roi=roi)
#     # perm     = MultiFactorPermuter(A)
#     # calc     = CalculatorANOVA1rm(A, S)
#     # mgr.set_permuter( perm )
#     # mgr.set_calculator( calc )
#     # z        = calc.teststat(mgr.y, A, S)  # use mgr.y bacause it may be masked via roi
#     # return _spm_object('F', z, mgr)



def regress(y, x, roi=None):
    from . permuters import RegressionPermuter
    from . calculators import CalculatorRegress0D, CalculatorRegress1D
    n        = y.shape[0]
    mgr      = get_perm_mgr(y, mv=False, roi=roi)
    perm     = RegressionPermuter(n)
    calc     = CalculatorRegress1D(x) if mgr.dim==1 else CalculatorRegress0D(x)
    mgr.set_permuter( perm )
    mgr.set_calculator( calc )
    z        = calc.teststat(mgr.y, list(range(n)))  # use mgr.y bacause it may be masked via roi
    return _spm_object('T', z, mgr)
    
def ttest(y, mu=None, roi=None):
    from . permuters import SingleSamplePermuter
    from . calculators import CalculatorTtest
    n        = y.shape[0]
    mgr      = get_perm_mgr(y, mv=False, roi=roi)
    perm     = SingleSamplePermuter(n)
    calc     = CalculatorTtest(n, mu)
    mgr.set_permuter( perm )
    mgr.set_calculator( calc )
    z        = calc.teststat(mgr.y, np.ones(n))  # use mgr.y bacause it may be masked via roi
    return _spm_object('T', z, mgr)

def ttest_paired(yA, yB, roi=None):
    return ttest(yA-yB, 0, roi=roi)

def ttest2(y0, y1, roi=None):
    from . permuters import MultiFactorPermuter
    from . calculators import CalculatorTtest2
    n0,n1    = y0.shape[0], y1.shape[0]
    y        = np.hstack([y0.T, y1.T]).T
    A        = np.array(  [0]*n0 + [1]*n1 )
    mgr      = get_perm_mgr(y, mv=False, roi=roi)
    perm     = MultiFactorPermuter(A)
    calc     = CalculatorTtest2(n0, n1)
    mgr.set_permuter( perm )
    mgr.set_calculator( calc )
    z        = calc.teststat(mgr.y, A)  # use mgr.y bacause it may be masked via roi
    return _spm_object('T', z, mgr)