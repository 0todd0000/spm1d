

import itertools
import numpy as np
import pytest
import spm1d
from spm1d.stats._datachecks import SPM1DError
from spm1d.stats.anova import designs, models


def _balanced(levels, n):
    """Balanced factor label vectors:  one entry per observation, n per cell."""
    J, out, inner = n * int(np.prod(levels)), [], n
    for nl in reversed(levels):
        out.insert(0, np.tile(np.repeat(np.arange(nl), inner), J // (nl * inner)))
        inner *= nl
    return out


def _dfE_of(design):
    model = models.LinearModel(np.zeros(design.X.shape[0]), design.X)
    model.fit()
    return int(model._dfE)


def _exact_dfE(design):
    X = design.X
    return int(X.shape[0] - np.linalg.matrix_rank(X))


#  Designs for which the SVD estimate of the residual rank was observed to be
#  1 too high.  The affected set depends on the BLAS; this is the complete set
#  tested on OpenBLAS/Linux and Accelerate/macOS.
KNOWN_ANOVA2 = [(3,2,2), (4,4,2), (4,4,3), (4,4,4), (4,4,5), (6,6,2), (6,6,3),
                (7,8,2), (7,9,3), (8,8,3), (9,10,2), (11,11,5), (12,5,2)]
KNOWN_ANOVA3 = [(2,3,2,2), (2,4,4,2), (4,2,4,2), (5,2,5,3)]


@pytest.mark.parametrize('a,b,n', KNOWN_ANOVA2)
def test_anova2_dfE_exact_known(a, b, n):
    A,B = _balanced((a,b), n)
    d   = designs.ANOVA2(A, B)
    assert _dfE_of(d) == _exact_dfE(d)


@pytest.mark.parametrize('a,b,c,n', KNOWN_ANOVA3)
def test_anova3_dfE_exact_known(a, b, c, n):
    A,B,C = _balanced((a,b,c), n)
    d     = designs.ANOVA3(A, B, C)
    assert _dfE_of(d) == _exact_dfE(d)


def test_anova1_dfE_exact_grid():
    for a,n in itertools.product(range(2,9), range(2,9)):
        A = _balanced((a,), n)[0]
        d = designs.ANOVA1(A)
        assert _dfE_of(d) == _exact_dfE(d), 'anova1 %dx n=%d' %(a,n)


def test_anova2_dfE_exact_grid():
    for a,b,n in itertools.product(range(2,7), range(2,7), range(2,6)):
        A,B = _balanced((a,b), n)
        d   = designs.ANOVA2(A, B)
        assert _dfE_of(d) == _exact_dfE(d), 'anova2 %dx%d n=%d' %(a,b,n)


def test_anova3_dfE_exact_grid():
    for a,b,c,n in itertools.product(range(2,5), range(2,5), range(2,5), range(2,4)):
        A,B,C = _balanced((a,b,c), n)
        d     = designs.ANOVA3(A, B, C)
        assert _dfE_of(d) == _exact_dfE(d), 'anova3 %dx%dx%d n=%d' %(a,b,c,n)


#  A saturated design has no residual, so the error term should be 0.

#  the two-level anova1 warning is unrelated to this test
@pytest.mark.filterwarnings('ignore:(?s).*one-way ANOVA with two levels.*:UserWarning')
def test_anova1_unreplicated_raises():
    y = np.array([1.0, 2.0])
    with pytest.raises(SPM1DError):
        spm1d.stats.anova1(y, np.array([0,1]), equal_var=True)


def test_anova2_unreplicated_raises():
    A,B = _balanced((3,4), 1)
    with pytest.raises(SPM1DError):
        spm1d.stats.anova2(np.arange(12, dtype=float), A, B, equal_var=True)


def test_anova3_unreplicated_raises():
    A,B,C = _balanced((2,2,2), 1)
    with pytest.raises(SPM1DError):
        spm1d.stats.anova3(np.arange(8, dtype=float), A, B, C, equal_var=True)


#  One subject leaves the subject block with no columns.

def test_anova1rm_one_subject_raises():
    with pytest.raises(SPM1DError):
        spm1d.stats.anova1rm(np.arange(3, dtype=float), np.array([0,1,2]),
                             np.array([0,0,0]), equal_var=True)


def test_anova2rm_one_subject_raises():
    y = np.arange(4, dtype=float)
    with pytest.raises(SPM1DError):
        spm1d.stats.anova2rm(y, np.array([0,0,1,1]), np.array([0,1,0,1]),
                             np.array([0,0,0,0]), equal_var=True)


def test_anova2onerm_one_subject_raises():
    y = np.arange(4, dtype=float)
    with pytest.raises(SPM1DError):
        spm1d.stats.anova2onerm(y, np.array([0,0,1,1]), np.array([0,1,0,1]),
                                np.array([0,0,0,0]), equal_var=True)


#  Replicated designs must be unaffected.

def test_replicated_anova2_runs():
    A,B  = _balanced((3,4), 2)
    rng  = np.random.default_rng(0)
    spms = spm1d.stats.anova2(rng.normal(size=A.size), A, B, equal_var=True)
    assert [int(f.df[1]) for f in spms] == [12, 12, 12]
