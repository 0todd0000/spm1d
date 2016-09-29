
'''
Confidence intervals (non-parametric)

If the CI cloud starting from the "datum" reaches the "criterion", the null hypothesis is rejected.
'''

# Copyright (C) 2016  Todd Pataky


import numpy as np
from .. ci import CIOneSample0D, CIOneSample1D
from .. ci import CIPairedSample0D, CIPairedSample1D, CIPairedDifference0D, CIPairedDifference1D
from .. ci import CITwoSample0D, CITwoSample1D, CITwoSampleDifference0D, CITwoSampleDifference1D
from ... stats import ttest as ttest_parametric
from ... stats import ttest2 as ttest2_parametric
from . stats import ttest, ttest2




class _NonParametricCI(object):
	isparametric   = False
class _NonParametricCI0D(_NonParametricCI):
	name           = '0D Non-Parametric Confidence Interval'
class _NonParametricCI1D(_NonParametricCI):
	name           = '1D Non-Parametric Confidence Interval'




class CIOneSample0DNP(_NonParametricCI0D, CIOneSample0D):
	pass
class CIOneSample1DNP(_NonParametricCI1D, CIOneSample1D):
	pass


class CIPairedSample0DNP(_NonParametricCI0D, CIPairedSample0D):
	pass
class CIPairedSample1DNP(_NonParametricCI1D, CIPairedSample1D):
	pass
class CIPairedDifference1DNP(_NonParametricCI0D, CIPairedDifference1D):
	pass
class CIPairedDifference0DNP(_NonParametricCI1D, CIPairedDifference0D):
	pass


class CITwoSampleDifference0DNP(_NonParametricCI0D, CITwoSampleDifference0D):
	pass
class CITwoSampleDifference1DNP(_NonParametricCI1D, CITwoSampleDifference1D):
	pass
class CITwoSample0DNP(_NonParametricCI0D, CITwoSample0D):
	pass
class CITwoSample1DNP(_NonParametricCI1D, CITwoSample1D):
	pass






def _snpmi2spmi(snpmi):
	snpmi.zstar  = snpmi.zstar if np.size(snpmi.zstar)==1 else max(snpmi.zstar)
	snpmi.df     = None
	snpmi.fwhm   = None
	snpmi.resels = None
	return snpmi



def ci_onesample(y, alpha=0.05, mu=None, iterations=-1):
	spmi        = ttest(y, mu).inference(alpha, two_tailed=True, iterations=iterations)
	spmi        = _snpmi2spmi(spmi)
	mean,s      = y.mean(axis=0), y.std(axis=0, ddof=1)
	hstar       = spmi.zstar * s / y.shape[0]**0.5
	CIClass     = CIOneSample1DNP if spmi.dim==1 else CIOneSample0DNP
	return CIClass(spmi, mean, hstar, mu)



def ci_pairedsample(yA, yB, alpha=0.05, datum='difference', mu=None, iterations=-1):
	spmi     = ttest(yA-yB, 0).inference(alpha, two_tailed=True, iterations=iterations)
	spmi     = _snpmi2spmi(spmi)
	mA,mB    = yA.mean(axis=0), yB.mean(axis=0)   #sample means
	spmparam = ttest_parametric(yA-yB, 0)
	s        = spmparam.sigma2**0.5                   #sample standard deviation
	hstar    = spmi.zstar * s / yA.shape[0]**0.5  #CI height
	if datum=='difference':
		CIClass  = CIPairedDifference1DNP if spmi.dim==1 else CIPairedDifference0DNP
		ci       = CIClass(spmi, mA-mB, hstar, mu)
	else:
		CIClass  = CIPairedSample1DNP if spmi.dim==1 else CIPairedSample0DNP
		ci       = CIClass(spmi, mA, mB, hstar, mu)
	return ci



def ci_twosample(yA, yB, alpha=0.05, datum='difference', mu=None, iterations=-1):
	spmi         = ttest2(yA, yB).inference(alpha, two_tailed=True, iterations=iterations)
	spmi         = _snpmi2spmi(spmi)
	JA,JB        = yA.shape[0], yB.shape[0]
	spmparam     = ttest2_parametric(yA, yB, equal_var=True)
	mA,mB        = spmparam.beta            #sample means
	s            = spmparam.sigma2**0.5     #sample standard deviation
	hstar        = spmi.zstar * s * (1./JA + 1./JB)**0.5
	if datum == 'difference':
		CIClass  = CITwoSampleDifference1DNP if spmi.dim==1 else CITwoSampleDifference0DNP
		ci       = CIClass(spmi, mA-mB, hstar, mu)
	else:
		CIClass  = CITwoSample1DNP if spmi.dim==1 else CITwoSample0DNP
		ci       = CIClass(spmi, mA, mB, hstar, mu)
	return ci



