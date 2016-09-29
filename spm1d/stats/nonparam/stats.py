
# Copyright (C) 2016  Todd Pataky

import numpy as np
from . import permuters, _snpm, _snpmlist



def _get_data_dim(y, ismultivariate=False):
	n = np.asarray(y).ndim
	return (n - 2) if ismultivariate else (n - 1)

def _get_snpm(STAT, perm, nFactors=None):
	z            = perm.get_test_stat_original()
	if STAT == 'T':
		snpm     = _snpm.SnPM0D_T(z, perm) if perm.dim==0 else _snpm.SnPM_T(z, perm)
	elif STAT == 'T2':
		snpm     = _snpm.SnPM0D_T2(z, perm) if perm.dim==0 else _snpm.SnPM_T2(z, perm)
	elif STAT == 'X2':
		snpm     = _snpm.SnPM0D_X2(z, perm) if perm.dim==0 else _snpm.SnPM_X2(z, perm)
	elif STAT == 'F':
		if isinstance(z, list):
			snpm = _snpmlist.SnPMFList0D(z, perm, nFactors=nFactors) if perm.dim==0 else _snpmlist.SnPMFList(z, perm, nFactors=nFactors)
		else:
			snpm = _snpm.SnPM0D_F(z, perm) if perm.dim==0 else _snpm.SnPM_F(z, perm)
	return snpm





### One-way ANOVA:
def anova1(y, A, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA10D(y, A) if dim==0 else permuters.PermuterANOVA11D(y, roi, A)
	return _get_snpm( 'F', perm )
def anova1rm(y, A, SUBJ, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA1rm0D(y, A, SUBJ) if dim==0 else permuters.PermuterANOVA1rm1D(y, roi, A, SUBJ)
	return _get_snpm( 'F', perm )

### Two-way ANOVA:
def anova2(y, A, B, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA20D(y, A, B) if dim==0 else permuters.PermuterANOVA21D(y, roi, A, B)
	return _get_snpm( 'F', perm, nFactors=2 )
def anova2nested(y, A, B, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA2nested0D(y, A, B) if dim==0 else permuters.PermuterANOVA2nested1D(y, roi, A, B)
	return _get_snpm( 'F', perm, nFactors=2 )
def anova2onerm(y, A, B, SUBJ, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA2onerm0D(y, A, B, SUBJ) if dim==0 else permuters.PermuterANOVA2onerm1D(y, roi, A, B, SUBJ)
	return _get_snpm( 'F', perm, nFactors=2 )
def anova2rm(y, A, B, SUBJ, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA2rm0D(y, A, B, SUBJ) if dim==0 else permuters.PermuterANOVA2rm1D(y, roi, A, B, SUBJ)
	return _get_snpm( 'F', perm, nFactors=2 )

### Three-way ANOVA:
def anova3(y, A, B, C, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA30D(y, A, B, C) if dim==0 else permuters.PermuterANOVA31D(y, roi, A, B, C)
	return _get_snpm( 'F', perm, nFactors=3 )
def anova3nested(y, A, B, C, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA3nested0D(y, A, B, C) if dim==0 else permuters.PermuterANOVA3nested1D(y, roi, A, B, C)
	return _get_snpm( 'F', perm, nFactors=3 )
def anova3onerm(y, A, B, C, SUBJ, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA3onerm0D(y, A, B, C, SUBJ) if dim==0 else permuters.PermuterANOVA3onerm1D(y, roi, A, B, C, SUBJ)
	return _get_snpm( 'F', perm, nFactors=3 )
def anova3tworm(y, A, B, C, SUBJ, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA3tworm0D(y, A, B, C, SUBJ) if dim==0 else permuters.PermuterANOVA3tworm1D(y, roi, A, B, C, SUBJ)
	return _get_snpm( 'F', perm, nFactors=3 )
def anova3rm(y, A, B, C, SUBJ, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterANOVA3rm0D(y, A, B, C, SUBJ) if dim==0 else permuters.PermuterANOVA3rm1D(y, roi, A, B, C, SUBJ)
	return _get_snpm( 'F', perm, nFactors=3 )
	





### Basic multivariate tests:
def cca(y, x, roi=None):
	dim     = _get_data_dim(y, ismultivariate=True)
	perm    = permuters.PermuterCCA1D(y, x, roi=roi) if dim==1 else permuters.PermuterCCA0D(y, x)
	return _get_snpm('X2', perm)

def hotellings(y, mu=None, roi=None):
	dim     = _get_data_dim(y, ismultivariate=True)
	perm    = permuters.PermuterHotellings1D(y, mu, roi=roi) if dim==1 else permuters.PermuterHotellings0D(y, mu)
	return _get_snpm('T2', perm)

def hotellings_paired(yA, yB, roi=None):
	return hotellings( yA - yB, roi=roi )

def hotellings2(yA, yB, roi=None):
	dim     = _get_data_dim(yA, ismultivariate=True)
	perm    = permuters.PermuterHotellings21D(yA, yB, roi=roi) if dim==1 else permuters.PermuterHotellings20D(yA, yB)
	return _get_snpm('T2', perm)

def manova1(y, A, roi=None):
	dim     = _get_data_dim(y, ismultivariate=True)
	perm    = permuters.PermuterMANOVA10D(y, A) if dim==0 else permuters.PermuterMANOVA11D(y, roi, A)
	return _get_snpm( 'X2', perm )





### Basic univariate tests:
def regress(y, x, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterRegress1D(y, x, roi=roi) if dim==1 else permuters.PermuterRegress0D(y, x)
	return _get_snpm('T', perm)

def ttest(y, mu=0, roi=None):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterTtest1D(y, mu, roi=roi) if dim==1 else permuters.PermuterTtest0D(y, mu)
	return _get_snpm('T', perm)

def ttest_paired(yA, yB, roi=None):
	return ttest(yA-yB, 0, roi=roi)

def ttest2(yA, yB, roi=None):
	dim     = _get_data_dim(yA)
	perm    = permuters.PermuterTtest21D(yA, yB, roi=roi) if dim==1 else permuters.PermuterTtest20D(yA, yB)
	return _get_snpm('T', perm)




