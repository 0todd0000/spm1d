'''
One- and two sample tests (using T contrasts).
'''

# Copyright (C) 2023  Todd Pataky



import numpy as np
from . _dec import appendargs, checkargs




# def _assemble_spm_objects(design, model, fit, teststats, roi=None):
# 	if fit.dvdim==0:
# 		from . _spmcls import SPM0D
# 		# spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 		spm = [SPM0D(design, model, fit, s)  for s in teststats]
# 	else:
# 		from . _spmcls import SPM1D
# 		spm = [SPM1D(design, model, fit, s, roi)  for s in teststats]
# 	if len(spm)==1:
# 		spm = spm[0]
# 	else:
# 		from . _spmcls import SPMFList
# 		spm = SPMFList( spm )
# 	return spm

# def _glm_design(y, design, equal_var=False, roi=None):
# 	'''
# 	Design object-based interface to glm
#
# 	This is an internal function that is NOT meant for users.
# 	'''
# 	QQ         = design.get_variance_model( equal_var=equal_var )
# 	# ctype      = 'T' if design.testname in ['ttest', 'ttest_paired', 'ttest2', 'regress'] else 'F'
# 	spm        = glm(y, design.X, design.C, QQ=QQ, roi=roi)
# 	spm.design = design
# 	return spm


# def glm(y, X, C, ctype='T', QQ=None, roi=None, gg=False, _Xeff=None):
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
# 	design    = GLM(X, C)
# 	model     = GeneralLinearModel(X, design.df0, QQ)
# 	fit       = model.fit( y )
# 	# teststat  = fit.calculate_t_stat( c, roi=roi )
# 	teststats = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff, ind=i )   for i,c in enumerate(C)]
# 	return _assemble_spm_objects(design, model, fit, teststats, roi=roi)

# def glm(y, X, C, QQ=None, roi=None, gg=False, _Xeff=None):
# 	'''
# 	General Linear Model
#
# 	Most general user-facing hypothesis testing function. All built-in
# 	tests (e.g. ttest2, anova1rm, etc.) represent specific cases of
# 	this "glm" function.
#
# 	The contrasts "c" must be numpy arrays. If a contrast is a 1D array
# 	it will be handled as a "T" contrast. If it is 2D it will be handled
# 	as an "F" contrast.
#
# 	'''
# 	from . glmc.designs import GLM
# 	from . glmc.models import GeneralLinearModel
# 	design    = GLM(X, C)
# 	model     = GeneralLinearModel(X, design.df0, QQ)
# 	fit       = model.fit( y )
# 	# teststat  = fit.calculate_t_stat( c, roi=roi )
# 	# return _assemble_spm_objects(design, model, fit, teststat, roi=roi)
# 	teststats = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff, ind=i )   for i,c in enumerate(C)]
# 	return _assemble_spm_objects(design, model, fit, teststats, roi=roi)

# def aov(y, X, C, QQ, df0=None, gg=False, _Xeff=None):
# 	from . glmc.models import GeneralLinearModel
# 	# df0       = 1, X.shape[0] - rank(X)
# 	model     = GeneralLinearModel(X, df0, QQ)
# 	fit       = model.fit( y )
# 	teststats = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff, ind=i )   for i,c in enumerate(C)]
# 	return model, fit, teststats
#
#
#
#
# def anova1old(y, A, equal_var=False):
# 	# if not equal_var:
# 	# 	raise NotImplementedError('variance components not yet tested for anova1')
#
# 	from . glmc.designs import ANOVA1
# 	design   = ANOVA1( A )
# 	QQ       = design.get_variance_model( equal_var=equal_var )
# 	# if equal_var:
# 	# 	import numpy as np
# 	# 	QQ   = None
# 	# 	QQ   = [np.eye(A.size)]
# 	# else:
# 	# 	QQ   = design.get_variance_model( equal_var=equal_var )
#
#
#
# 	model,fit,teststats = aov(y, design.X, design.C, QQ, df0=design.df0)
#
# 	return _assemble_spm_objects(design, model, fit, teststats)


@appendargs
def anova1(y, A, equal_var=False, roi=None):
	from . glmc.designs import ANOVA1
	from . glmc.ui import _glm_via_design
	# design   = ANOVA1( A )
	return _glm_via_design( y , ANOVA1( A ) , equal_var, roi )
	# QQ       = design.get_variance_model( equal_var=equal_var )
	# if equal_var:
	# 	import numpy as np
	# 	QQ   = None
	# 	QQ   = [np.eye(A.size)]
	# else:
	# 	QQ   = design.get_variance_model( equal_var=equal_var )
	
	
	
	# model,fit,teststats = aov(y, design.X, design.C, QQ, df0=design.df0)
	#
	# return _assemble_spm_objects(design, model, fit, teststats)


