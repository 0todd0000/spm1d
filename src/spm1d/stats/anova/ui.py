
# import scipy.stats

# from . _glm import OneWayANOVAModel, OneWayRMANOVAModel
from .. _dec import appendSPMargs



# def aov(y, X, C, Q, gg=False, _Xeff=None):
# 	model    = GeneralLinearModel()
# 	model.set_design_matrix( X )
# 	model.set_contrast_matrix( C )
# 	model.set_variance_model( Q )
# 	fit      = model.fit( y )
# 	fit.estimate_variance()
# 	fit.calculate_effective_df( _Xeff )
# 	fit.calculate_f_stat()
# 	if gg:
# 		fit.greenhouse_geisser()
# 	f,df     = fit.f, fit.df
# 	if fit.dvdim==1:
# 		p  = scipy.stats.f.sf(float(f), df[0], df[1])
# 	else:
# 		fwhm    = rft1d.geom.estimate_fwhm( fit.e )
# 		p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
# 	return f, df, p, model

# def aov(y, X, C, Q, gg=False, _Xeff=None):
# 	model    = GeneralLinearModel()
# 	model.set_design_matrix( X )
# 	# model.set_contrast_matrix( C )
# 	model.set_variance_model( Q )
# 	fit      = model.fit( y )
# 	fit.estimate_variance()
#
# 	SPM = []
# 	for c in C:
# 		model.set_contrast_matrix( c )
# 		fit.calculate_effective_df( _Xeff )
# 		fit.calculate_f_stat()
# 		if gg:
# 			fit.greenhouse_geisser()
#
# 		f,df     = fit.f, fit.df
# 		if fit.dvdim==1:
# 			from .. _spmcls import SPM0D
# 			spm = SPM0D('F', fit.f, fit.df, beta=None, residuals=None, sigma2=None, X=None)
#
# 			# p  = scipy.stats.f.sf(float(f), df[0], df[1])
# 		else:
# 			from .. _spmcls import SPM1D
# 			fwhm    = rft1d.geom.estimate_fwhm( fit.e )
# 			p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
#
# 		SPM.append(spm)
# 	if len(SPM)==1:
# 		SPM = SPM[0]
# 	else:
# 		from .. _spmcls import SPMFList
# 		SPM = SPMFList( SPM, nfactors=2 )
# 	return SPM
# 	# return f, df, p, model



# def aov(y, X, C, Q, gg=False, _Xeff=None):
# 	from . models import GeneralLinearModel
# 	model    = GeneralLinearModel()
# 	model.set_design_matrix( X )
# 	model.set_variance_model( Q )
# 	fit      = model.fit( y )
# 	fit.estimate_variance()
# 	f,df,ms,ss = [], [], [], []
# 	for c in C:
# 		model.set_contrast_matrix( c.C )
# 		fit.calculate_effective_df( _Xeff )
# 		fit.calculate_f_stat()
# 		if gg:
# 			fit.adjust_df_greenhouse_geisser()
# 		f.append( fit._f )
# 		df.append( fit._df )
# 		ms.append( fit._ms )
# 		ss.append( fit._ss )
# 	return f, df, fit
#

class GLMResults(object):
	def __init__(self, design, model, fit, stats):
		self.design  = design
		self.model   = model
		self.fit     = fit
		self.stats   = stats


# def aov(y, design, Q, gg=False, _Xeff=None):
# 	from . models import GeneralLinearModel
# 	model    = GeneralLinearModel()
# 	model.set_design_matrix( design.X )
# 	model.set_variance_model( Q )
# 	fit      = model.fit( y )
# 	stats    = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff )   for c in design.C]
# 	glmr     = GLMResults(design, model, fit, stats)
# 	return glmr
# 	# for c in C:
# 	# 	res  =
# 	#
# 	# 	model.set_contrast_matrix( c.C )
# 	# 	fit.calculate_effective_df( _Xeff )
# 	# 	fit.calculate_f_stat()
# 	# 	if gg:
# 	# 		fit.adjust_df_greenhouse_geisser()
# 	# 	f.append( fit._f )
# 	# 	df.append( fit._df )
# 	# 	ms.append( fit._ms )
# 	# 	ss.append( fit._ss )
# 	# return f, df, fit
#


