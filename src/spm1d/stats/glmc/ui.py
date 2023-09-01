


# def _assemble_spm_objects_t(design, model, fit, teststat, roi=None):
# 	if fit.dvdim==0:
# 		from . _spmcls import SPM0D
# 		spm = SPM0D(design, model, fit, teststat)
# 	else:
# 		from . _spmcls import SPM1D
# 		spm = SPM1D(design, model, fit, teststat)
# 	return spm


def _assemble_spm_objects(design, model, fit, teststats, roi=None):
	if fit.dvdim==0:
		from .. _spmcls import SPM0D
		# spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
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

def _glm_via_design(y, design, equal_var=False, roi=None):
	'''
	Design object-based interface to glm
	
	This is an internal function that is NOT meant for users.
	'''
	QQ         = design.get_variance_model( equal_var=equal_var )
	ctype      = 'T' if design.testname in ['ttest', 'ttest_paired', 'ttest2', 'regress'] else 'F'
	spm        = glm(y, design.X, design.C, ctype=ctype, QQ=QQ, roi=roi)
	spm.design = design
	return spm


def glm(y, X, C, ctype='T', QQ=None, roi=None, gg=False, _Xeff=None):
	'''
	General Linear Model

	Most general user-facing hypothesis testing function

	Note:  all built-in tests (e.g. ttest2, anova1rm, etc.)
	represent specific cases of this glm function.
	'''
	from . designs import GLM
	from . models import GeneralLinearModel
	# from . glmc._la import rank
	# df0       = 1, X.shape[0] - rank(X)
	design    = GLM(X, C)
	model     = GeneralLinearModel(X, design.df0, QQ)
	fit       = model.fit( y )
	if ctype == 'T':
		teststat  = fit.calculate_t_stat( c, roi=roi )
	else:
		teststat = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff, ind=i )   for i,c in enumerate(C)]
	return _assemble_spm_objects(design, model, fit, teststat, roi=roi)



