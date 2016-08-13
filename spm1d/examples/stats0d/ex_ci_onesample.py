
import numpy as np
from matplotlib import pyplot
import spm1d
from spm1d.stats import ttest
from spm1d.stats._spm import df2str, dflist2str



# class _CI(object):
# 	@staticmethod
# 	def _check_mu(mu):
# 		self.check_mu(mu, dim=0)
# 		if (mu is not None) and not (isinstance(mu, (int,float))):
# 			raise ValueError('mu be')
	


class CI0DOneSample(object):
	kind                  = 'One sample'
	datum                 = 'mean'
	criterion             = 'mu'
	dim                   = 0
	
	def __init__(self, spmi, mean, hstar, mu=None):
		### main parameters:
		self.mean         = float(mean)
		self.mu           = mu
		### probability:
		self.alpha        = spmi.alpha
		self.df           = spmi.df
		self.zstar        = spmi.zstar
		### confidence interval:
		self.hstar        = hstar
		self.ci           = mean - hstar, mean + hstar
		self.h0reject     = spmi.h0reject

	def _check_args(mu):
		self.check_mu(mu)



	def __repr__(self):
		s        = ''
		s       += '0D Confidence Interval (%d%s)\n'    %(100*(1-self.alpha), '%')
		s       += '   kind       :  %s\n'              %self.kind
		s       += '   datum      :  %s  (%.5f)\n'      %(self.datum, self.mean)
		if self.mu is not None:
			s   += '   criterion  :  %s  (%.5f)\n'      %(self.criterion, self.mu)
		s       += '   Probability\n'
		s       += '      alpha      :  %.3f\n'         %self.alpha
		s       += '      df         :  %s\n'           %dflist2str(self.df)
		s       += '      zstar      :  %.5f\n'         %self.zstar
		s       += '   Confidence interval\n'
		s       += '      hstar      :  %.5f\n'         %self.hstar
		s       += '      ci         :  (%.5f, %.5f)\n' %self.ci
		if self.mu is not None:
			s   += '      h0reject   :  %s\n'           %self.h0reject
		return s

		



def ci_onesample(y, alpha=0.05, mu=None):
	spmi    = ttest(y, mu).inference(alpha, two_tailed=True)
	mean    = spmi.beta.flatten()  #sample mean
	mean    = mean if (mu is None) else (mean + mu)
	s       = spmi.sigma2**0.5     #sample standard deviation
	hstar   = spmi.zstar * s / y.shape[0]**0.5
	CIclass = ConfidenceInterval if spmi.dim==1 else CI0DOneSample
	return CIclass(spmi, mean, hstar, mu=mu)




#(0) Load dataset:
dataset = spm1d.data.uv0d.ci1.MinnesotaGeyerRate()
dataset = spm1d.data.uv0d.ci1.WebsterSleep()
y,mu    = dataset.get_data()
print dataset


#(1) Compute confidence interval:
alpha      = 0.05
# ci         = spm1d.stats.ci_onesample(y, alpha, mu=None)
ci         = ci_onesample(y, alpha, mu=None)
print( ci )

ci         = ci_onesample(y, alpha, mu=10)
print( ci )