def aov(y, X, C, Q, gg=False, _Xeff=None):
	from . models import GeneralLinearModel
	model     = GeneralLinearModel()
	model.set_design_matrix( X )
	model.set_variance_model( Q )
	fit      = model.fit( y )
	# stats    = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff )   for c in design.C]
	# model.fit( y )
	teststats = [fit.calculate_f_stat( c, gg=gg, _Xeff=_Xeff, ind=i )   for i,c in enumerate(C)]
	# glmr     = GLMResults(design, model, fit, stats)
	return model, fit, teststats
	# for c in C:
	# 	res  =
	#
	# 	model.set_contrast_matrix( c.C )
	# 	fit.calculate_effective_df( _Xeff )
	# 	fit.calculate_f_stat()
	# 	if gg:
	# 		fit.adjust_df_greenhouse_geisser()
	# 	f.append( fit._f )
	# 	df.append( fit._df )
	# 	ms.append( fit._ms )
	# 	ss.append( fit._ss )
	# return f, df, fit
	
	
	



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


# def _assemble_spm_objects(f, df, design, fit, testname=None):
# 	if fit.dvdim==1:
# 		from .. _spmcls import SPM0D as _SPM
# 	else:
# 		from .. _spmcls import SPM1D as _SPM
# 	# spm = [_SPM('F', ff, ddf, beta=None, residuals=None, sigma2=None, X=None)  for ff,ddf in zip(f,df)]
# 	spm = [_SPM('F', ff, ddf, design, fit, c)  for ff,ddf,c in zip(f,df,design.C)]
# 	if len(spm)==1:
# 		spm = spm[0]
# 	else:
# 		from .. _spmcls import SPMFList
# 		spm = SPMFList( spm )
# 	return spm

# def _assemble_spm_objects(f, df, design, fit):
# 	if fit.dvdim==1:
# 		from .. _spmcls import SPM0D as _SPM
# 	else:
# 		from .. _spmcls import SPM1D as _SPM
# 	# spm = [_SPM('F', ff, ddf, beta=None, residuals=None, sigma2=None, X=None)  for ff,ddf in zip(f,df)]
# 	spm = [_SPM('F', ff, ddf, design, fit, c)  for ff,ddf,c in zip(f,df,design.contrasts)]
# 	if len(spm)==1:
# 		spm = spm[0]
# 	else:
# 		from .. _spmcls import SPMFList
# 		spm = SPMFList( spm )
# 	return spm

# def _assemble_spm_objects(results, design, fit, roi=None):
# 	if fit.dvdim==0:
# 		from .. _spmcls import SPM0D
# 		spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 	else:
# 		from .. _spmcls import SPM1D
# 		spm = [SPM1D(r, design, fit, c, roi)  for r,c in zip(results, design.contrasts)]
# 	# spm = [_SPM('F', ff, ddf, beta=None, residuals=None, sigma2=None, X=None)  for ff,ddf in zip(f,df)]
# 	# spm = [_SPM('F', ff, ddf, design, fit, c)  for ff,ddf,c in zip(f,df,design.contrasts)]
# 	# spm = [_SPM('F', r.f, r.df, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 	# spm = [_SPM(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 	if len(spm)==1:
# 		spm = spm[0]
# 	else:
# 		from .. _spmcls import SPMFList
# 		spm = SPMFList( spm )
# 	return spm

# def _assemble_spm_objects(glmr, roi=None):
# 	if fit.dvdim==0:
# 		from .. _spmcls import SPM0D
# 		spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 	else:
# 		from .. _spmcls import SPM1D
# 		spm = [SPM1D(r, design, fit, c, roi)  for r,c in zip(results, design.contrasts)]
# 	# spm = [_SPM('F', ff, ddf, beta=None, residuals=None, sigma2=None, X=None)  for ff,ddf in zip(f,df)]
# 	# spm = [_SPM('F', ff, ddf, design, fit, c)  for ff,ddf,c in zip(f,df,design.contrasts)]
# 	# spm = [_SPM('F', r.f, r.df, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 	# spm = [_SPM(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 	if len(spm)==1:
# 		spm = spm[0]
# 	else:
# 		from .. _spmcls import SPMFList
# 		spm = SPMFList( spm )
# 	return spm


