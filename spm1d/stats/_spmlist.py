
'''
SPM module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
'''

# Copyright (C) 2016  Todd Pataky


from .. _plot import _plot_F_list


class SPMFList(list):
	STAT          = 'F'
	name          = 'SPM{F} list'
	design        = ''
	dim           = 0
	nEffects      = 1
	isparametric  = True
	effect_labels = None
	
	def __init__(self, FF, nFactors=2):
		super(SPMFList, self).__init__(FF)
		self.nEffects  = len(self)
		self.nFactors  = nFactors
		self.dim       = self[0].dim
		if self.dim==0:
			self.name += ' (0D)'
	def __getitem__(self, i):
		if isinstance(i, int):
			return super(SPMFList, self).__getitem__(i)
		else:
			return self[ self.effect_labels.index(i) ]
	def __repr__(self):
		return self._repr_summ()
	
	def _repr_get_header(self):
		s        = '%s\n'  %self.name
		s       += '   design    :  %s\n'      %self.design
		s       += '   nEffects  :  %d\n'      %self.nEffects
		return s
	def _repr_summ(self):
		s         = self._repr_get_header()
		s        += 'Effects:\n'
		for f in self:
			s    += '   %s' %f._repr_summ()
		return s
	def _repr_verbose(self):
		s        = self._repr_get_header()
		s       += '\n'
		for f in self:
			s   += f.__repr__()
			s   += '\n'
		return s
	
	def get_df_values(self):
		return [f.df for f in self]
	def get_effect_labels(self):
		return tuple( [f.effect for f in self] )
	def get_f_values(self):
		return tuple( [f.z for f in self] )
	def inference(self, alpha=0.05):
		FFi               = SPMFiList(  [f.inference(alpha=alpha)   for f in self]  )
		FFi.set_design_label( self.design )
		FFi.effect_labels = self.effect_labels
		FFi.nFactors      = self.nFactors
		return FFi
	def plot(self, plot_threshold_label=True, plot_p_values=True, autoset_ylim=True):
		_plot_F_list(self, plot_threshold_label, plot_p_values, autoset_ylim)
	def print_summary(self):
		print( self._repr_summ() )
	def print_verbose(self):
		print( self._repr_verbose() )
	def set_design_label(self, label):
		self.design  = str(label)
	def set_effect_labels(self, labels):
		[F.set_effect_label(label)  for F,label in zip(self, labels)]
		self.effect_labels   = [F.effect_short   for F in self]



class SPMFiList(SPMFList):
	name          = 'SPM{F} inference list'
	def get_h0reject_values(self):
		return tuple( [f.h0reject for f in self] )
	def get_p_values(self):
		return tuple( [f.p for f in self] )
	def get_zstar_values(self):
		return tuple( [f.zstar for f in self] )


