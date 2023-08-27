'''
One- and two sample tests (using T contrasts).
'''

# Copyright (C) 2023  Todd Pataky



import numpy as np
from .. _dec import appendargs, checkargs
from .. _la import rank



def _assemble_spm_objects(design, model, fit, teststat, roi=None):
	if fit.dvdim==0:
		from .. _spmcls import SPM0D
		spm = SPM0D(design, model, fit, teststat)
	else:
		from .. _spmcls import SPM1D
		spm = SPM1D(design, model, fit, teststat)
	return spm
	





def glm(y, X, c, ctype='T', QQ=None, roi=None):
	'''
	General Linear Model
	
	Most general user-facing hypothesis testing function
	
	Note:  all built-in tests (e.g. ttest2, anova1rm, etc.)
	represent specific cases of this glm function.
	'''
	from . models import GeneralLinearModel
	df0       = 1, X.shape[0] - rank(X)
	model     = GeneralLinearModel(X, df0, QQ)
	fit       = model.fit( y )
	teststat  = fit.calculate_t_stat( c, roi=roi )
	return model, fit, teststat




@appendargs
@checkargs
def regress(y, x, roi=None):
	from . designs import REGRESS
	design = REGRESS(x)
	model,fit,teststat = glm(y, design.X, design.contrasts[0].C)
	spm    = _assemble_spm_objects(design, model, fit, teststat)
	spm.r  = spm.z / (  (spm.design.J - 2 + spm.z**2)**0.5)   # t = r * ((J-2)/(1-r*r) )**0.5
	# df0    = design.get_df0(y.shape[0])
	# print(df0)
	return spm



@appendargs
@checkargs
def ttest(y, mu=0, roi=None):
	from . designs import TTEST
	design    = TTEST(y, mu)
	# df0       = design.get_df0(y.shape[0])
	model,fit,teststat = glm(y-mu, design.X, design.contrasts[0].C)
	
	return _assemble_spm_objects(design, model, fit, teststat)
	
	

@appendargs
@checkargs
def ttest2(y0, y1, equal_var=False, roi=None):
	from . designs import TTEST2
	from .. _cov import CovarianceModel
	n0,n1     = y0.shape[0], y1.shape[0]
	y         = np.hstack( (y0,y1) ) if (y0.ndim==1) else np.vstack(  (y0, y1)  )
	design    = TTEST2(n0, n1)
	if equal_var:
		QQ    = None
		cmodel = CovarianceModel(design.X)
		# cmodel.add_constant_var()
	else:
		cmodel = CovarianceModel(design.X)
		cmodel.add_group_vars()
		# model.add_autocorr()
		QQ    = cmodel.get_model()

	model,fit,teststat = glm(y, design.X, design.contrasts[0].C, QQ=QQ)
	return _assemble_spm_objects(design, model, fit, teststat)


@checkargs
def ttest_paired(y0, y1, roi=None):
	return ttest(y0-y1, 0, roi=roi)



