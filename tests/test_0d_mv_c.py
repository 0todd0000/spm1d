

import pytest
import numpy as np
import spm1d
import spm1d.stats.c



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



def test_hotellings():
    datasets = []
    datasets.append(   spm1d.data.mv0d.hotellings1.RSXLHotellings1()   )
    datasets.append(   spm1d.data.mv0d.hotellings1.Sweat()   )


    for dataset in datasets:
        y,mu  = dataset.get_data()
        spm   = spm1d.stats.c.hotellings(y, mu).inference(0.05)
        assert dataset.z == pytest.approx(spm.z, abs=1e-2)
        assert dataset.df == pytest.approx(spm.df, abs=1e-3)
        _assert_p(dataset.p, spm.p, tol=1e-3)



def test_hotellings_paired():
    datasets = []
    datasets.append(   spm1d.data.mv0d.hotellings_paired.NCSSBeforeAfter()   )
    datasets.append(   spm1d.data.mv0d.hotellings_paired.RSXLHotellingsPaired()   )


    for dataset in datasets:
        y0,y1 = dataset.get_data()
        y     = np.vstack( [y0,y1] )
        x     = np.asarray( [0]*y0.shape[0] + [1]*y1.shape[0] )
        spm   = spm1d.stats.c.hotellings_paired(y, x).inference(0.05)
        assert dataset.z == pytest.approx(spm.z, abs=1e-1)
        assert dataset.df == pytest.approx(spm.df, abs=1e-3)
        _assert_p(dataset.p, spm.p, tol=1e-3)


def test_hotellings2():
    datasets = []
    datasets.append(   spm1d.data.mv0d.hotellings2.RSXLHotellings2()   )
    datasets.append(   spm1d.data.mv0d.hotellings2.HELPHomeless()   )


    for dataset in datasets:
        y0,y1 = dataset.get_data()
        y     = np.vstack( [y0,y1] )
        x     = np.asarray( [0]*y0.shape[0] + [1]*y1.shape[0] )
        spm   = spm1d.stats.c.hotellings2(y, x).inference(0.05)
        assert dataset.z == pytest.approx(spm.z, abs=1e-1)
        assert dataset.df == pytest.approx(spm.df, abs=1e-3)
        _assert_p(dataset.p, spm.p, tol=1e-3)


def test_cca():
    datasets = []
    datasets.append(   spm1d.data.mv0d.cca.FitnessClub()   )
    datasets.append(   spm1d.data.mv0d.cca.StackExchange()   )


    for dataset in datasets:
        y,x   = dataset.get_data()
        spm   = spm1d.stats.c.cca(y, x).inference(0.05)
        assert dataset.z == pytest.approx(spm.z, abs=1e-1)
        assert dataset.df == pytest.approx(spm.df, abs=1e-3)
        _assert_p(dataset.p, spm.p, tol=1e-3)


def test_manova1():
    datasets = []
    datasets.append(   spm1d.data.mv0d.manova1.AnimalDepression()   )
    datasets.append(   spm1d.data.mv0d.manova1.Stevens2002()   )


    for dataset in datasets:
        y,A   = dataset.get_data()
        spm   = spm1d.stats.c.manova1(y, A).inference(0.05)
        assert dataset.z == pytest.approx(spm.z, abs=1e-1)
        assert dataset.df == pytest.approx(spm.df, abs=1e-3)
        _assert_p(dataset.p, spm.p, tol=1e-3)