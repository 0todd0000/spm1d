
from .. _dec import appendSPMargs



# class GLMResults(object):
# 	def __init__(self, design, model, fit, stats):
# 		self.design  = design
# 		self.model   = model
# 		self.fit     = fit
# 		self.stats   = stats



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
	from . designs import ANOVA1
	design   = ANOVA1( A )
	Q        = design.get_variance_model( equal_var=equal_var )
	return aov(y, design.X, design.C, Q)
	
	
def anova1rm(y, A, SUBJ, equal_var=False, gg=True):
	from . designs import ANOVA1RM
	design   = ANOVA1RM( A, SUBJ )
	Q        = design.get_variance_model( equal_var=equal_var )
	return aov(y, design.X, design.C, Q, gg=True, _Xeff= design.X[:,:-1] )  # "design.X[:,:-1]" is a hack;  there must be a different way
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




def _assemble_spm_objects(design, model, fit, teststats, roi=None):
	if fit.dvdim==0:
		from .. _spmcls import SPM0D
		spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
	else:
		from .. _spmcls import SPM1D
		spm = [SPM1D(design, model, fit, s, roi)  for s in teststats]
	if len(spm)==1:
		spm = spm[0]
	else:
		from .. _spmcls import SPMFList
		spm = SPMFList( spm )
	return spm


# @appendSPMargs
def anova2(y, A, B, equal_var=False, roi=None):
	if not equal_var:
		raise NotImplementedError('variance components not yet implemented for anova2')
	from . designs import ANOVA2
	design   = ANOVA2( A, B )
	# Q        = design.get_variance_model( equal_var=equal_var )
	
	# temporary variance components:
	import numpy as np
	J       = A.size
	Q       = [np.eye(J)]

	model,fit,teststats = aov(y, design.X, design.C, Q)
	
	return _assemble_spm_objects(design, model, fit, teststats)
