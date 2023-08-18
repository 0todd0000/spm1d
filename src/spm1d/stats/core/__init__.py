

# import numpy as np
# from .. _spmcls import SPM0D
# from . designs import TTEST
# from . factors import Factor
# from . contrasts import Contrast
# from . models import GeneralLinearModel
# from .. _la import rank
# from ... util import array2shortstr, dflist2str, df2str, DisplayParams
# # eps = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors
#
#
#
#
#
#
#
#
#
#
# def glm_t(y, X, c, QQ=None):
# 	model     = GeneralLinearModel()
# 	model.set_design_matrix( X )
# 	# model.set_variance_model( QQ )
# 	fit       = model.fit( y )
# 	# t         = fit.calculate_t_stat( c, gg=gg, _Xeff=_Xeff, ind=i )
# 	teststat  = fit.calculate_t_stat( c )
# 	# teststats = [   for i,c in enumerate(C)]
# 	return model, fit, teststat
# 	# print(t)
#
#
#
#
# def _assemble_spm_objects(design, model, fit, teststat, roi=None):
# 	if fit.dvdim==0:
# 		# from .. _spmcls import SPM0D
# 		from spm1d.stats._spmcls import SPM0D
# 		# spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
# 		spm = SPM0D(design, model, fit, teststat)
# 	else:
# 		# from .. _spmcls import SPM1D
# 		from spm1d.stats._spmcls import SPM1D
# 		spm = SPM1D(design, model, fit, teststat)
# 		# spm = [SPM1D(design, model, fit, s, roi)  for s in teststats]
# 	# if len(spm)==1:
# 	# 	spm = spm[0]
# 	# else:
# 	# 	from .. _spmcls import SPMFList
# 	# 	spm = SPMFList( spm )
# 	return spm
#
#
#
#
# def ttest(y, mu=0, roi=None):
# 	design    = TTEST(y, mu)
# 	model,fit,teststat = glm_t(y, design.X, design.contrasts[0].C)
# 	return _assemble_spm_objects(design, model, fit, teststat)
# 	# return model,fit,teststat
#
#