@appendargs
def anova1rm(y, A, SUBJ, equal_var=False, gg=True, roi=None):
	from . glmc.designs import ANOVA1RM
	from . glmc.ui import _glm_via_design
	# design   = ANOVA1RM( A, SUBJ )
	# QQ       = design.get_variance_model( equal_var=equal_var )
	return _glm_via_design( y , ANOVA1RM( A, SUBJ ) , equal_var, roi )
	
	# model,fit,teststats = aov(y, design.X, design.C, QQ, df0=design.df0, gg=False, _Xeff= design.X[:,:-1] )  # "design.X[:,:-1]" is a hack;  there must be a different way
	#
	# return _assemble_spm_objects(design, model, fit, teststats)
	
	# model    = GeneralLinearModel()
	# model.set_design_matrix( design.X )
	# model.set_contrast_matrix( design.C )
	# model.set_variance_model( Q )
	# fit      = model.fit( y )
	# fit.estimate_variance()
	# fit.calculate_effective_df(  design.X[:,:-1]  )   # "design.X[:,:-1]" is a hack;  there must be a different way
	# fit.calculate_f_stat()
	# if gg:
	# 	fit.greenhouse_geisser()
	# f,df   = fit.f, fit.df
	# if fit.dvdim==1:
	# 	p  = scipy.stats.f.sf(float(f), df[0], df[1])
	# else:
	# 	fwhm    = rft1d.geom.estimate_fwhm( fit.e )
	# 	p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
	# return f, df, p, model


# def anova1rm(y, A, SUBJ, equal_var=False, gg=True):
#
# 	# if not equal_var:
# 	# 	raise NotImplementedError('variance components not yet tested for anova1rm')
#
# 	from . glmc.designs import ANOVA1RM
# 	design   = ANOVA1RM( A, SUBJ )
# 	QQ   = design.get_variance_model( equal_var=equal_var )
# 	# if equal_var:
# 	# 	import numpy as np
# 	# 	QQ   = None
# 	# 	QQ   = [np.eye(A.size)]
# 	# else:
# 	# Q        = design.get_variance_model( equal_var=equal_var )
#
# 	model,fit,teststats = aov(y, design.X, design.C, QQ, df0=design.df0, gg=False, _Xeff= design.X[:,:-1] )  # "design.X[:,:-1]" is a hack;  there must be a different way
#
# 	return _assemble_spm_objects(design, model, fit, teststats)
#
# 	# model    = GeneralLinearModel()
# 	# model.set_design_matrix( design.X )
# 	# model.set_contrast_matrix( design.C )
# 	# model.set_variance_model( Q )
# 	# fit      = model.fit( y )
# 	# fit.estimate_variance()
# 	# fit.calculate_effective_df(  design.X[:,:-1]  )   # "design.X[:,:-1]" is a hack;  there must be a different way
# 	# fit.calculate_f_stat()
# 	# if gg:
# 	# 	fit.greenhouse_geisser()
# 	# f,df   = fit.f, fit.df
# 	# if fit.dvdim==1:
# 	# 	p  = scipy.stats.f.sf(float(f), df[0], df[1])
# 	# else:
# 	# 	fwhm    = rft1d.geom.estimate_fwhm( fit.e )
# 	# 	p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
# 	# return f, df, p, model



@appendargs
def anova2(y, A, B, equal_var=False, gg=True, roi=None):
	from . glmc.designs import ANOVA2
	from . glmc.ui import _glm_via_design
	# design   = ANOVA1RM( A, SUBJ )
	# QQ       = design.get_variance_model( equal_var=equal_var )
	return _glm_via_design( y , ANOVA2( A, B ) , equal_var, roi )



@appendargs
def anova2rm(y, A, B, S, equal_var=False, gg=True, roi=None):
	from . glmc.designs import ANOVA2RM
	from . glmc.ui import _glm_via_design
	# design   = ANOVA1RM( A, SUBJ )
	# QQ       = design.get_variance_model( equal_var=equal_var )
	return _glm_via_design( y , ANOVA2RM( A, B, S ) , equal_var, roi )

# # @appendSPMargs
# def anova2(y, A, B, equal_var=False, roi=None):
# 	if not equal_var:
# 		raise NotImplementedError('variance components not yet implemented for anova2')
# 	from . glmc.designs import ANOVA2
# 	design   = ANOVA2( A, B )
# 	# QQ       = design.get_variance_model( equal_var=equal_var )
#
# 	# # temporary variance components:
# 	# import numpy as np
# 	# J       = A.size
# 	# QQ      = [np.eye(J)]
# 	QQ      = None
#
# 	model,fit,teststats = aov(y, design.X, design.C, QQ, df0=design.df0)
#
# 	return _assemble_spm_objects(design, model, fit, teststats)