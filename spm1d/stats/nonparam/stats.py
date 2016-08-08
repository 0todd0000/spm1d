
import numpy as np
import permuters, _snpm



def _anova(perm):
	z      = perm.get_test_stat_original()
	if isinstance(z, list):
		spm = _snpm.SnPM0D_Flist(z, perm)
	else:
		spm = _snpm.SnPM0D_F(z, perm)
	return spm

def _build_snpm(STAT, z, perm):
	# is0d = np.size(z) == 0
	# print is0d
	if STAT == 'T':
		spm     = _snpm.SnPM0D_T(z, perm) if perm.dim==0 else _snpm.SnPM_T(z, perm)
	return spm

def _get_data_dim(y):
	return np.asarray(y).ndim - 1



def anova1(y, A):
	return _anova(   permuters.PermuterANOVA1(y, A)   )
def anova1rm(y, A, SUBJ):
	return _anova(   permuters.PermuterANOVA1rm(y, A, SUBJ)   )

def anova2(y, A, B):
	return _anova(  permuters.PermuterANOVA2(y, A, B)  )
def anova2nested(y, A, B):
	return _anova(  permuters.PermuterANOVA2nested(y, A, B)  )
def anova2onerm(y, A, B, SUBJ):
	return _anova(  permuters.PermuterANOVA2onerm(y, A, B, SUBJ)  )
def anova2rm(y, A, B, SUBJ):
	return _anova(  permuters.PermuterANOVA2rm(y, A, B, SUBJ)  )

def anova3(y, A, B, C):
	return _anova(  permuters.PermuterANOVA3(y, A, B, C)  )
def anova3nested(y, A, B, C):
	return _anova(  permuters.PermuterANOVA3nested(y, A, B, C)  )
def anova3onerm(y, A, B, C, SUBJ):
	return _anova(  permuters.PermuterANOVA3onerm(y, A, B, C, SUBJ)  )
def anova3tworm(y, A, B, C, SUBJ):
	return _anova(  permuters.PermuterANOVA3tworm(y, A, B, C, SUBJ)  )
def anova3rm(y, A, B, C, SUBJ):
	return _anova(  permuters.PermuterANOVA3rm(y, A, B, C, SUBJ)  )







def cca(y, x):
	perm    = permuters.PermuterCCA0D(y, x)
	z       = perm.get_test_stat_original()
	return _snpm.SnPM0D_X2(z, perm)

def hotellings(y, mu=None):
	perm    = permuters.PermuterHotellings0D(y, mu)
	z       = perm.get_test_stat_original()
	return _snpm.SnPM0D_T2(z, perm)

def hotellings_paired(yA, yB):
	perm    = permuters.PermuterHotellings0D(yA-yB, mu=None)
	z       = perm.get_test_stat_original()
	return _snpm.SnPM0D_T2(z, perm)

def hotellings2(yA, yB):
	perm    = permuters.PermuterHotellings20D(yA, yB)
	z       = perm.get_test_stat_original()
	return _snpm.SnPM0D_T2(z, perm)








def regress(y, x):
	perm    = permuters.PermuterRegress0D(y, x)
	z       = perm.get_test_stat_original()
	return _snpm.SnPM0D_T(z, perm)

def ttest(y, mu=0):
	dim     = _get_data_dim(y)
	perm    = permuters.PermuterTtest1D(y, mu) if dim==1 else permuters.PermuterTtest0D(y, mu)
	z       = perm.get_test_stat_original()
	return _build_snpm('T', z, perm)

def ttest_paired(yA, yB):
	return ttest(yA-yB, 0)

def ttest2(yA, yB):
	perm    = permuters.PermuterTtest20D(yA, yB)
	z       = perm.get_test_stat_original()
	return _snpm.SnPM0D_T(z, perm)




