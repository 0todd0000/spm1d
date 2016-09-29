
import numpy as np
from .. import _base




class KendallRandomNumbers(_base.DatasetNormality):
	def _set_values(self):
		self.www  = 'http://www.statext.com/practice/NormalityTest04.php'
		self.Y    = np.array([303, 338, 406, 457, 461, 469, 474, 489, 515, 583])
		self.z    = 0.66
		self.df   = 1,2
		self.p    = 0.7195
		self.note = 'Note     ', 'Original data are from p.194 of:  Kendall M (1948) Rank Correlation Methods, Charles Griffin & Company Ltd.'


class RFaithful(_base.DatasetNormalitySW):
	def _set_values(self):
		self.www  = 'http://cran.us.r-project.org/doc/manuals/R-intro.html#Examining-the-distribution-of-a-set-of-data'
		self.Y    = np.array([3.6  ,  3.333,  4.533,  4.7  ,  3.6  ,  4.35 ,  3.917,  4.2,         4.7  ,  4.8  ,  4.25 ,  3.45 ,  3.067,  4.533,  3.6  ,  4.083,         3.85 ,  4.433,  4.3  ,  4.467,  3.367,  4.033,  3.833,  4.833,         4.783,  4.35 ,  4.567,  4.533,  3.317,  3.833,  4.633,  4.8  ,         4.716,  4.833,  4.883,  3.717,  4.567,  4.317,  4.5  ,  4.8  ,         4.4  ,  4.167,  4.7  ,  4.7  ,  4.033,  4.5  ,  4.   ,  5.067,         4.567,  3.883,  3.6  ,  4.133,  4.333,  4.1  ,  4.067,  4.933,         3.95 ,  4.517,  4.   ,  4.333,  4.817,  4.3  ,  4.667,  3.75 ,         4.9  ,  4.367,  4.5  ,  4.05 ,  4.7  ,  4.85 ,  3.683,  4.733,         4.9  ,  4.417,  4.633,  4.6  ,  4.417,  4.067,  4.25 ,  4.6  ,         3.767,  4.5  ,  4.65 ,  4.167,  4.333,  4.383,  4.933,  3.733,         4.233,  4.533,  4.817,  4.333,  4.633,  5.1  ,  5.033,  4.   ,         4.6  ,  3.567,  4.   ,  4.5  ,  4.083,  3.967,  4.15 ,  3.833,         3.5  ,  4.583,  5.   ,  4.617,  4.583,  3.333,  4.167,  4.333,         4.5  ,  4.   ,  4.167,  4.583,  4.25 ,  3.767,  4.433,  4.083,         4.417,  4.8  ,  4.8  ,  4.1  ,  3.966,  4.233,  3.5  ,  4.366,         4.667,  4.35 ,  4.133,  4.6  ,  4.367,  3.85 ,  4.5  ,  4.7  ,         3.833,  3.417,  4.233,  4.8  ,  4.15 ,  4.267,  4.483,  4.   ,         4.117,  4.083,  4.267,  3.917,  4.55 ,  4.083,  4.183,  4.45 ,         4.283,  3.95 ,  4.15 ,  4.933,  4.583,  3.833,  4.367,  4.35 ,         4.45 ,  3.567,  4.5  ,  4.15 ,  3.817,  3.917,  4.45 ,  4.283,         4.767,  4.533,  4.25 ,  4.75 ,  4.117,  4.417,  4.467])
		self.z    = 0.9793
		self.p    = 0.01052
		self.note = 'Note     ', 'Subset of the Old Faithful dataset "faithful" in R (r-project.org);  the Shapiro-Wilk test was conducted only on responses with values greater than three.'


class RSAge(_base.DatasetNormalitySW):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/tests-normality-and-symmetry/statistical-tests-normality-symmetry/shapiro-wilk-expanded-test/'
		self.Y    = np.array([65,61,63,86,70,  55,74,35,72,68,  45,58])
		self.z    = 0.971026
		self.p    = 0.921649
		self.note = 'Note     ', 'Shapiro-Wilk Expanded Test, Example 1'

class RSShapiroWilk1(_base.DatasetNormalitySW):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/tests-normality-and-symmetry/statistical-tests-normality-symmetry/shapiro-wilk-expanded-test/'
		self.Y    = np.array([19, 41, 29, 95, 8, 29, 11, 59, 41, 48, 53, 35, 11])
		self.z    = 0.918062
		self.p    = 0.236166
		self.note = 'Note     ', 'Shapiro-Wilk Expanded Test, Example 3, Sample 1'

class RSShapiroWilk2(_base.DatasetNormalitySW):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/tests-normality-and-symmetry/statistical-tests-normality-symmetry/shapiro-wilk-expanded-test/'
		self.Y    = np.array([12, 27, 18, 23, 72, 27, 27, 53, 3, 45, 53, 125, 50])
		self.z    = 0.864487
		self.p    = 0.044166
		self.note = 'Note     ', 'Shapiro-Wilk Expanded Test, Example 3, Sample 2'

class RSShapiroWilk3(_base.DatasetNormalitySW):
	def _set_values(self):
		self.www  = 'http://www.real-statistics.com/tests-normality-and-symmetry/statistical-tests-normality-symmetry/shapiro-wilk-expanded-test/'
		self.Y    = np.array([145, 125, 190, 135, 220, 5, 130, 210, 3, 165, 165, 150, 60])
		self.z    = 0.89263
		self.p    = 0.105972
		self.note = 'Note     ', 'Shapiro-Wilk Expanded Test, Example 3, Sample 3'

class ZarBiostatisticalAnalysis68(_base.DatasetNormality):
	def _set_values(self):
		self.www  = 'https://mathworks.com/matlabcentral/fileexchange/3954-dagosptest'
		self.Y    = np.array([63, 63, 64, 64, 65, 65, 65, 66, 66, 66, 66, 66, 67, 67, 67, 67, 68, 68, 68, 68, 68, 68, 69, 69, 69, 69, 69, 70, 70, 70, 70, 70, 70, 70, 70, 71, 71, 71, 71, 71, 71, 71, 72, 72, 72, 72, 72, 72, 72, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 74, 74, 74, 74, 74, 74, 75, 75, 75, 76, 76])
		self.z    = 4.3931
		self.df   = 1,2
		self.p    = 0.1112
		self.note = 'Note     ', 'Data available in "DagosPtest.m" at Matlab Central.  Data are from Example 6.8 (p.89) in:  Zar JH (1999), Biostatistical Analysis (2nd ed.). NJ: Prentice-Hall, Englewood Cliffs. '



