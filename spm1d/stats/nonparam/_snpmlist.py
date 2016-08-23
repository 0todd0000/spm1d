
import numpy as np
import _snpm
from .. import _spmlist



class SnPMFList0D(_spmlist.SPMFList, _snpm._SnPM0D):
	
	name          = 'SnPM{F} list'
	isparametric  = False
	
	def __init__(self, z, perm):
		z                   = [0 if np.isnan(zz) else zz  for zz in z]
		FF                  = [_snpm.SnPM0D_F(zz, isinlist=True)   for zz in z]
		super(SnPMFList0D, self).__init__(FF)
		self.permuter       = perm             #permuter (for conducting inference)
		self.nPermUnique    = perm.nPermTotal  #number of unique permutations possible
		self.z              = z                #test statistic
		self.set_design_label( perm.get_design_label() )
		self.set_effect_labels( perm.get_effect_labels() )
	
	def _repr_get_header(self):
		s        = '%s\n'  %self.name
		s       += '   design      :  %s\n'      %self.design
		s       += '   nEffects    :  %d\n'      %self.nEffects
		s       += '   nPermUnique :  %s\n'      %self.get_nPermUnique_asstr()
		return s
	
	

	def inference(self, alpha=0.05, iterations=-1, force_iterations=False):
		self._check_iterations(iterations, alpha, force_iterations)
		self.permuter.build_pdf(iterations)
		zstarlist = self.permuter.get_z_critical_list(alpha)
		plist     = self.permuter.get_p_value_list(self.z, zstarlist, alpha)
		return SnPMFiList0D(self, alpha, zstarlist, plist, iterations)




class SnPMFiList0D(_spmlist.SPMFiList, _snpm._SnPM):
	name          = 'SnPM{F} inference list'
	isparametric  = False
	
	def __init__(self, snpmlist, alpha, zstarvalues, pvalues, iterations):
		FFi       = []
		for F,zstar,p in zip(snpmlist, zstarvalues, pvalues):
			Fi    = _snpm.SnPM0DiF(F, alpha, zstar, p, isinlist=True)
			FFi.append( Fi )
		super(SnPMFiList0D, self).__init__( FFi )
		
		# z                   = [0 if np.isnan(zz) else zz  for zz in z]
		# FF                  = [SnPM0D_F(zz, isinlist=True)   for zz in z]
		# super(SnPMFList0D, self).__init__(FF)
		self.alpha          = alpha
		self.permuter       = snpmlist.permuter             #permuter (for conducting inference)
		self.nPermUnique    = snpmlist.permuter.nPermTotal  #number of unique permutations possible
		self.nPermActual    = snpmlist.permuter.Z.shape[0]
		self.z              = [Fi.z  for Fi in self]    #test statistic
		self.set_design_label( self.permuter.get_design_label() )
		self.set_effect_labels( self.permuter.get_effect_labels() )


	def _repr_get_header(self):
		s        = '%s\n'  %self.name
		s       += '   design      :  %s\n'      %self.design
		s       += '   nEffects    :  %d\n'      %self.nEffects
		s       += '   nPermUnique :  %s\n'      %self.get_nPermUnique_asstr()
		s       += '   nPermActual :  %d\n'      %self.nPermActual
		return s
		

	




class SnPMFList(_spmlist.SPMFList, _snpm._SnPM1D):
	
	name          = 'SnPM{F} list'
	isparametric  = False
	
	def __init__(self, z, perm):
		FF                  = [_snpm.SnPM_F(zz, perm, isinlist=True)   for zz in z]
		super(SnPMFList, self).__init__(FF)
		self.permuter       = perm             #permuter (for conducting inference)
		self.nPermUnique    = perm.nPermTotal  #number of unique permutations possible
		self.z              = z                #test statistic
		self.set_design_label( perm.get_design_label() )
		self.set_effect_labels( perm.get_effect_labels() )
	
	def _repr_get_header(self):
		s        = '%s\n'  %self.name
		s       += '   design      :  %s\n'      %self.design
		s       += '   nEffects    :  %d\n'      %self.nEffects
		s       += '   nPermUnique :  %s\n'      %self.get_nPermUnique_asstr()
		return s
	
	# def _repr_summ(self):
	# 	return '{:<5} F = {:<8}\n'.format(self.effect_short,  '%.3f'%self.z)
		
	# def _repr_summ(self):
	# 	s         = self._repr_get_header()
	# 	s        += 'Effects:\n'
	# 	for f in self:
	# 		s    += '   %s' %f._repr_summ()
	# 	return s
	
	

	# def inference(self, alpha=0.05, iterations=-1, force_iterations=False):
	# 	self._check_iterations(iterations, alpha, force_iterations)
	# 	self.permuter.build_pdf(iterations)
	# 	zstarlist = self.permuter.get_z_critical_list(alpha)
	# 	plist     = self.permuter.get_p_value_list(self.z, zstarlist, alpha)
	# 	return SnPMFiList0D(self, alpha, zstarlist, plist, iterations)
	
	def build_secondary_pdf(self, zstarlist, circular=False):
		self.permuter.build_secondary_pdf( zstar, circular )
	

	def inference(self, alpha=0.05, iterations=-1, interp=True, circular=False, force_iterations=False, cluster_metric='MaxClusterIntegral'):
		self._check_iterations(iterations, alpha, force_iterations)
		### build primary PDF:
		self.permuter.build_pdf(iterations)
		zstarlist  = self.permuter.get_z_critical_list(alpha)
		### build secondary PDF:
		self.permuter.set_metric( cluster_metric )
		self.permuter.build_secondary_pdfs(zstarlist, circular)
		### assemble clusters and conduct cluster-level inference:
		FFi            = []
		for F,zstar in zip(self, zstarlist):
			clusters   = F._get_clusters(zstar, False, interp, circular, iterations, cluster_metric)
			clusters   = F._cluster_inference(clusters, False)
			Fi         = _snpm.SnPMiF(F, alpha, zstar, clusters)
			FFi.append( Fi )
		return SnPMFiList( self, FFi )

		# else:
		# 	Fi     = SnPMinference(self, alpha, zstar, two_tailed, clusters)
		# return Fi



class SnPMFiList(SnPMFList):

	name          = 'SnPM{F} inference list'
	isparametric  = False

	def __init__(self, snpmlist, FFi ):
		super(SnPMFList, self).__init__(FFi)
		self.permuter       = snpmlist.permuter
		self.nPermUnique    = snpmlist.nPermUnique
		# self.z              = z                #test statistic
		self.set_design_label( self.permuter.get_design_label() )
		self.set_effect_labels( self.permuter.get_effect_labels() )

