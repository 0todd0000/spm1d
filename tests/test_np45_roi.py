
'''
Tests for new nonparametric inference routines that were
added to version 0.4.50 in June 2025

For 1D analysis including ROIs:
  - comparison of parametric and nonparametric results
'''


import pytest
import numpy as np
import spm1d



def _assert_p(p0, p1, tol=1e-5):
    if p0 == '<0.001':
        assert p1 < 0.001
    elif p0 == '<0.05':
        assert p1 < 0.05
    elif p0 == '<0.01':
        assert p1 < 0.01
    elif p0 == '>0.05':
        assert p1 > 0.05
    else:
        assert p0 == pytest.approx(p1, abs=tol)



def test_ttest():
    alpha       = 0.05
    two_tailed  = True
    datasets    = []
    datasets.append(  spm1d.data.uv1d.t1.Random()  )
    datasets.append(  spm1d.data.uv1d.t1.SimulatedPataky2015a()  )
    datasets.append(  spm1d.data.uv1d.t1.SimulatedPataky2015b()  )
    zctols      = [0.3, 0.2, 0.1]
    for i,(dataset,zctol) in enumerate( zip(datasets, zctols) ):
        np.random.seed(i)
        y,mu    = dataset.get_data()
        roi     = np.array( [False]*y.shape[1] )
        roi[70:80] = True
        spm     = spm1d.stats.ttest(y, mu, roi=roi).inference(alpha, two_tailed=two_tailed)
        snpm    = spm1d.stats.nonparam.ttest(y, mu, roi=roi)
        niter   = -1 if snpm.nPermUnique < 10000 else 1000
        snpm    = snpm.inference(alpha, two_tailed=two_tailed, iterations=niter)
        assert np.ma.allclose(spm.z, snpm.z, atol=1e-4)
        assert spm.zstar == pytest.approx(snpm.zstar, abs=zctol)
        for p in snpm.p:
            assert (p>=snpm.mgr.minp) and (p<=alpha)

def test_ttest_paired():
    alpha       = 0.05
    two_tailed  = True
    datasets    = []
    datasets.append(  spm1d.data.uv1d.t2.PlantarArchAngle()  )
    zctols      = [0.3]
    for i,(dataset,zctol) in enumerate( zip(datasets, zctols) ):
        np.random.seed(i)
        y0,y1   = dataset.get_data()
        roi     = np.array( [False]*y0.shape[1] )
        roi[70:80] = True
        spm     = spm1d.stats.ttest_paired(y1, y0, roi=roi).inference(alpha, two_tailed=two_tailed)
        snpm    = spm1d.stats.nonparam.ttest_paired(y1, y0, roi=roi)
        niter   = -1 if snpm.nPermUnique < 10000 else 1000
        snpm    = snpm.inference(alpha, two_tailed=two_tailed, iterations=niter)
        assert np.ma.allclose(spm.z, snpm.z, atol=1e-4)
        assert spm.zstar == pytest.approx(snpm.zstar, abs=zctol)
        for p in snpm.p:
            assert (p>=snpm.mgr.minp) and (p<=alpha)


class _SmallSampleLargePosNegEffects6(object):
    def __init__(self):
        n  = 6
        y0 = np.random.randn(n,101)
        y1 = np.random.randn(n,101) + 2*np.sin( np.linspace(0,10,101) )
        y0 = spm1d.util.smooth(y0, 8)
        y1 = spm1d.util.smooth(y1, 8)
        self.y0 = y0
        self.y1 = y1
    def get_data(self):
        return self.y0, self.y1


def test_ttest2():
    alpha       = 0.05
    two_tailed  = True
    datasets = []
    datasets.append(  spm1d.data.uv1d.t2.PlantarArchAngle()  )
    datasets.append(  _SmallSampleLargePosNegEffects6()  )
    zctols      = [0.2, 0.2]
    for i,(dataset,zctol) in enumerate( zip(datasets, zctols) ):
        np.random.seed(i)
        y0,y1   = dataset.get_data()
        roi     = np.array( [False]*y0.shape[1] )
        roi[70:80] = True
        spm     = spm1d.stats.ttest2(y1, y0, roi=roi).inference(alpha, two_tailed=two_tailed)
        snpm    = spm1d.stats.nonparam.ttest2(y1, y0, roi=roi)
        niter   = -1 if snpm.nPermUnique < 10000 else 1000
        snpm    = snpm.inference(alpha, two_tailed=two_tailed, iterations=niter)
        assert np.ma.allclose(spm.z, snpm.z, atol=1e-4)
        assert spm.zstar == pytest.approx(snpm.zstar, abs=zctol)
        for p in snpm.p:
            assert (p>=snpm.mgr.minp) and (p<=alpha)

