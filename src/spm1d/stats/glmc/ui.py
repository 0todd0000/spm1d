


def _assemble_spm_objects(design, model, fit, teststats, roi=None):
	if fit.dvdim==0:
		from .. _spmcls import SPM0D
		spm = [SPM0D(design, model, fit, s)  for s in teststats]
	else:
		from .. _spmcls import SPM1D
		spm = [SPM1D(design, model, fit, s, roi)  for s in teststats]
	if len(spm)==1:
		spm = spm[0]
	else:
		from .. _spmcls import SPMFList
		spm = SPMFList( spm )
	return spm

def _glm_via_design(y, design, equal_var=False, roi=None, gg=False, _Xeff=None):
	'''
	Design object-based interface to glm
	
	This is an internal function that is NOT meant for users.
	'''
	from . models import GeneralLinearModel
	if isinstance(equal_var, bool):
		QQ    = design.get_variance_model( equal_var=equal_var )
	else:
		QQ    = equal_var
	model     = GeneralLinearModel(design.X, design.df0, QQ)
	fit       = model.fit( y )
	C         = design.get_contrast_matrices()
	teststats = fit.calculate_teststats(C, gg=gg, _Xeff=_Xeff, roi=roi)
	return _assemble_spm_objects(design, model, fit, teststats, roi=roi)


def glm(y, X, C, QQ=None, roi=None, gg=False, _Xeff=None):
	'''
	General Linear Model

	Most general user-facing hypothesis testing function. All built-in
	tests (e.g. ttest2, anova1rm, etc.) represent specific cases of
	this "glm" function.
	
	The contrasts "c" must be numpy arrays. If a contrast is a 1D array
	it will be handled as a "T" contrast. If it is 2D it will be handled
	as an "F" contrast.
	
	'''
	from . designs import GLM
	design = GLM(X, C)
	return _glm_via_design(y, design, QQ, roi, gg=False, _Xeff=None)
	
	


# def _glm_via_design(y, design, equal_var=False, roi=None):
# 	'''
# 	Design object-based interface to glm
#
# 	This is an internal function that is NOT meant for users.
# 	'''
# 	QQ         = design.get_variance_model( equal_var=equal_var )
# 	# ctype      = 'T' if design.testname in ['ttest', 'ttest_paired', 'ttest2', 'regress'] else 'F'
# 	# if design.contrast_type == 'T'
# 	spm        = glm(y, design.X, design.C, QQ=QQ, roi=roi)
# 	spm.design = design
# 	return spm
#
#
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
# 	from . designs import GLM
# 	from . models import GeneralLinearModel
# 	design    = GLM(X, C)
# 	model     = GeneralLinearModel(X, design.df0, QQ)
# 	fit       = model.fit( y )
# 	teststats = fit.calculate_teststats(C, gg=gg, _Xeff=_Xeff, roi=roi)
# 	return _assemble_spm_objects(design, model, fit, teststats, roi=roi)
