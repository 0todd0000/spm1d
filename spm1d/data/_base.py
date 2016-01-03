'''
Base classes for all built-in datasets.
'''

# Copyright (C) 2016  Todd Pataky
# designs.py version: 0.3.2 (2016/01/03)


import os
import numpy as np


def get_datafilepath():
	return os.path.join( os.path.dirname(__file__), 'datafiles' )


class _Dataset(object):
	def __init__(self):
		self._rtol    = 0.001  #relative tolerance (for unit tests)
		self.STAT     = 'Z'
		self.design   = None   #design string (e.g. "One-way ANOVA")
		self.dim      = 0      #data dimensionality (0 or 1)
		self.Y        = None   #dataset
		self.z        = None   #expected test stat
		self.df       = None   #expected degrees of freedom
		self.p        = None   #expected p value
		self.cite     = None   #literature citation (if relevant)
		self.datafile = None   #data file (if available on the web)
		self.www      = None   #web source
		self.note     = None   #note
		self._set_values()
	def __repr__(self):
		s      = 'Dataset\n'
		s     += '   Name      : "%s"\n' %self.__class__.__name__
		s     += '   Design    :  %s\n' %self.design
		s     += '   Data dim  :  %d\n' %self.dim
		if self.cite:
			s += '   Reference :  %s\n' %self.cite
		if self.www:
			s += '   Web       :  %s\n' %self.www
		if self.datafile:
			s += '   Data file :  %s\n' %self.datafile
		if self.note:
			s += '   %s :  %s\n' %tuple(self.note)
		ss     = self.get_expected_results_as_string()
		s     += ss 
		return s
	def _printR(self, x, name='x'):
		print '%s = c(%s)' %(name, str(x.tolist())[1:-1])
	def _printRs(self, xx, names=('x')):
		for x,name in zip(xx,names):
			print
			self._printR(x, name)
	def _set_values(self):    #abstract method;  instantiated by all subclasses
		pass
	def get_dependent_variable(self):
		return self.Y
	def get_expected_df(self):
		return self.df
	def get_data(self):
		return self.Y
	def get_expected_test_stat(self):
		return self.z
	def get_expected_p_value(self):
		return self.p
	def get_expected_results_as_string(self):
		s      = '  (Expected results)\n'
		s     += '  %s          :  %s\n' %(self.STAT, str(self.z))
		s     += '  df         :  %s\n' %str(self.df)
		s     += '  p          :  %s\n' %str(self.p)
		return s




# class _Dataset0D(_Dataset):
# 	pass
class Dataset1D(_Dataset):
	def __init__(self):
		super(Dataset1D, self).__init__()
		self.dim       = 1


class _DatasetANOVA(_Dataset):
	def __init__(self):
		super(_DatasetANOVA, self).__init__()
		self.STAT   = 'F'
class _DatasetT(_Dataset):
	def __init__(self):
		super(_DatasetT, self).__init__()
		self.STAT   = 't'
class _DatasetT2(_Dataset):
	def __init__(self):
		super(_DatasetT2, self).__init__()
		self.STAT   = 'T2'
class _DatasetX2(_Dataset):
	def __init__(self):
		super(_DatasetX2, self).__init__()
		self.STAT   = 'X2'



class DatasetANOVA1(_DatasetANOVA):
	def __init__(self):
		self.rm       = False  #repeated measures
		super(DatasetANOVA1, self).__init__()
		self.design = 'One-way ANOVA'
	def get_data(self):
		return self.Y, self.A
	# def get_expected_df(self, type='sphericity_assumed'):
	# 	if type=='sphericity_assumed':
	# 		return self.df
	# 	if type=='GG':
	# 		return self.dfGG
	# 	elif type=='GGX':
	# 		return self.dfGGX
	# 	elif type=='HF':
	# 		return self.dfHF
	# def get_expected_p_value(self, type='sphericity_assumed'):
	# 	if type=='sphericity_assumed':
	# 		return self.p
	# 	if type=='GG':
	# 		return self.pGG
	# 	elif type=='GGX':
	# 		return self.pGGX
	# 	elif type=='HF':
	# 		return self.pHF
	
class DatasetANOVA1rm(_DatasetANOVA):
	def __init__(self):
		self.rm       = True  #repeated measures
		super(DatasetANOVA1rm, self).__init__()
		self.design = 'One-way repeated measures ANOVA'
	def get_data(self):
		return self.Y, self.A, self.SUBJ

