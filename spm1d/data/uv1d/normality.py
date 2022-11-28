
import os
import numpy as np
from .. import _base


class NormalityAppendixDataset(_base.DatasetNormality1D):
	def __init__(self, name='A1'):
		self.dname    = str(name)
		super(NormalityAppendixDataset, self).__init__()
	def _set_values(self):
		self.datafile = os.path.join(_base.get_datafilepath(), 'normality_dataset_%s.npy' %self.dname)
		self.Y        = np.load( self.datafile )
		self.cite     = 'Pataky TC, Vanrenterghem J, Robinson MA (2016) Normality assessments for one-dimensional biomechanical data.  Journal of Biomechanics (in review).'
		self.note     = 'Note     ', 'Appendix %s, Dataset %s' %(self.dname[0], self.dname)


