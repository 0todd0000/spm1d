
import numpy as np
from .. import _base




class RSFlavor(_base.DatasetT2):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/students-t-distribution/two-sample-t-test-equal-variances/'
		self.YA   = np.array([34,52,17,45,5,29,31,6,52,64])
		self.YB   = np.array([12,8,6,16,12,14,10,18,4,11])
		self.Y    = np.hstack([self.YA, self.YB])
		self.A    = np.array([0]*15 + [1]*15)
		self.z    = 3.454842
		self.df   = 1,9.83928
		self.p    = 0.003162



class ColumbiaPlacebo(_base.DatasetT2):
	def _set_values(self):
		self.www  = 'http://www.stat.columbia.edu/~martin/W2024/R2.pdf'
		self.YA   = np.array([101, 110, 103, 93, 99, 104])
		self.YB   = np.array([91, 87, 99, 77, 88, 91])
		self.Y    = np.hstack([self.YA, self.YB])
		self.A    = np.array([0]*15 + [1]*15)
		self.z    = 3.4456
		self.df   = 1,9.48
		self.p    = 0.003391












