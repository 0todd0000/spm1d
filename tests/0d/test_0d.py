

import pytest
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
    datasets = []
    datasets.append(  spm1d.data.uv0d.t1.RSWeightReduction()  )
    datasets.append(  spm1d.data.uv0d.t1.ColumbiaSalmonella()  )
    for dataset in datasets:
        y,mu    = dataset.get_data()
        spm     = spm1d.stats.ttest(y, mu).inference(0.05, two_tailed=False)
        assert dataset.z == pytest.approx(spm.z, abs=1e-4)
        assert dataset.df == pytest.approx(spm.df, abs=1e-4)
        assert dataset.p == pytest.approx(spm.p, abs=1e-4)

def test_ttest_paired():
    datasets = []
    datasets.append(  spm1d.data.uv0d.tpaired.RSWeightClinic()  )
    datasets.append(  spm1d.data.uv0d.tpaired.ColumbiaMileage()  )
    for dataset in datasets:
        y0,y1   = dataset.get_data()
        spm     = spm1d.stats.ttest_paired(y0, y1).inference(0.05, two_tailed=False)
        assert dataset.z == pytest.approx(spm.z, abs=1e-4)
        assert dataset.df == pytest.approx(spm.df, abs=1e-4)
        assert dataset.p == pytest.approx(spm.p, abs=1e-4)

def test_ttest2():
    datasets = []
    datasets.append(  spm1d.data.uv0d.t2.RSFlavor()  )
    datasets.append(  spm1d.data.uv0d.t2.ColumbiaPlacebo()  )
    for dataset in datasets:
        yA,yB   = dataset.get_data()
        spm     = spm1d.stats.ttest2(yA, yB, equal_var=True).inference(0.05, two_tailed=False)
        assert dataset.z == pytest.approx(spm.z, abs=1e-4)
        assert dataset.df == pytest.approx(spm.df, abs=1e-4)
        assert dataset.p == pytest.approx(spm.p, abs=1e-4)

def test_regress():
    datasets = []
    datasets.append(  spm1d.data.uv0d.regress.RSRegression()  )
    datasets.append(  spm1d.data.uv0d.regress.ColumbiaHeadCircumference()  )
    for dataset in datasets:
        y,x     = dataset.get_data()
        spm     = spm1d.stats.regress(y, x).inference(0.05, two_tailed=True)
        assert dataset.z == pytest.approx(spm.z, abs=1e-4)
        assert dataset.df == pytest.approx(spm.df, abs=1e-4)
        assert dataset.p == pytest.approx(spm.p, abs=1e-4)




def test_anova1():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova1.Cars()  )
    datasets.append(  spm1d.data.uv0d.anova1.Sound()  )
    datasets.append(  spm1d.data.uv0d.anova1.Southampton1()  )
    datasets.append(  spm1d.data.uv0d.anova1.ConstructionUnequalSampleSizes()  )
    datasets.append(  spm1d.data.uv0d.anova1.RSUnequalSampleSizes()  )
    for dataset in datasets:
        y,A     = dataset.get_data()
        spm     = spm1d.stats.anova1(y, A, equal_var=True).inference(0.05)
        assert dataset.z == pytest.approx(spm.z, abs=1e-2)
        assert dataset.df == pytest.approx(spm.df, abs=1e-4)
        _assert_p(dataset.p, spm.p, tol=1e-3)


def test_anova1rm():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova1rm.Abdi2010()  )
    datasets.append(  spm1d.data.uv0d.anova1rm.Groceries()  )
    datasets.append(  spm1d.data.uv0d.anova1rm.Imacelebrity()  )
    datasets.append(  spm1d.data.uv0d.anova1rm.Southampton1rm()  )
    for dataset in datasets:
        y,A,S   = dataset.get_data()
        spm     = spm1d.stats.anova1rm(y, A, S, equal_var=True).inference(0.05)
        assert dataset.z == pytest.approx(spm.z, abs=1e-2)
        assert dataset.df == pytest.approx(spm.df, abs=1e-4)
        _assert_p(dataset.p, spm.p, tol=1e-3)

def test_anova2():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova2.Detergent()  )
    datasets.append(  spm1d.data.uv0d.anova2.Mouse()  )
    datasets.append(  spm1d.data.uv0d.anova2.Satisfaction()  )
    datasets.append(  spm1d.data.uv0d.anova2.SouthamptonCrossed1()  )
    datasets.append(  spm1d.data.uv0d.anova2.SPM1D3x3()  )
    datasets.append(  spm1d.data.uv0d.anova2.SPM1D3x4()  )
    datasets.append(  spm1d.data.uv0d.anova2.SPM1D3x5()  )
    datasets.append(  spm1d.data.uv0d.anova2.SPM1D4x4()  )
    datasets.append(  spm1d.data.uv0d.anova2.SPM1D4x5()  )

    for dataset in datasets:
        y,A,B   = dataset.get_data()
        spms    = spm1d.stats.anova2(y, A, B, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-2)
            assert df == pytest.approx(spm.df, abs=1e-4)
            _assert_p(p, spm.p, tol=1e-3)



