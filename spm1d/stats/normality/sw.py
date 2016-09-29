
'''
Normality testing using the Shapiro-Wilks statistic

'''

# Copyright (C) 2016  Todd Pataky

import numpy as np
from scipy import stats
from .. t import regress as _main_regress
from .. anova import anova1 as _main_anova1
from .. anova import anova1rm as _main_anova1rm
from .. anova import anova2 as _main_anova2
from .. anova import anova2nested as _main_anova2nested
from .. anova import anova2rm as _main_anova2rm
from .. anova import anova2onerm as _main_anova2onerm
from .. anova import anova3 as _main_anova3
from .. anova import anova3nested as _main_anova3nested
from .. anova import anova3rm as _main_anova3rm
from .. anova import anova3onerm as _main_anova3onerm
from .. anova import anova3tworm as _main_anova3tworm


def sw_single_node(x):
	w,p = stats.shapiro(x)
	return w,p

def residuals(y):
	J  = y.shape[0]
	if np.ndim(y)==1:
		w,p    = sw_single_node(y)
	else:
		w,p    = np.array( [sw_single_node(yy) for yy in y.T] ).T
	return w,p



def _stack_data(*args):
	return np.hstack(args) if (np.ndim(args[0])==1) else np.vstack(args)


def anova1(y, A):
	spm  = _main_anova1(y, A)
	return residuals( spm.residuals )
def anova1rm(y, A, SUBJ):
	spm  = _main_anova1rm(y, A, SUBJ, _force_approx0D=True)
	return residuals( spm.residuals )

def anova2(y, A, B):
	spm  = _main_anova2(y, A, B)
	return residuals( spm[0].residuals )
def anova2nested(y, A, B):
	spm  = _main_anova2nested(y, A, B)
	return residuals( spm[0].residuals )
def anova2onerm(y, A, B, SUBJ):
	spm  = _main_anova2onerm(y, A, B, SUBJ, _force_approx0D=True)
	return residuals( spm[0].residuals )
def anova2rm(y, A, B, SUBJ):
	spm  = _main_anova2rm(y, A, B, SUBJ, _force_approx0D=True)
	return residuals( spm[0].residuals )


def anova3(y, A, B, C):
	spm  = _main_anova3(y, A, B, C)
	return residuals( spm[0].residuals )
def anova3nested(y, A, B, C):
	spm  = _main_anova3nested(y, A, B, C)
	return residuals( spm[0].residuals )
def anova3onerm(y, A, B, C, SUBJ):
	spm  = _main_anova3onerm(y, A, B, C, SUBJ, _force_approx0D=True)
	return residuals( spm[0].residuals )
def anova3tworm(y, A, B, C, SUBJ):
	spm  = _main_anova3tworm(y, A, B, C, SUBJ, _force_approx0D=True)
	return residuals( spm[0].residuals )
def anova3rm(y, A, B, C, SUBJ):
	spm  = _main_anova3rm(y, A, B, C, SUBJ, _force_approx0D=True)
	return residuals( spm[0].residuals )



def regress(y, x):
	spm  = _main_regress(y, x)
	return residuals( spm.residuals )


def ttest(y):
	r   = y - y.mean(axis=0)
	return residuals(r)

def ttest_paired(yA, yB):
	return ttest( yA - yB )
	
def ttest2(yA, yB):
	rA   = yA - yA.mean(axis=0)
	rB   = yB - yB.mean(axis=0)
	r    = _stack_data(rA, rB)
	return residuals(r)
