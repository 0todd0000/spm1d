
'''
SPM-0D module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for 0D SPMs.
'''

# Copyright (C) 2023  Todd Pataky


import numpy as np
from . _spm import _SPM
from ... util import dflist2str, tuple2str, DisplayParams





class SPM0D(_SPM):
	
	dim         =  0

	def __repr__(self):
		dp      = DisplayParams( self )
		dp.add_header( self._class_str )
		dp.add( 'testname' )
		dp.add( 'STAT' )
		dp.add( 'z', fmt='%.5f' )
		if self.isregress:
			dp.add('r', fmt='%.5f')
		dp.add( 'df', fmt=dflist2str )
		if self.isanova:
			# dp.add( 'ss' , tuple2str )
			# dp.add( 'ms' , tuple2str )
			dp.add( 'ss', fmt='%.5f' )
			dp.add( 'ms', fmt='%.5f' )
			dp.add( 'name' )
			dp.add( 'name_short' )
		
		return dp.asstr()


	# def _adjust_df(self):
	#   this code was commented out on 2023-06-01 during v0.5 development
	# 	it uses the old _reml.py module which is now in _cov.py
	#   but this method may not be necessary at all
	#
	### heteroscedasticity correction:
	# 	if self.testname == 'ttest2':
	# 		from .. import _reml
	# 		yA,yB            = self._args
	# 		y                = np.hstack([yA,yB]) if (self.dim==0) else np.vstack([yA,yB])
	# 		JA,JB            = yA.shape[0], yB.shape[0]
	# 		J                = JA + JB
	# 		q0,q1            = np.eye(JA), np.eye(JB)
	# 		Q0,Q1            = np.matrix(np.zeros((J,J))), np.matrix(np.zeros((J,J)))
	# 		Q0[:JA,:JA]      = q0
	# 		Q1[JA:,JA:]      = q1
	# 		Q                = [Q0, Q1]
	# 		df               = _reml.estimate_df_T(y, self.X, self.residuals, Q)
	# 		dfa              = (1, df)
	#
	# 	elif self.testname == 'anova1':
	# 		warnings.warn('\nWARNING:  Non-sphericity corrections for one-way ANOVA are currently approximate and have not been verified.\n', UserWarning, stacklevel=2)
	# 		Y,X,r   = model.Y, model.X, model.eij
	# 		Q,C     = design.A.get_Q(), design.contrasts.C.T
	# 		spm.df  = _reml.estimate_df_anova1(Y, X, r, Q, C)
	


	# def _inference_perm(self, alpha, nperm=10000, dirn=0):
	# 	if self.isinlist:
	# 		raise NotImplementedError( 'Permutation inference must be conducted using the parent SnPMList (for two- and three-way ANOVA).' )
	#
	#
	# 	results = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, dirn=dirn)
	# 	return self._build_spmi(results)
	
	
	def _repr_summ(self, n=5):  # used only for ANOVA
		fmts = '{:<%s}   F = {:<8} df = {}\n' %n
		return fmts.format( self.name_s,  '%.3f'%self.z, dflist2str(self.df) )
		# return fmts.format( self.effect_label,  '%.3f'%self.z, dflist2str(self.df) )
		# return '{:<5}:   F = {:<8} df = {}\n'.format(self.effect_label,  '%.3f'%self.z, dflist2str(self.df))
	def _repr_teststat_short(self):
		return '%.3f' %self.z
	
	

	def inference(self, alpha, method='param', **kwargs):
		from . _argparsers import InferenceArgumentParser0D
		parser   = InferenceArgumentParser0D(self.STAT, method)
		parser.parse( alpha, **kwargs )

		from ... import prob

		if method == 'param':
			dfa = self.df
			# if not equal_var:
			# 	dfa = self._adjust_df()
			# iresults  = prob.param(self.STAT, self.z, dfa, alpha=alpha, dirn=dirn)
			iresults  = prob.param(self.STAT, self.z, dfa, alpha=alpha, **kwargs)
			
			

		elif method == 'perm':
			if self.isinlist:
				raise NotImplementedError( 'Permutation inference must be conducted using the parent SnPMList (for two- and three-way ANOVA).' )
			dfa      = self.df
			# iresults = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, dirn=dirn)
			iresults = prob.perm(self.STAT, self.z, alpha=alpha, testname=self.testname, args=self._args, nperm=nperm, **kwargs)
			
			# spmi = self._inference_perm(alpha, **parser.kwargs)

		return self._iresults2spmi(iresults, dfa, alpha, method, kwargs)






