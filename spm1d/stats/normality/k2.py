
'''
Normality testing

All procedures fit the given model, calculate residuals then
"normality.residuals" to conduct a D'Agostino-Pearson K2 test
on the residuals.
'''

# Copyright (C) 2016  Todd Pataky

from math import log
import numpy as np
from .. _spm import SPM0D_X2, SPM_X2
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
from ... import rft1d



def k2_single_node(x):
	'''
	Compute the D'Agostino-Pearson K2 test statistic at a single node.
	
	This code is modified from "DagosPtest.m" by Antonio Trujillo-Ortiz available at:
	https://mathworks.com/matlabcentral/fileexchange/3954-dagosptest/content/DagosPtest.m
	and is based on the methods described in the paper below:
	
	D'Agostino, Ralph B.; Albert Belanger; Ralph B. D'Agostino, Jr (1990)
	"A suggestion for using powerful and informative tests of normality"
	The American Statistician 44(4): 316-321.  doi:10.2307/2684359
	
	See also:
	https://en.wikipedia.org/wiki/D%27Agostino%27s_K-squared_test
	
	"DagosPtest.m" authors:
	
	A. Trujillo-Ortiz and R. Hernandez-Walls
	Facultad de Ciencias Marinas
	Universidad Autonoma de Baja California
	Apdo. Postal 453
	Ensenada, Baja California
	Mexico.
	atrujo@uabc.mx
	
	
	------------ LICENSE -------------------------------------------
	
	Copyright (c) 2015, Antonio Trujillo-Ortiz
	All rights reserved.

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are
	met:

	    * Redistributions of source code must retain the above copyright
	      notice, this list of conditions and the following disclaimer.
	    * Redistributions in binary form must reproduce the above copyright
	      notice, this list of conditions and the following disclaimer in
	      the documentation and/or other materials provided with the distribution

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
	ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
	LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
	CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
	SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
	POSSIBILITY OF SUCH DAMAGE.
	'''
	### sort data:
	n   = float( x.size )
	x   = np.sort( np.asarray(x, dtype=float) )
	### estimate skewness and kurtosis:
	s1  = x.sum()
	s2  = (x**2).sum()
	s3  = (x**3).sum()
	s4  = (x**4).sum()
	SS  = s2 - (s1**2 / n)
	v   = SS / (n-1)
	k3  = ((n*s3)-(3*s1*s2)+((2*(s1**3))/n))/((n-1)*(n-2))
	g1  = k3 / (v**1.5)
	k4  = ((n+1)*((n*s4)-(4*s1*s3)+(6*(s1**2)*(s2/n))-((3*(s1**4))/(n**2)))/((n-1)*(n-2)*(n-3)))-((3*(SS**2))/((n-2)*(n-3)))
	g2  = k4/v**2
	eg1 = ((n-2)*g1)/ (n*(n-1))**0.5                         #skewness
	eg2 = ((n-2)*(n-3)*g2)/((n+1)*(n-1))+((3*(n-1))/(n+1))   #kurtosis
	### transformed sample skewness:
	A   = eg1 * (((n+1)*(n+3))/(6*(n-2)))**0.5
	B   = (3*((n**2)+(27*n)-70)*((n+1)*(n+3)))/((n-2)*(n+5)*(n+7)*(n+9))
	C   = (2*(B-1))**0.5 - 1
	D   = C**0.5
	E   = 1/ log(D)**0.5
	F   = A / (2/(C-1))**0.5
	Zg1 = E* log( F + (F**2+1)**0.5 )                        #transformed skewness
	### transformed sample kurtosis:
	G   = (24*n*(n-2)*(n-3))/((n+1)**2*(n+3)*(n+5))
	H   = ((n-2)*(n-3)*g2)/((n+1)*(n-1)* G**0.5)
	J   = ((6*(n**2-(5*n)+2))/((n+7)*(n+9))) * ((6*(n+3)*(n+5))/((n*(n-2)*(n-3))))**0.5
	K   = 6+((8/J)*((2/J) + (1+(4/J**2))**0.5   )   )
	L   = (1-(2/K))/(1+H * (2/(K-4))**0.5   )
	Zg2 = (1-(2/(9*K))-L**(1./3)) / (2/(9*K))**0.5           #transformed kurtosis
	### D'Agostino-Pearson test statistic:
	k2  = Zg1**2 + Zg2**2
	return k2


def residuals(y):
	'''
	Compute the D'Agostino-Pearson K2 test statistic continuum for a set of
	model residuals.
	'''
	J  = y.shape[0]
	if J < 8:
		raise( ValueError('In order to conduct a normality test there must at least 8 observations. Only %d found.' %J)   )
	df     = 1, 2
	if np.ndim(y)==1:
		k2     = k2_single_node(y)
		spm    = SPM0D_X2(k2, df, residuals=y)
	else:
		k2     = np.array( [k2_single_node(yy)   for yy in y.T] )
		fwhm   = rft1d.geom.estimate_fwhm(y)
		resels = rft1d.geom.resel_counts(y, fwhm, element_based=False)
		spm    = SPM_X2(k2, df, fwhm, resels, residuals=y)
	return spm




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