def _assemble_spm_objects(design, model, fit, teststats, roi=None):
	if fit.dvdim==0:
		from .. _spmcls import SPM0D
		spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
	else:
		from .. _spmcls import SPM1D
		# spm = [SPM1D(r, design, fit, c, roi)  for r,c in zip(results, design.contrasts)]
		# spm = [SPM1D(r, design, fit, c, roi)  for r,c in zip(results, design.contrasts)]
		spm = [SPM1D(design, model, fit, s, roi)  for s in teststats]
	# spm = [_SPM('F', ff, ddf, beta=None, residuals=None, sigma2=None, X=None)  for ff,ddf in zip(f,df)]
	# spm = [_SPM('F', ff, ddf, design, fit, c)  for ff,ddf,c in zip(f,df,design.contrasts)]
	# spm = [_SPM('F', r.f, r.df, design, fit, c)  for r,c in zip(results, design.contrasts)]
	# spm = [_SPM(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
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
	# C       = [c.C  for c in design.contrasts]

	# res,fit = aov(y, design.X, design.C, Q)
	#
	# # print(res)
	# # print(fit)
	#
	# # f,df,fit = aov(y, design.X, design.contrasts, Q)
	# # return res, design, fit
	# return _assemble_spm_objects(res, design, fit, roi)
	model,fit,teststats = aov(y, design.X, design.C, Q)
	# return glm,stats
	
	return _assemble_spm_objects(design, model, fit, teststats)

	# # # glmr = aov(y, design.X, design.C, Q)
	# # glmr = aov(y, design, Q)
	# #
	# # # glmr = aov(y, design, Q)
	# # # # print( glmr )
	# # # return glmr
	# # return _assemble_spm_objects(glmr, roi)
	#
	# # print(res)
	# # print(fit)
	#
	# # f,df,fit = aov(y, design.X, design.contrasts, Q)
	# # return res, design, fit
	# return _assemble_spm_objects(glmr, roi)




# def anova1(y, A, equal_var=False):
# 	from . designs import ANOVA1
# 	design   = ANOVA1( A )
# 	Q        = design.get_variance_model( equal_var=equal_var )
# 	model    = GeneralLinearModel()
# 	model.set_design_matrix( design.X )
# 	model.set_contrast_matrix( design.C )
# 	model.set_variance_model( Q )
# 	fit      = model.fit( y )
# 	fit.estimate_variance()
# 	fit.calculate_effective_df()
# 	fit.calculate_f_stat()
# 	f,df     = fit.f, fit.df
# 	if fit.dvdim==1:
# 		p  = scipy.stats.f.sf(float(f), df[0], df[1])
# 	else:
# 		fwhm    = rft1d.geom.estimate_fwhm( fit.e )
# 		p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
# 	return f, df, p, model


# def anova1rm(y, A, SUBJ, equal_var=False, gg=True):
# 	from . designs import ANOVA1RM
# 	design   = ANOVA1RM( A, SUBJ )
# 	Q        = design.get_variance_model( equal_var=equal_var )
# 	model    = GeneralLinearModel()
# 	model.set_design_matrix( design.X )
# 	model.set_contrast_matrix( design.C )
# 	model.set_variance_model( Q )
# 	fit      = model.fit( y )
# 	fit.estimate_variance()
# 	fit.calculate_effective_df(  design.X[:,:-1]  )   # "design.X[:,:-1]" is a hack;  there must be a different way
# 	fit.calculate_f_stat()
# 	if gg:
# 		fit.greenhouse_geisser()
# 	f,df   = fit.f, fit.df
# 	if fit.dvdim==1:
# 		p  = scipy.stats.f.sf(float(f), df[0], df[1])
# 	else:
# 		fwhm    = rft1d.geom.estimate_fwhm( fit.e )
# 		p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
# 	return f, df, p, model



# def anova1(y, A, equal_var=False):
# 	model  = OneWayANOVAModel(y, A)
# 	model.build_variance_model( equal_var=equal_var )
# 	model.fit()
# 	model.estimate_variance()
# 	model.calculate_effective_df()
# 	model.calculate_f_stat()
# 	f,df   = model.f, model.df
#
# 	if isinstance(f, float):
# 		p  = scipy.stats.f.sf(f, df[0], df[1])
# 	else:
# 		fwhm    = rft1d.geom.estimate_fwhm( model.e )
# 		p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
#
# 	return f, df, p, model



# def anova1rm(y, A, SUBJ, equal_var=False, gg=True):
# 	model  = OneWayRMANOVAModel(y, A, SUBJ)
# 	model.build_variance_model( equal_var=equal_var )
# 	model.fit()
# 	model.estimate_variance(  )
# 	model.calculate_effective_df()
# 	model.calculate_f_stat()
# 	if gg:
# 		model.greenhouse_geisser()
#
# 	f,df,V   = model.f, model.df, model.V
#
# 	if isinstance(f, float):
# 		p  = scipy.stats.f.sf(f, df[0], df[1])
# 	else:
# 		fwhm    = rft1d.geom.estimate_fwhm( model.e )
# 		p       = rft1d.f.sf(f.max(), df, y.shape[1], fwhm)
# 	return f, df, p, model