def test_anova2nested():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova2nested.QIMacros()  )
    datasets.append(  spm1d.data.uv0d.anova2nested.SouthamptonNested1()  )

    for dataset in datasets:
        y,A,B   = dataset.get_data()
        spms    = spm1d.stats.anova2nested(y, A, B, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-2)
            assert df == pytest.approx(spm.df, abs=1e-4)
            _assert_p(p, spm.p, tol=1e-3)


def test_anova2onerm():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova2onerm.RSXLDrug()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.Santa23()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.Southampton2onerm()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x3()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x4()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x4A()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D3x5()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D4x4()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.SPM1D4x5()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.Santa23UnequalSampleSizes()  )
    datasets.append(  spm1d.data.uv0d.anova2onerm.Southampton2onermUnequalSampleSizes()  )

    for dataset in datasets:
        y,A,B,S = dataset.get_data()
        spms    = spm1d.stats.anova2onerm(y, A, B, S, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-2)
            assert df == pytest.approx(spm.df, abs=1e-3)
            _assert_p(p, spm.p, tol=1e-3)



def test_anova2rm():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova2rm.Antidepressant()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.RSXLTraining()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.SocialNetworks()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.Southampton2rm()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D3x3()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D3x4()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D3x5()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D4x4()  )
    datasets.append(  spm1d.data.uv0d.anova2rm.SPM1D4x5()  )

    for dataset in datasets:
        y,A,B,S = dataset.get_data()
        spms    = spm1d.stats.anova2rm(y, A, B, S, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-2)
            assert df == pytest.approx(spm.df, abs=1e-3)
            _assert_p(p, spm.p, tol=1e-3)


def test_anova3():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova3.RSItalian()  )
    datasets.append(  spm1d.data.uv0d.anova3.SouthamptonFullyCrossedMixed()  )

    for dataset in datasets:
        y,A,B,C = dataset.get_data()
        spms    = spm1d.stats.anova3(y, A, B, C, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-2)
            assert df == pytest.approx(spm.df, abs=1e-3)
            _assert_p(p, spm.p, tol=1e-3)



def test_anova3nested():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova3nested.SouthamptonNested3()  )

    for dataset in datasets:
        y,A,B,C = dataset.get_data()
        spms    = spm1d.stats.anova3nested(y, A, B, C, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-2)
            assert df == pytest.approx(spm.df, abs=1e-3)
            _assert_p(p, spm.p, tol=1e-3)



def test_anova3onerm():
    datasets = []
    datasets.append(  spm1d.data.uv0d.anova3onerm.NYUCaffeine()  )
    datasets.append(  spm1d.data.uv0d.anova3onerm.Southampton3onerm()  )

    for dataset in datasets:
        y,A,B,C,S = dataset.get_data()
        spms      = spm1d.stats.anova3onerm(y, A, B, C, S, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-1)
            assert df == pytest.approx(spm.df, abs=1e-3)
            _assert_p(p, spm.p, tol=1e-3)


def test_anova3rm():
    datasets = []
    datasets.append(   spm1d.data.uv0d.anova3rm.SPM1D2x2x2()   )
    datasets.append(   spm1d.data.uv0d.anova3rm.SPM1D2x3x5()   )
    datasets.append(   spm1d.data.uv0d.anova3rm.SPM1D3x3x3()   )


    for dataset in datasets:
        y,A,B,C,S = dataset.get_data()
        spms      = spm1d.stats.anova3rm(y, A, B, C, S, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-3)
            assert df == pytest.approx(spm.df, abs=1e-3)
            _assert_p(p, spm.p, tol=1e-3)


def test_anova3tworm():
    datasets = []
    datasets.append(   spm1d.data.uv0d.anova3tworm.NYUHiringExperience()   )
    datasets.append(   spm1d.data.uv0d.anova3tworm.Southampton3tworm()   )


    for dataset in datasets:
        y,A,B,C,S = dataset.get_data()
        spms      = spm1d.stats.anova3tworm(y, A, B, C, S, equal_var=True).inference(0.05)
        for spm,z,df,p in zip(spms, dataset.z, dataset.df, dataset.p):
            assert z == pytest.approx(spm.z, abs=1e-1)
            assert df == pytest.approx(spm.df, abs=1e-3)
            _assert_p(p, spm.p, tol=1e-3)


