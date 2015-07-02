

import numpy as np
from .. import _base




class FitnessClub(_base.DatasetCCA):
	'''
	NOTE:  This analysis is not yet implemented in spm1d!!!!
	Both independent and dependent variables are three-component vectors.
	This requires use of Wilks' Lambda, Roy's Greatest Root or another test statistic.
	'''
	def _set_values(self):
		self.www  = 'http://support.sas.com/documentation/cdl/en/statug/63033/HTML/default/viewer.htm#statug_cancorr_sect020.htm'
		A = np.array([
		   [191,  36,  50,   5,  162,   60],
		   [189,  37,  52,   2,  110,   60],
		   [193,  38,  58,  12,  101,  101],
		   [162,  35,  62,  12,  105,   37],
		   [189,  35,  46,  13,  155,   58],
		   [182,  36,  56,   4,  101,   42],
		   [211,  38,  56,   8,  101,   38],
		   [167,  34,  60,   6,  125,   40],
		   [176,  31,  74,  15,  200,   40],
		   [154,  33,  56,  17,  251,  250],
		   [169,  34,  50,  17,  120,   38],
		   [166,  33,  52,  13,  210,  115],
		   [154,  34,  64,  14,  215,  105],
		   [247,  46,  50,   1,   50,   50],
		   [193,  36,  46,   6,   70,   31],
		   [202,  37,  62,  12,  210,  120],
		   [176,  37,  54,   4,   60,   25],
		   [157,  32,  52,  11,  230,   80],
		   [156,  33,  54,  15,  225,   73],
		   [138,  33,  68,   2,  110,   43]
		])
		self.x    = A[:,0]   #only use the first independent variable
		self.Y    = A[:,3:]
		self.z    = 5.1458   #computed using MATLAB's canoncorr
		self.df   = (1, 3)
		self.p    = 0.1614   #computed using MATLAB's canoncorr



class StackExchange(_base.DatasetCCA):
	'''
	NOTE:  This analysis is not yet implemented in spm1d!!!!
	Both independent and dependent variables are three-component vectors.
	This requires use of Wilks' Lambda, Roy's Greatest Root or another test statistic.
	'''
	def _set_values(self):
		self.www  = 'http://stats.stackexchange.com/questions/117489/how-can-i-run-an-analysis-of-variance-with-one-independent-variable-and-multiple'
		A = np.array([
			[4.19, 5.51, 19.76, 50.00, 19.36, 54.07],
			[8.60, 10.16, 33.01, 82.99, 38.48, 44.95],
			[8.03, 7.82, 31.29, 79.05, 40.12, 59.18],
			[6.64, 8.99, 27.13, 69.13, 30.44, 59.02],
			[7.03, 8.22, 25.29, 74.45, 36.02, 50.88],
			[1.50, 5.90, 10.69, 22.88, 10.34, 34.50],
			[4.36, 7.61, 19.27, 44.47, 20.06, 24.62],
			[7.17, 8.30, 26.72, 68.68, 31.61, 20.16],
			[2.68, 5.61, 14.25, 37.07, 15.20, 67.75],
			[7.91, 7.75, 30.93, 82.01, 38.62, 65.36],
			[3.74, 5.24, 16.42, 40.17, 17.54, 15.19]
		])
		self.x    = A[:,0]
		self.Y    = A[:,1:]
		self.z    = 47.1219     #computed using MATLAB's canoncorr
		self.df   = (1, 5)
		self.p    = 5.3655e-09  #computed using MATLAB's canoncorr




