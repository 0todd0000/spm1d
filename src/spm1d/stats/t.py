'''
One- and two sample tests (using T contrasts).
'''

# Copyright (C) 2023  Todd Pataky



import numpy as np
from . _dec import appendargs, checkargs



def _assemble_spm_objects(design, model, fit, teststat, roi=None):
	if fit.dvdim==0:
		from . _spmcls import SPM0D
		spm = SPM0D(design, model, fit, teststat)
	else:
		from . _spmcls import SPM1D
		spm = SPM1D(design, model, fit, teststat)
	return spm



def _glm_design(y, design, equal_var=False, roi=None):
	'''
	Design object-based interface to glm

	This is an internal function that is NOT meant for users.
	'''
	QQ         = design.get_variance_model( equal_var=equal_var )
	if design.is_single_contrast_design:
		spm    = glm(y, design.X, design.c, QQ=QQ, roi=roi)
	else:
		pass
	spm.design = design
	return spm


# def glm(y, X, c, ctype='T', QQ=None, roi=None):
# 	'''
# 	General Linear Model
#
# 	Most general user-facing hypothesis testing function
#
# 	Note:  all built-in tests (e.g. ttest2, anova1rm, etc.)
# 	represent specific cases of this glm function.
# 	'''
# 	from . glmc.designs import GLM
# 	from . glmc.models import GeneralLinearModel
# 	# from . glmc._la import rank
# 	# df0       = 1, X.shape[0] - rank(X)
# 	design    = GLM(X, c)
# 	model     = GeneralLinearModel(X, design.df0, QQ)
# 	fit       = model.fit( y )
# 	teststat  = fit.calculate_t_stat( c, roi=roi )
# 	return _assemble_spm_objects(design, model, fit, teststat, roi=roi)


def glm(y, X, c, QQ=None, roi=None):
	'''
	General Linear Model

	Most general user-facing hypothesis testing function. All built-in
	tests (e.g. ttest2, anova1rm, etc.) represent specific cases of
	this "glm" function.
	
	The contrasts "c" must be numpy arrays. If a contrast is a 1D array
	it will be handled as a "T" contrast. If it is 2D it will be handled
	as an "F" contrast.
	
	'''
	from . glmc.designs import GLM
	from . glmc.models import GeneralLinearModel
	design    = GLM(X, c)
	model     = GeneralLinearModel(X, design.df0, QQ)
	fit       = model.fit( y )
	teststat  = fit.calculate_t_stat( c, roi=roi )
	return _assemble_spm_objects(design, model, fit, teststat, roi=roi)
	
	
# from . glmc.ui import _glm_via_design as _glm_design


@appendargs
@checkargs
def regress(y, x, roi=None):
	from . glmc.designs import REGRESS
	spm    = _glm_design(y, REGRESS(x) , roi)
	spm.r  = spm.z / (  (spm.design.J - 2 + spm.z**2)**0.5)   # t = r * ((J-2)/(1-r*r) )**0.5
	return spm


@appendargs
@checkargs
def ttest(y, mu=0, roi=None):
	from . glmc.designs import TTEST
	return _glm_design(y-mu, TTEST( y.shape[0] ) , roi)


@appendargs
@checkargs
def ttest2(y0, y1, equal_var=False, roi=None):
	from . glmc.designs import TTEST2
	n0,n1     = y0.shape[0], y1.shape[0]
	y         = np.hstack( (y0,y1) ) if (y0.ndim==1) else np.vstack(  (y0, y1)  )
	return _glm_design(y, TTEST2(n0, n1) , equal_var, roi)


@checkargs
def ttest_paired(y0, y1, roi=None):
	return ttest(y0-y1, 0, roi=roi)



'''
Below is (commented) development code to more clearly
show processing flow for an example function (ttest2)
'''

# @appendargs
# @checkargs
# def ttest2(y0, y1, equal_var=False, roi=None):
# 	from . glmc.designs import TTEST2
# 	# from .. _cov import CovarianceModel
# 	n0,n1     = y0.shape[0], y1.shape[0]
# 	y         = np.hstack( (y0,y1) ) if (y0.ndim==1) else np.vstack(  (y0, y1)  )
# 	design    = TTEST2(n0, n1)
# 	QQ        = design.get_variance_model( equal_var=equal_var )
# 	# if equal_var:
# 	# 	QQ    = None
# 	# 	cmodel = CovarianceModel(design.X)
# 	# 	# cmodel.add_constant_var()
# 	# else:
# 	# 	cmodel = CovarianceModel(design.X)
# 	# 	cmodel.add_group_vars()
# 	# 	# model.add_autocorr()
# 	# 	QQ    = cmodel.get_model()
#
# 	model,fit,teststat = glm(y, design.X, design.contrasts[0].C, QQ=QQ)
# 	return _assemble_spm_objects(design, model, fit, teststat)
