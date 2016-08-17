
import numpy as np
from .. import _base




class ZarBiostatisticalAnalysis68(_base.DatasetNormality):
	def _set_values(self):
		self.www  = 'https://mathworks.com/matlabcentral/fileexchange/3954-dagosptest'
		self.Y    = np.array([63, 63, 64, 64, 65, 65, 65, 66, 66, 66, 66, 66, 67, 67, 67, 67, 68, 68, 68, 68, 68, 68, 69, 69, 69, 69, 69, 70, 70, 70, 70, 70, 70, 70, 70, 71, 71, 71, 71, 71, 71, 71, 72, 72, 72, 72, 72, 72, 72, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 74, 74, 74, 74, 74, 74, 75, 75, 75, 76, 76])
		self.z    = 4.3931
		self.df   = 1,2
		self.p    = 0.1112
		self.note = 'Note     ', 'Data available in "DagosPtest.m" at Matlab Central.  Data are from Example 6.8 (p.89) in:  Zar JH (1999), Biostatistical Analysis (2nd ed.). NJ: Prentice-Hall, Englewood Cliffs. '


class KendallRandomNumbers(_base.DatasetNormality):
	def _set_values(self):
		self.www  = 'http://www.statext.com/practice/NormalityTest04.php'
		self.Y    = np.array([303, 338, 406, 457, 461, 469, 474, 489, 515, 583])
		self.z    = 0.66
		self.df   = 1,2
		self.p    = 0.7195
		self.note = 'Note     ', 'Original data are from p.194 of:  Kendall M (1948) Rank Correlation Methods, Charles Griffin & Company Ltd.'


