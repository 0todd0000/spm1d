
import numpy as np
import permuters, _snpm



def _get_data_dim(y, ismultivariate=False):
	if ismultivariate:
		dim = np.asarray(y).ndim - 2
	else:
		dim = np.asarray(y).ndim - 1
	return dim

def _get_snpm(STAT, perm):
	z       = perm.get_test_stat_original()
	roi     = perm.roi
	if STAT == 'T':
		snpm    = _snpm.SnPM0D_T(z, perm) if perm.dim==0 else _snpm.SnPM_T(z, perm, roi)
	elif STAT == 'T2':
		snpm    = _snpm.SnPM0D_T2(z, perm) if perm.dim==0 else _snpm.SnPM_T2(z, perm, roi)
	elif STAT == 'X2':
		snpm    = _snpm.SnPM0D_X2(z, perm) if perm.dim==0 else _snpm.SnPM_X2(z, perm, roi)
	elif STAT == 'F':
		if isinstance(z, list):
			snpm = _snpm.SnPM0D_Flist(z, perm) if perm.dim==0 else _snpm.SnPM1D_Flist(z, perm, roi)
		else:
			snpm = _snpm.SnPM0D_F(z, perm) if perm.dim==0 else _snpm.SnPM0D(z, perm, roi)
	return snpm





### One-way ANOVA:
def anova1(y, A):
	return _get_snpm( 'F',   permuters.PermuterANOVA1(y, A)   )
def anova1rm(y, A, SUBJ):
	return _get_snpm( 'F',   permuters.PermuterANOVA1rm(y, A, SUBJ)   )
### Two-way ANOVA:
def anova2(y, A, B):
	return _get_snpm( 'F',  permuters.PermuterANOVA2(y, A, B)  )
def anova2nested(y, A, B):
	return _get_snpm( 'F',  permuters.PermuterANOVA2nested(y, A, B)  )
def anova2onerm(y, A, B, SUBJ):
	return _get_snpm( 'F',  permuters.PermuterANOVA2onerm(y, A, B, SUBJ)  )
def anova2rm(y, A, B, SUBJ):
	return _get_snpm( 'F',  permuters.PermuterANOVA2rm(y, A, B, SUBJ)  )
### Three-way ANOVA:
def anova3(y, A, B, C):
	return _get_snpm( 'F',  permuters.PermuterANOVA3(y, A, B, C)  )
def anova3nested(y, A, B, C):
	return _get_snpm( 'F',  permuters.PermuterANOVA3nested(y, A, B, C)  )
def anova3onerm(y, A, B, C, SUBJ):
	return _get_snpm( 'F',  permuters.PermuterANOVA3onerm(y, A, B, C, SUBJ)  )
def anova3tworm(y, A, B, C, SUBJ):
	return _get_snpm( 'F',  permuters.PermuterANOVA3tworm(y, A, B, C, SUBJ)  )
def anova3rm(y, A, B, C, SUBJ):
	return _get_snpm( 'F',  permuters.PermuterANOVA3rm(y, A, B, C, SUBJ)  )






### Basic multivariate tests:
def cca(y, x):
	dim     = _get_data_dim(y, ismultivariate=True)
	perm    = permuters.PermuterCCA1D(y, x) if dim==1 else permuters.PermuterCCA0D(y, x)
	return _get_snpm('X2', perm)

def hotellings(y, mu=None):
	dim     = _get_data_dim(y, ismultivariate=True)
	perm    = permuters.PermuterHotellings1D(y, mu) if dim==1 else permuters.PermuterHotellings0D(y, mu)
	return _get_snpm('T2', perm)

def hotellings_paired(yA, yB):
	return hotellings( yA - yB )

def hotellings2(yA, yB):
	dim     = _get_data_dim(yA, ismultivariate=True)
	perm    = permuters.PermuterHotellings21D(yA, yB) if dim==1 else permuters.PermuterHotellings20D(yA, yB)
	return _get_snpm('T2', perm)





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




