
'''
SPM module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
'''

# Copyright (C) 2023  Todd Pataky


import numpy as np
from ... import prob
# from ... _plot import _plot_F_list
from ... util import array2shortstr, arraytuple2str, dflist2str, resels2str, DisplayParams



class SPMFList(list):
	STAT          = 'F'
	name          = 'SPM{F} list'
	# testname      = None
	# design        = ''
	dim           = 0
	isparametric  = True
	effect_labels = None
	
	# def __init__(self, FF):
	# 	super().__init__(FF)
	# 	self.neffects  = len(self)
	# 	self.dim       = self[0].dim
	# 	# if self.dim==0:
	# 	# 	self.name += ' (0D)'


	# def __init__(self, FF, nFactors=2):
	# 	super(SPMFList, self).__init__(FF)
	# 	self.nEffects  = len(self)
	# 	self.nFactors  = nFactors
	# 	self.dim       = self[0].dim
	# 	if self.dim==0:
	# 		self.name += ' (0D)'
	def __getitem__(self, i):
		if isinstance(i, int):
			return super().__getitem__(i)
		else:
			return self[ self.effect_labels.index(i) ]
	def __repr__(self):
		return self._repr_summ()
	

	@property
	def contrasts(self):
		return self[0].design.contrasts
	@property
	def design(self):
		return self[0].design
	@property
	def dfe(self):
		return self[0].df[1]
	@property
	def dim(self):
		return self[0].dim
	@property
	def fit(self):
		return self[0].fit
	@property
	def neffects(self):
		return len(self)
	@property
	def nfactors(self):
		return self[0].design.nfactors
	@property
	def testname(self):
		return self[0].testname

	
	def _repr_get_header(self):
		s        = '%s\n'  %self.name
		s       += '   testname  :  %s\n'      %self.testname
		s       += '   nfactors  :  %d\n'      %self.nfactors
		s       += '   neffects  :  %d\n'      %self.neffects
		return s
	# def _repr_summ(self):
	# 	n         = max( [len(spm.contrast.name_s) for spm in self] )
	# 	s         = self._repr_get_header()
	# 	s        += 'Effects:\n'
	# 	for f in self:
	# 		s    += '   %s' %f._repr_summ(n)
	# 	return s
	def _repr_verbose(self):
		s        = self._repr_get_header()
		s       += '\n'
		for f in self:
			s   += f.__repr__()
			s   += '\n'
		return s


	def _repr_summ(self):
		dp      = DisplayParams( self )
		dp.add_default_header()
		dp.add( 'testname' )
		dp.add( 'nfactors' )
		dp.add( 'neffects' )
		dp.add_header('Effects')
		s = dp.asstr()
		for f in self:
			s    += '    %s' %f._repr_summ()
		# dp.add( 'STAT' )
		# if self.isanova:
		# 	dp.add( 'effect_name' )
		# 	dp.add( 'ss' , array2shortstr )
		# 	dp.add( 'ms' , array2shortstr )
		# dp.add( 'z', fmt=array2shortstr )
		# if self.isregress:
		# 	dp.add('r', fmt=array2shortstr )
		# dp.add( 'df', fmt=dflist2str )
		# dp.add_header( 'Smoothness estimates:' )
		# dp.add( 'fwhm', fmt='%.3f' )
		# dp.add( 'lkc', fmt='%.3f' )
		# dp.add( 'resels', fmt=resels2str )
		return s

	



	def _set_data(self, *args, **kwargs):
		self._args   = args
		self._kwargs = kwargs
		for f in self:
			f._set_data( *args, **kwargs )
	def _set_testname(self, name):
		self.testname = str( name )
		for f in self:
			f._set_testname( name )
	
	def get_df_values(self):
		return [f.df for f in self]
	def get_effect_labels(self):
		return tuple( [f.effect for f in self] )
	def get_f_values(self):
		return tuple( [f.z for f in self] )
	
	
	# def _inference0d(self, alpha, **kwargs):
	# 	if method == 'param':
	# 		results  = prob.param(self.STAT, self.z, dfa, alpha=alpha, dirn=dirn)
	# 		return self._build_spmi(results, alpha, dirn=dirn, df_adjusted=dfa)
	#
	# 		spmi = self._inference_param(alpha, **kwargs)
	#
	# 	elif method == 'perm':
	# 		spmi = self._inference_perm(alpha, **kwargs)
		
	
	# def _build_spmis(self, method, alpha, zc, p, df_adjusted=None):
	
	# def _build_spmis_perm(self, results, alpha, df_adjusted=None):
	# 	from copy import deepcopy
	# 	from . _spm0di import SPM0Di
	#
	# 	fis = []
	# 	for f,res in enumerate( zip(self,results) ):
	# 		fi             = deepcopy( f )
	# 		fi.__class__   = SPM0Di
	# 		fi.df_adjusted = df_adjusted
	# 		fi.method      = results.method
	# 		fi.alpha       = alpha
	# 		fi.zc          = results.zc
	# 		fi.p           = results.p[i]
	# 		fi.nperm       = results.nperm
	# 		fi.permuter    = results.permuter
	# 		fis.append( fi )
	# 	return SPMFiList( fis )

		# fis = []
		# for i,(f) in enumerate(self):
		# 	fi             = deepcopy( f )
		# 	fi.__class__   = SPM0Di
		# 	fi.df_adjusted = df_adjusted
		# 	fi.method      = results.method
		# 	fi.alpha       = alpha
		# 	fi.zc          = results.zc[i]
		# 	fi.p           = results.p[i]
		# 	fi.nperm       = results.nperm
		# 	fi.permuter    = results.permuter
		# 	fis.append( fi )
		# return SPMFiList( fis )
	

	def inference(self, alpha=0.05, method='param', **kwargs):
		
		dfa = None
		
		# if self.dim == 0:
		# 	if method=='param':
		# 		FFi               = SPMFiList(  [f.inference(alpha=alpha, **kwargs)   for f in self]  )
		#
		# 	elif method=='perm':
		# 		z       = np.array([f.z for f in self])
		# 		nperm   = kwargs['nperm']
		# 		results = prob.perm(self.STAT, z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, dim=0)
		# 		FFi     = self._build_spmis_perm(results, alpha, df_adjusted=dfa)


		if method in ['param', 'rft']:
			# FFi     = SPMFiList(self,  [f.inference(alpha=alpha, **kwargs)   for f in self]  )
			FFi     = SPMFiList(  [f.inference(alpha=alpha, **kwargs)   for f in self]  )
			
		elif method == 'perm':
			z       = np.array([f.z for f in self])
			nperm   = kwargs['nperm']
			results = prob.perm(self.STAT, z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, dim=self.dim)
			FFi     = SPMFiList( [f._build_spmi(res, dfa)  for f,res in zip(self, results)]   )
			
		elif method == 'fdr':
			FFi     = SPMFiList( [f.inference(alpha=alpha, method='fdr', **kwargs)   for f in self]  )
		

		# FFi.set_design_label( self.design )
		# FFi.effect_labels = self.effect_labels
		# FFi.nfactors      = self.nfactors
		
		return FFi
		
		


	def normality_test(self, alpha=0.05):
		# residuals are identical for all F objects (same model)
		# so normality test can be conducted on any of the F objects
		return self[0].normality_test(alpha=alpha)
	
		
		
	def plot(self, plot_threshold_label=True, plot_p_values=True, autoset_ylim=True):
		from ... _plot import _plot_F_list
		_plot_F_list(self, plot_threshold_label, plot_p_values, autoset_ylim)
	def print_summary(self):
		print( self._repr_summ() )
			
			
		print( self._repr_verbose() )
	def print_verbose(self):
		print( self._repr_verbose() )
	# def set_design_label(self, label):
	# 	self.design  = str(label)
	def set_effect_labels(self, labels):
		[F.set_effect_label(label)  for F,label in zip(self, labels)]
		self.effect_labels   = [F.effect_label_s   for F in self]

	def set_factor_names(self, names, names_s=None):
		self.design.set_factor_names(names, names_s)

		# if names_short is None:
		# 	names_short = [None] * self.nfactors
		#
		# for factor,s,ss in zip(self.design.factors, names, names_short):
		# 	factor.set_name( s, ss )


