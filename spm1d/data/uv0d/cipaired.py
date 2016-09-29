
import numpy as np
from .. import _base




class FraminghamSystolicBloodPressure(_base.DatasetCIpaired):
	def _set_values(self):
		self.www      = 'http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/BS704_Confidence_Intervals/BS704_Confidence_Intervals_print.html'
		self.YA       = np.array([141, 119, 122, 127, 125, 123, 113, 106, 131, 142, 131, 135, 119, 130, 121], dtype=float)
		self.YB       = np.array([168, 111, 139, 127, 155, 115, 125, 123, 130, 137, 130, 129, 112, 141, 122], dtype=float)
		self.alpha    = 0.05
		self.mu       = 0
		self.ci       = (-12.4, 1.8)
		self.note     = 'Note     ', 'From "Confidence Intervals for Matched Samples, Continuous Outcome" at the link above.'





