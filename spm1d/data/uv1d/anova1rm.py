# coding: utf-8

import os
import numpy as np
from .. import _base




class SpeedGRFcategoricalRM(_base.DatasetANOVA1rm, _base.Dataset1D):
	def _set_values(self):
		self.cite     = 'Pataky, T. C., Caravaggi, P., Savage, R., Parker, D., Goulermas, J., Sellers, W., & Crompton, R. (2008). New insights into the plantar pressure correlates of walking speed using pedobarographic statistical parametric mapping (pSPM). Journal of Biomechanics, 41(9), 1987–1994.'
		self.datafile = os.path.join(_base.get_datafilepath(), 'ex_grf_means.npz')
		Z             = np.load(self.datafile)
		self.Y        = Z['Y']
		self.A        = Z['SPEED']
		self.SUBJ     = Z['SUBJ']
		Z.close()
		self.z        = None
		self.df       = None
		self.p        = None