# class SPMiList(list):
# 	pass


class SPMFiList(SPMFList):
	name          = 'SPM{F} inference list'
	
	# def __init__(self, spmlist, spmis):
	# 	super().__init__(spmis)
	# 	# self.testname = spmlist.testname
	
	
	@property
	def h0reject(self):
		for f in self:
			if f.h0reject:
				return True
		return False
	def get_h0reject_values(self):
		return tuple( [f.h0reject for f in self] )
	def get_p_values(self):
		return tuple( [f.p for f in self] )
	def get_zstar_values(self):
		return tuple( [f.zstar for f in self] )


	def print_table(self):
		n    = 1 + max(   [len(f.name_s)  for f in self]   )
		fmt0 = '{:<%d} {:>6} {:>8} {:>8} {:>8} {:>8}' %n
		fmt  = '{:<%d} {:6.3f} {:8.3f} {:8.3f} {:8.3f} {:8.3f}' %n
		fmte = '{:<%d} {:6.3f} {:8.3f} {:8.3f}' %n
		# print table
		print( fmt0.format('Source', 'DF', 'SS', 'MS', 'F', 'P') )
		for f in self:
			print( fmt.format(f.name_s, f.df[0], f.ss, f.ms, f.z, f.p) )
		print( fmte.format('Error', self.dfe, self.fit.sse, self.fit.mse) )

