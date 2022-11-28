# coding: utf-8

import os
import numpy as np
from .. import _base




class SimulatedPataky2015c(_base.DatasetRegress, _base.Dataset1D):
	def _set_values(self):
		self.cite     = 'Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2015). Zero- vs. one-dimensional, parametric vs. non-parametric, and confidence interval vs. hypothesis testing procedures in one-dimensional biomechanical trajectory analysis. Journal of Biomechanics, 1–9. http://doi.org/10.1016/j.jbiomech.2015.02.051'
		self.datafile = os.path.join(_base.get_datafilepath(), 'simscalar_datasetC.npy')
		self.Y        = np.load(self.datafile)
		self.x        = np.arange(self.Y.shape[0])
		self.z        = None
		self.r        = None
		self.df       = None
		self.p        = None


class SpeedGRF(_base.DatasetRegress, _base.Dataset1D):
	def __init__(self, subj=0):
		self.subj     = int(subj)
		super(SpeedGRF, self).__init__()

	def _set_values(self):
		self.cite     = 'Pataky, T. C., Caravaggi, P., Savage, R., Parker, D., Goulermas, J., Sellers, W., & Crompton, R. (2008). New insights into the plantar pressure correlates of walking speed using pedobarographic statistical parametric mapping (pSPM). Journal of Biomechanics, 41(9), 1987–1994.'
		fnameY        = os.path.join(_base.get_datafilepath(), 'ex_grf_subj%03d.npy'%self.subj)
		fnameX        = os.path.join(_base.get_datafilepath(), 'ex_grf_speeds.npy')
		self.datafile = fnameY
		self.Y        = np.load(fnameY)
		self.x        = np.load(fnameX)[:,self.subj]
		self.z        = None
		self.r        = None
		self.df       = None
		self.p        = None





