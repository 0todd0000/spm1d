
import numpy as np
from .. import _base




class RSWeightClinic(_base.DatasetTpaired):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/students-t-distribution/paired-sample-t-test/'
		self.YA   = np.array([210,205,193,182,259,239,164,197,222,211,187,175,186,243,246])
		self.YB   = np.array([197,195,191,174,236,226,157,196,201,196,181,164,181,229,231])
		# self.Y    = np.hstack([self.YA, self.YB])
		# self.A    = np.array([0]*15 + [1]*15)
		self.two_tailed = True
		self.z    = 6.6896995
		self.df   = 1,14
		self.p    = 1.028e-5



class ColumbiaMileage(_base.DatasetTpaired):
	def _set_values(self):
		self.www  = 'http://www.stat.columbia.edu/~martin/W2024/R2.pdf'
		self.YA   = np.array([19, 22, 24, 24, 25, 25, 26, 26, 28, 32])
		self.YB   = np.array([16, 20, 21, 22, 23, 22, 27, 25, 27, 28])
		# self.Y    = np.hstack([self.YA, self.YB])
		# self.A    = np.array([0]*15 + [1]*15)
		self.two_tailed = False
		self.z    = 4.4721
		self.df   = 1,9
		self.p    = 0.000775