class DatasetANOVA2(_DatasetANOVA):
	def __init__(self):
		self.rm       = False  #repeated measures
		super(DatasetANOVA2, self).__init__()
		self.design = 'Two-way ANOVA'
	def get_data(self):
		return self.Y, self.A, self.B
	def print_variables_R_format(self):
		self._printRs(self.get_data(), ['Y','A','B'])
class DatasetANOVA2nested(DatasetANOVA2):
	def __init__(self):
		super(DatasetANOVA2nested, self).__init__()
		self.design = 'Two-way ANOVA (nested)'
class DatasetANOVA2rm(DatasetANOVA2):
	def __init__(self):
		self.rm       = True  #repeated measures
		super(DatasetANOVA2rm, self).__init__()
		self.design = 'Two-way repeated measures ANOVA'
	def get_data(self):
		return self.Y, self.A, self.B, self.SUBJ
class DatasetANOVA2onerm(DatasetANOVA2rm):
	def __init__(self):
		super(DatasetANOVA2onerm, self).__init__()
		self.design = 'Two-way ANOVA (repeated measures on one factor)'



class DatasetANOVA3(_DatasetANOVA):
	def __init__(self):
		self.rm       = False  #repeated measures
		super(DatasetANOVA3, self).__init__()
		self.design = 'Three-way ANOVA'
	def get_data(self):
		return self.Y, self.A, self.B, self.C
class DatasetANOVA3nested(DatasetANOVA3):
	def __init__(self):
		super(DatasetANOVA3nested, self).__init__()
		self.design = 'Three-way ANOVA (nested)'
class DatasetANOVA3rm(DatasetANOVA3):
	def __init__(self):
		self.rm       = True  #repeated measures
		super(DatasetANOVA3rm, self).__init__()
		self.design = 'Three-way ANOVA (repeated measures on all factors)'
	def get_data(self):
		return self.Y, self.A, self.B, self.C, self.SUBJ
	def print_variables_R_format(self):
		self._printRs(self.get_data(), ['Y','A','B','C','SUBJ'])
class DatasetANOVA3onerm(DatasetANOVA3rm):
	def __init__(self):
		self.rm       = True  #repeated measures
		super(DatasetANOVA3onerm, self).__init__()
		self.design = 'Three-way ANOVA (repeated measures on one factor)'
class DatasetANOVA3tworm(DatasetANOVA3rm):
	def __init__(self):
		super(DatasetANOVA3tworm, self).__init__()
		self.design = 'Three-way ANOVA (repeated measures on two factors)'





class DatasetCCA(_DatasetX2):
	def __init__(self):
		super(DatasetCCA, self).__init__()
		self.design = "Canonical Correlation Analysis"
	def get_data(self):
		return self.Y, self.x



class DatasetHotellings1(_DatasetT2):
	def __init__(self):
		super(DatasetHotellings1, self).__init__()
		self.design = "One-sample Hotelling's T2 test"
	def get_data(self):
		return self.Y, self.mu
class DatasetHotellings2(_DatasetT2):
	def __init__(self):
		super(DatasetHotellings2, self).__init__()
		self.design = "Two-sample Hotelling's T2 test"
	def get_data(self):
		return self.YA, self.YB
class DatasetHotellingsPaired(DatasetHotellings2):
	def __init__(self):
		super(DatasetHotellingsPaired, self).__init__()
		self.design = "Paired Hotelling's T2 test"



class DatasetMANOVA1(_DatasetX2):
	def __init__(self):
		super(DatasetMANOVA1, self).__init__()
		self.design = "One-way MANOVA"
	def get_data(self):
		return self.Y, self.A







class DatasetT1(_DatasetT):
	def __init__(self):
		self.mu     = None
		super(DatasetT1, self).__init__()
		self.design = 'One-sample t test'
	def get_data(self):
		return self.Y, self.mu

class DatasetT2(_DatasetT):
	def __init__(self):
		self.YA     = None
		self.YB     = None
		self.A      = None
		super(DatasetT2, self).__init__()
		self.design = 'Two-sample t test'
	def get_data(self):
		return self.YA, self.YB

class DatasetTpaired(DatasetT2):
	def __init__(self):
		super(DatasetTpaired, self).__init__()
		self.design = 'Paired t test'


class DatasetRegress(_DatasetT):
	def __init__(self):
		super(DatasetRegress, self).__init__()
		self.design = 'Simple linear regression'
	def get_data(self):
		return self.Y, self.x
	def get_expected_results_as_string(self):
		s      = '  (Expected results)\n'
		s     += '   %s          :  %s\n' %(self.STAT, self.z)
		s     += '   df         :  %s\n' %str(self.df)
		s     += '   r          :  %s\n' %str(self.r)
		s     += '   p          :  %s\n' %str(self.p)
		return s






