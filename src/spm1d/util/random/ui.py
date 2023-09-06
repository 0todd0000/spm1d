
'''
Random data returned in format required for spm1d.stats functions 
'''


# def _generic(fname, *args, **kwargs):
# 	exec( f'from . c import {fname} as c_{fname}')
# 	y,args_ = eval(  f'c_{fname}(*args, **kwargs)')
# 	return y,args_
#
#
#
# def ttest(J, s, Q=None, fwhm=None):
# 	y,_  = _generic('ttest', J, s, Q=Q, fwhm=fwhm)
# 	return y,0








def anova1(JJ, ss, Q=None, fwhm=None):
	from . c import anova1 as c_anova1
	y,(A,) = c_anova1(JJ, ss, Q, fwhm)
	return y,A

def regress(J, s, Q=None, fwhm=None):
	from . c import regress as c_ttest
	y,(x,) = c_ttest(J, s, Q, fwhm)
	return y,x

def ttest(J, s, Q=None, fwhm=None):
	from . c import ttest as c_ttest
	y,_ = c_ttest(J, s, Q, fwhm)
	return y,0

def ttest_paired(J, ss, Q=None, fwhm=None):
	from . c import ttest_paired as c_ttestp
	y,(A,) = c_ttestp(J, ss, Q, fwhm)
	y0,y1  = y[A==0], y[A==1]
	return y0,y1

def ttest2(JJ, ss, Q=None, fwhm=None):
	from . c import ttest2 as c_ttest2
	y,(A,) = c_ttest2(JJ, ss, Q, fwhm)
	y0,y1  = y[A==0], y[A==1]
	return y0,y1

