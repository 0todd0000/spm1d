
from .. _dec import appendargs



# class GLMResults(object):
# 	def __init__(self, design, model, fit, stats):
# 		self.design  = design
# 		self.model   = model
# 		self.fit     = fit
# 		self.stats   = stats


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


def aov(y, X, C, Q, gg=False, _Xeff=None):
	from . models import GeneralLinearModel
	model     = GeneralLinearModel()
	model.set_design_matrix( X )
	model.set_variance_model( Q )
	fit       = model.fit( y )
	teststats = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff, ind=i )   for i,c in enumerate(C)]
	# glmr     = GLMResults(design, model, fit, stats)
	return model, fit, teststats




def anova1(y, A, equal_var=False):
	# if not equal_var:
	# 	raise NotImplementedError('variance components not yet tested for anova1')
	
	from . designs import ANOVA1
	design   = ANOVA1( A )
	QQ       = design.get_variance_model( equal_var=equal_var )
	# if equal_var:
	# 	import numpy as np
	# 	QQ   = None
	# 	QQ   = [np.eye(A.size)]
	# else:
	# 	QQ   = design.get_variance_model( equal_var=equal_var )
	
	
	
	model,fit,teststats = aov(y, design.X, design.C, QQ)
	
	return _assemble_spm_objects(design, model, fit, teststats)
	
	
	# return aov(y, design.X, design.C, Q)
	
	
def anova1rm(y, A, SUBJ, equal_var=False, gg=True):
	
	# if not equal_var:
	# 	raise NotImplementedError('variance components not yet tested for anova1rm')
	
	from . designs import ANOVA1RM
	design   = ANOVA1RM( A, SUBJ )
	QQ   = design.get_variance_model( equal_var=equal_var )
	# if equal_var:
	# 	import numpy as np
	# 	QQ   = None
	# 	QQ   = [np.eye(A.size)]
	# else:
	# Q        = design.get_variance_model( equal_var=equal_var )
	
	model,fit,teststats = aov(y, design.X, design.C, QQ, gg=False, _Xeff= design.X[:,:-1] )  # "design.X[:,:-1]" is a hack;  there must be a different way
	
	return _assemble_spm_objects(design, model, fit, teststats)
	
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






# @appendSPMargs
def anova2(y, A, B, equal_var=False, roi=None):
	if not equal_var:
		raise NotImplementedError('variance components not yet implemented for anova2')
	from . designs import ANOVA2
	design   = ANOVA2( A, B )
	# QQ       = design.get_variance_model( equal_var=equal_var )
	
	# temporary variance components:
	import numpy as np
	J       = A.size
	QQ      = [np.eye(J)]

	model,fit,teststats = aov(y, design.X, design.C, QQ)
	
	return _assemble_spm_objects(design, model, fit, teststats)
