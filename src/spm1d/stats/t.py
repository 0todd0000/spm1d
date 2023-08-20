'''
One- and two sample tests.
'''

# Copyright (C) 2023  Todd Pataky



# import numpy as np
# from .. _spmcls import SPM0D

# from . factors import Factor
# from . contrasts import Contrast

# from .. _la import rank
# from ... util import array2shortstr, dflist2str, df2str, DisplayParams
# eps = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors



import numpy as np
# from . _datachecks import checkargs
from . _dec import appendargs, checkargs






def _assemble_spm_objects(design, model, fit, teststat, roi=None):
	if fit.dvdim==0:
		# from .. _spmcls import SPM0D
		from spm1d.stats._spmcls import SPM0D
		# spm = [SPM0D(r, design, fit, c)  for r,c in zip(results, design.contrasts)]
		spm = SPM0D(design, model, fit, teststat)
	else:
		# from .. _spmcls import SPM1D
		from spm1d.stats._spmcls import SPM1D
		spm = SPM1D(design, model, fit, teststat)
		# spm = [SPM1D(design, model, fit, s, roi)  for s in teststats]
	# if len(spm)==1:
	# 	spm = spm[0]
	# else:
	# 	from .. _spmcls import SPMFList
	# 	spm = SPMFList( spm )
	return spm
	



def glm(y, X, c, QQ=None):
	from . core.models import GeneralLinearModel
	model     = GeneralLinearModel()
	model.set_design_matrix( X )
	# model.set_variance_model( QQ )
	fit       = model.fit( y )
	teststat  = fit.calculate_t_stat( c )
	return model, fit, teststat




@appendargs
@checkargs
def regress(y, x, roi=None):
	from . core.designs import REGRESS
	design = REGRESS(x)
	model,fit,teststat = glm(y, design.X, design.contrasts[0].C)
	spm    = _assemble_spm_objects(design, model, fit, teststat)
	spm.r  = spm.z / (  (spm.design.J - 2 + spm.z**2)**0.5)   # t = r * ((J-2)/(1-r*r) )**0.5
	return spm
	
	# spm.r          = spm.z / (  (J - 2 + spm.z**2)**0.5)   # t = r * ((J-2)/(1-r*r) )**0.5
	
	
	# # _datachecks.check('regress', Y, x)
	# J              = y.shape[0]
	# X              = np.ones((J,2))
	# X[:,0]         = x
	# c              = (1,0)
	# spm            = glm(y, X, c)
	# spm.r          = spm.z / (  (J - 2 + spm.z**2)**0.5)   # t = r * ((J-2)/(1-r*r) )**0.5
	# return spm



@appendargs
@checkargs
def ttest(y, mu=0, roi=None):
	# _datachecks.check('ttest', y, mu)
	from . core.designs import TTEST
	design    = TTEST(y, mu)
	model,fit,teststat = glm(y, design.X, design.contrasts[0].C)
	return _assemble_spm_objects(design, model, fit, teststat)
	# return model,fit,teststat
	
	

@appendargs
@checkargs
def ttest2(y0, y1, roi=None):
	from . core.designs import TTEST2
	n0,n1     = y0.shape[0], y1.shape[0]
	y         = np.hstack( (y0,y1) ) if (y0.ndim==1) else np.vstack(  (y0, y1)  )
	design    = TTEST2(n0, n1)
	model,fit,teststat = glm(y, design.X, design.contrasts[0].C)
	return _assemble_spm_objects(design, model, fit, teststat)
	# return model,fit,teststat


@checkargs
def ttest_paired(y0, y1, roi=None):
	return ttest(y0-y1, 0, roi=roi)



