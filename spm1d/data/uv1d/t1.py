# coding: utf-8

import os
import numpy as np
from .. import _base





class Random(_base.DatasetT1, _base.Dataset1D):
	def _set_values(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'random.npy')
		self.Y        = np.load(self.datafile)
		self.mu       = 0
		self.z        = None
		self.df       = None
		self.p        = None


class RandomRough(_base.DatasetT1, _base.Dataset1D):
	def _set_values(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'random_rough.npy')
		self.Y        = np.load(self.datafile)
		self.mu       = 0
		self.z        = None
		self.df       = None
		self.p        = None


class SimulatedPataky2015a(_base.DatasetT1, _base.Dataset1D):
	def _set_values(self):
		self.cite     = 'Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2015). Zero- vs. one-dimensional, parametric vs. non-parametric, and confidence interval vs. hypothesis testing procedures in one-dimensional biomechanical trajectory analysis. Journal of Biomechanics, 1–9. http://doi.org/10.1016/j.jbiomech.2015.02.051'
		self.datafile = os.path.join(_base.get_datafilepath(), 'simscalar_datasetA.npy')
		self.Y        = np.load(self.datafile)
		self.mu       = 0
		self.z        = None
		self.df       = None
		self.p        = None

class SimulatedPataky2015b(_base.DatasetT1, _base.Dataset1D):
	def _set_values(self):
		self.cite     = 'Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2015). Zero- vs. one-dimensional, parametric vs. non-parametric, and confidence interval vs. hypothesis testing procedures in one-dimensional biomechanical trajectory analysis. Journal of Biomechanics, 1–9. http://doi.org/10.1016/j.jbiomech.2015.02.051'
		self.datafile = os.path.join(_base.get_datafilepath(), 'simscalar_datasetB.npy')
		self.Y        = np.load(self.datafile)
		self.mu       = 0
		self.z        = None
		self.df       = None
		self.p        = None