def test_regress():
    alpha       = 0.05
    two_tailed  = True
    datasets = []
    datasets.append(  spm1d.data.uv1d.regress.SimulatedPataky2015c()  )
    datasets.append(  spm1d.data.uv1d.regress.SpeedGRF()  )
    zctols      = [0.2, 0.2]
    for i,(dataset,zctol) in enumerate( zip(datasets, zctols) ):
        np.random.seed(i)
        y,x     = dataset.get_data()
        roi     = np.array( [False]*y.shape[1] )
        roi[70:80] = True
        spm     = spm1d.stats.regress(y, x, roi=roi).inference(alpha, two_tailed=two_tailed)
        snpm    = spm1d.stats.nonparam.regress(y, x, roi=roi)
        niter   = -1 if snpm.nPermUnique < 10000 else 1000
        snpm    = snpm.inference(alpha, two_tailed=two_tailed, iterations=niter)
        assert np.ma.allclose(spm.z, snpm.z, atol=1e-4)
        assert spm.zstar == pytest.approx(snpm.zstar, abs=zctol)
        for p in snpm.p:
            assert (p>=snpm.mgr.minp) and (p<=alpha)



#
# def test_anova1():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova1.Cars()  )
#     datasets.append(  spm1d.data.uv0d.anova1.Sound()  )
#     datasets.append(  spm1d.data.uv0d.anova1.Southampton1()  )
#     datasets.append(  spm1d.data.uv0d.anova1.ConstructionUnequalSampleSizes()  )
#     datasets.append(  spm1d.data.uv0d.anova1.RSUnequalSampleSizes()  )
#     for dataset in datasets:
#         y,A     = dataset.get_data()
#         spm     = spm1d.stats.anova1(y, A, equal_var=True).inference(0.05)
#         assert dataset.z == pytest.approx(spm.z, abs=1e-2)
#         assert dataset.df == pytest.approx(spm.df, abs=1e-4)
#         _assert_p(dataset.p, spm.p, tol=1e-3)
#
#
# def test_anova1rm():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova1rm.Abdi2010()  )
#     datasets.append(  spm1d.data.uv0d.anova1rm.Groceries()  )
#     datasets.append(  spm1d.data.uv0d.anova1rm.Imacelebrity()  )
#     datasets.append(  spm1d.data.uv0d.anova1rm.Southampton1rm()  )
#     for dataset in datasets:
#         y,A,S   = dataset.get_data()
#         spm     = spm1d.stats.anova1rm(y, A, S, equal_var=True).inference(0.05)
#         assert dataset.z == pytest.approx(spm.z, abs=1e-2)
#         assert dataset.df == pytest.approx(spm.df, abs=1e-4)
#         _assert_p(dataset.p, spm.p, tol=1e-3)
#
# def test_anova2():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova2.Detergent()  )
#     datasets.append(  spm1d.data.uv0d.anova2.Mouse()  )
#     datasets.append(  spm1d.data.uv0d.anova2.Satisfaction()  )
#     datasets.append(  spm1d.data.uv0d.anova2.SouthamptonCrossed1()  )
#     datasets.append(  spm1d.data.uv0d.anova2.SPM1D3x3()  )
#     datasets.append(  spm1d.data.uv0d.anova2.SPM1D3x4()  )
#     datasets.append(  spm1d.data.uv0d.anova2.SPM1D3x5()  )
#     datasets.append(  spm1d.data.uv0d.anova2.SPM1D4x4()  )
#     datasets.append(  spm1d.data.uv0d.anova2.SPM1D4x5()  )
#
#     for dataset in datasets:
#         y,A,B   = dataset.get_data()
#         spms    = spm1d.stats.anova2(y, A, B, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-2)
#             assert df == pytest.approx(spm.df, abs=1e-4)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
#
# def test_anova2nested():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova2nested.QIMacros()  )
#     datasets.append(  spm1d.data.uv0d.anova2nested.SouthamptonNested1()  )
#
#     for dataset in datasets:
#         y,A,B   = dataset.get_data()
#         spms    = spm1d.stats.anova2nested(y, A, B, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-2)
#             assert df == pytest.approx(spm.df, abs=1e-4)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
# def test_anova2onerm():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova2onerm.RSXLDrug()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.Santa23()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.Southampton2onerm()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x3()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x4()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x4A()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x5()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D4x4()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D4x5()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.Santa23UnequalSampleSizes()  )
#     datasets.append(  spm1d.data.uv0d.anova2onerm.Southampton2onermUnequalSampleSizes()  )
#
#     for dataset in datasets:
#         y,A,B,S = dataset.get_data()
#         spms    = spm1d.stats.anova2onerm(y, A, B, S, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-2)
#             assert df == pytest.approx(spm.df, abs=1e-3)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
#
# def test_anova2rm():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova2rm.Antidepressant()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.RSXLTraining()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.SocialNetworks()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.Southampton2rm()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D3x3()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D3x4()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D3x5()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D4x4()  )
#     datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D4x5()  )
#
#     for dataset in datasets:
#         y,A,B,S = dataset.get_data()
#         spms    = spm1d.stats.anova2rm(y, A, B, S, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-2)
#             assert df == pytest.approx(spm.df, abs=1e-3)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
# def test_anova3():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova3.RSItalian()  )
#     datasets.append(  spm1d.data.uv0d.anova3.SouthamptonFullyCrossedMixed()  )
#
#     for dataset in datasets:
#         y,A,B,C = dataset.get_data()
#         spms    = spm1d.stats.anova3(y, A, B, C, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-2)
#             assert df == pytest.approx(spm.df, abs=1e-3)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
#
# def test_anova3nested():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova3nested.SouthamptonNested3()  )
#
#     for dataset in datasets:
#         y,A,B,C = dataset.get_data()
#         spms    = spm1d.stats.anova3nested(y, A, B, C, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-2)
#             assert df == pytest.approx(spm.df, abs=1e-3)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
#
# def test_anova3onerm():
#     datasets = []
#     datasets.append(  spm1d.data.uv0d.anova3onerm.NYUCaffeine()  )
#     datasets.append(  spm1d.data.uv0d.anova3onerm.Southampton3onerm()  )
#
#     for dataset in datasets:
#         y,A,B,C,S = dataset.get_data()
#         spms      = spm1d.stats.anova3onerm(y, A, B, C, S, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-1)
#             assert df == pytest.approx(spm.df, abs=1e-3)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
# def test_anova3rm():
#     datasets = []
#     datasets.append(   spm1d.data.uv0d.anova3rm.SPM1D2x2x2()   )
#     datasets.append(   spm1d.data.uv0d.anova3rm.SPM1D2x3x5()   )
#     datasets.append(   spm1d.data.uv0d.anova3rm.SPM1D3x3x3()   )
#
#
#     for dataset in datasets:
#         y,A,B,C,S = dataset.get_data()
#         spms      = spm1d.stats.anova3rm(y, A, B, C, S, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-3)
#             assert df == pytest.approx(spm.df, abs=1e-3)
#             _assert_p(p, spm.p, tol=1e-3)
#
#
# def test_anova3tworm():
#     datasets = []
#     datasets.append(   spm1d.data.uv0d.anova3tworm.NYUHiringExperience()   )
#     datasets.append(   spm1d.data.uv0d.anova3tworm.Southampton3tworm()   )
#
#
#     for dataset in datasets:
#         y,A,B,C,S = dataset.get_data()
#         spms      = spm1d.stats.anova3tworm(y, A, B, C, S, equal_var=True).inference(0.05)
#         for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
#             assert z == pytest.approx(spm.z, abs=1e-1)
#             assert df == pytest.approx(spm.df, abs=1e-3)
#             _assert_p(p, spm.p, tol=1e-3)


