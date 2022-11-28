# coding: utf-8

import os
import numpy as np
from .. import _base




class PlantarArchAngle(_base.DatasetTpaired, _base.Dataset1D):
	def _set_values(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'ex_kinematics.npy')
		self.cite     = 'Caravaggi, P., Pataky, T., Günther, M., Savage, R., & Crompton, R. (2010). Dynamics of longitudinal arch support in relation to walking speed: contribution of the plantar aponeurosis. Journal of Anatomy, 217(3), 254–261. http://doi.org/10.1111/j.1469-7580.2010.01261.x'
		Y             = np.load(self.datafile)
		self.YA       = Y[10:20]
		self.YB       = Y[20:]
		self.z        = None
		self.df       = None
		self.p        = None