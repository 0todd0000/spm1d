
from math import ceil
import numpy as np
from metrics import metric_dict
from .. import _spm
from .. _spm import p2string, plist2string, _SPMF, SPMFList, SPMFiList
from .. _clusters import ClusterNonparam






class _SnPM(object):
	'''Parent class for all non-parametric SPM classes.'''
	
	STAT          = 'Z'     #test statistic ("T", "F", "X2" or "T2")
	isparametric  = False
	dim           = 0
	
	def _check_iterations(self, iterations, alpha, force_iterations):
		if iterations > self.nPermUnique:
			if self.nPermUnique!=-1:
				raise( ValueError('\nNumber of specified iterations (%d) exceeds the maximum possible number of iterations (%d)\n'%(iterations,self.nPermUnique)) )
		elif (((iterations==-1) and (self.nPermUnique>10000)) or (iterations>10000)) and not force_iterations:
			n    = self.nPermUnique if iterations==-1 else iterations
			raise( Warning('\nThe total nuumber of permutations is very large: %d\nTo enable non-parametric calculations for this many iterations set "force_iterations=True" when calling "inference".\nNOTE: Setting "force_iterations=True" may require substantial computational resources and may cause crashes. USE WITH CAUTION.'%n ))
		elif (iterations!=-1) and (iterations<10):
			raise( ValueError('\nNumber of specified iterations (%d) must be at least 10\n'%iterations) )
		elif (iterations>0) and (iterations<1/alpha):
			raise( ValueError('\nNumber of specified iterations (%d) must be at least %d to conduct inference at alpha=%0.5f\n'%(iterations, ceil(1/alpha), alpha) ))

	def get_nPermUnique_asstr(self):
		n = self.nPermUnique
		if n is None:
			s  = 'None  (child of SnPM list)'
		else:
			s  = str(n) if (n < 1e6) else '%.4g' %n
			s += ' permutations possible'
		return s



'''
################################
   0D SnPM CLASS DEFINITIONS
################################
'''





class _SnPM0D(_SnPM):
	'''Parent class for all 0D non-parametric SPM classes.'''
	def __init__(self, z, perm=None, isinlist=False):
		z                   = 0 if np.isnan(z) else z
		self.permuter       = perm             #permuter (for conducting inference)
		self.nPermUnique    = None if isinlist else perm.nPermTotal  #number of unique permutations possible
		self.z              = z                #test statistic
		self.isinlist       = isinlist         #is this object in a list (i.e. two- or three-way ANOVA)

	def __repr__(self):
		stat     = self.STAT
		if stat == 'T':
			stat = 't'
		nPermU   = 'inf' if (self.nPermUnique==-1) else str(self.nPermUnique)
		s        = ''
		s       += 'SnPM{%s}\n' %stat
		s       += '   SPM.z            :  %.3f\n' %self.z
		s       += '   SnPM.nPermUnique :  %s\n'   %self.get_nPermUnique_asstr()
		return s

	def inference(self, alpha=0.05, iterations=-1, force_iterations=False):
		if self.isinlist:
			raise( NotImplementedError( 'Non-parametric inference must be conducted using the parent SnPMList (for two- and three-way ANOVA).' ) )
		self._check_iterations(iterations, alpha, force_iterations)
		self.permuter.build_pdf(iterations)
		zstar     = self.permuter.get_z_critical(alpha)
		p         = self.permuter.get_p_value(self.z, zstar, alpha)
		return SnPM0Dinference(self, alpha, zstar, p)


class SnPMFList0D(SPMFList, _SnPM0D):
	
	name          = 'SnPM{F} list'
	isparametric  = False
	
	def __init__(self, z, perm):
		z                   = [0 if np.isnan(zz) else zz  for zz in z]
		FF                  = [SnPM0D_F(zz, isinlist=True)   for zz in z]
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
		# FFi       = []
		# for F,zstar,p in zip(self, zstarlist, plist):
		# 	spmi  = SnPM0DiF(F, alpha, zstar, p, isinlist=True)
		# 	FFi.append( spmi )
		# return SnPMFiList0D(self, FFi)
		
		# spmilist  = []
		# for z,zstar,p in zip(self.z, zstarlist, plist):
		# 	spm   = SnPM0D_F(z, self.permuter)
		# 	spmi  = SnPM0Dinference(spm, alpha, zstar, p)
		# 	spmilist.append( spmi )
		# return spmilist


class SnPMFiList0D(SPMFiList, _SnPM):
	name          = 'SnPM{F} inference list'
	isparametric  = False
	
	def __init__(self, snpmlist, alpha, zstarvalues, pvalues, iterations):
		FFi       = []
		for F,zstar,p in zip(snpmlist, zstarvalues, pvalues):
			Fi    = SnPM0DiF(F, alpha, zstar, p, isinlist=True)
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

# class _SnPM0Dlist(_SnPM0D):
	# def __init__(self, z, perm):
	# 	z                   = [0 if np.isnan(zz) else zz  for zz in z]
	# 	self.permuter       = perm             #permuter (for conducting inference)
	# 	self.nPermUnique    = perm.nPermTotal  #number of unique permutations possible
	# 	self.z              = z                #test statistic
#
# 	def __repr__(self):
# 		stat     = self.STAT
# 		zs       = ''
# 		for zz in self.z:
# 			zs  += '%.3f, ' %zz
# 		zs       = zs[:-2]
# 		nPermU   = 'inf' if (self.nPermUnique==-1) else str(self.nPermUnique)
# 		s        = ''
# 		s       += 'SnPM{%s}\n' %stat
# 		s       += '   SPM.z            :  %s\n' %zs
# 		s       += '   SnPM.nPermUnique :  %s unique permutations available\n' %self.get_nPermUnique_asstr()
# 		return s
#
# 	def inference(self, alpha=0.05, iterations=-1, force_iterations=False):
# 		self._check_iterations(iterations, alpha, force_iterations)
# 		self.permuter.build_pdf(iterations)
# 		zstarlist = self.permuter.get_z_critical_list(alpha)
# 		plist     = self.permuter.get_p_value_list(self.z, zstarlist, alpha)
# 		spmilist  = []
# 		for z,zstar,p in zip(self.z, zstarlist, plist):
# 			spm   = SnPM0D_F(z, self.permuter)
# 			spmi  = SnPM0Dinference(spm, alpha, zstar, p)
# 			spmilist.append( spmi )
# 		return spmilist








class SnPM0D_T(_SnPM0D):
	STAT = 'T'
	
	def inference(self, alpha=0.05, two_tailed=True, iterations=-1, force_iterations=False):
		self._check_iterations(iterations, alpha, force_iterations)
		self.permuter.build_pdf(iterations)
		alpha0    = 0.5*alpha if two_tailed else alpha
		zstar     = self.permuter.get_z_critical(alpha0, two_tailed)
		p         = self.permuter.get_p_value(self.z, zstar, alpha)
		return SnPM0Dinference(self, alpha, zstar, p, two_tailed)

class SnPM0D_F(_SnPM0D, _SPMF):
	STAT = 'F'
	
	def _repr_summ(self):
		return '{:<5} F = {:<8}\n'.format(self.effect_short,  '%.3f'%self.z)
	
class SnPM0D_X2(_SnPM0D):
	STAT = 'X2'
class SnPM0D_T2(_SnPM0D):
	STAT = 'T2'
# class SnPM0D_Flist(_SnPM0Dlist):
# 	STAT = 'F'





class SnPM0Dinference(_SnPM0D):
	def __init__(self, spm, alpha, zstar, p, two_tailed=False, isinlist=False):
		super(SnPM0Dinference, self).__init__(spm.z, spm.permuter, isinlist=isinlist)
		self.STAT           = spm.STAT
		self.PDF            = None if isinlist else self.permuter.Z       #permutation PDF
		self.alpha          = alpha                 #Type I error rate
		self.nPerm          = None if isinlist else self.permuter.Z.size  #number of permutations
		self.p              = p                     #P values for each cluster
		self.two_tailed     = two_tailed            #two-tailed test boolean
		self.h0reject       = None                  #null rejection decision
		self.zstar          = zstar                 #critical threshold
		self._check_null()
		
	def __repr__(self):
		stat     = self.STAT
		if stat == 'T':
			stat = 't'
		s        = ''
		s       += 'SnPM{%s} inference field\n' %stat
		s       += '   SPM.z              :  %.3f\n' %self.z
		s       += '   SnPM.nPermUnique   :  %s\n'   %self.get_nPermUnique_asstr()
		s       += 'Inference:\n'
		if not self.isinlist:
			s   += '   SnPM.nPermActual   :  %d actual permutations\n' %self.nPerm
		s       += '   SPM.alpha          :  %.3f\n' %self.alpha
		if self.two_tailed:
			s   += '   SPM.zstar (lower)  :  %.5f\n' %self.zstar[0]
			s   += '   SPM.zstar (upper)  :  %.5f\n' %self.zstar[1]
		else:
			s   += '   SPM.zstar          :  %.5f\n' %self.zstar
		if self.STAT == 'T':
			s   += '   SPM.two_tailed     :  %s\n'   %str(self.two_tailed)
		s       += '   SPM.h0reject       :  %s\n'   %str(self.h0reject)
		s       += '   SPM.p              :  %s\n' %p2string(self.p)
		return s


	def _check_null(self):
		if self.two_tailed:
			zc0,zc1         = self.zstar
			h0              = (self.z < zc0) or (self.z > zc1)
		else:
			h0              = self.z > self.zstar
		self.h0reject       = h0




class SnPM0DiF(SnPM0Dinference, _SPMF):
	def _repr_summ(self):
		return '{:<5} F = {:<8} p = {}\n'.format(self.effect.split(' ')[1],  '%.3f'%self.z, p2string(self.p))
	









'''
################################
   1D SnPM CLASS DEFINITIONS
################################
'''

class _SnPM1D(_SnPM, _spm._SPM):
	
	dim           = 1
	
	'''Parent class for all 1D non-parametric SPM classes.'''
	def __init__(self, z, perm):
		z[np.isnan(z)]      = 0
		self.permuter       = perm             #permuter (for conducting inference)
		self.Q              = z.size           #field size
		self.nPermUnique    = perm.nPermTotal  #number of unique permutations possible
		self.roi            = perm.roi         #region(s) of interest
		self.z              = z                #test statistic
		self._ClusterClass  = ClusterNonparam



	def __repr__(self):
		stat     = self.STAT
		if stat == 'T':
			stat = 't'
		s        = ''
		s       += 'SnPM{%s}\n' %stat
		s       += '   SnPM.z           :  (1x%d) test stat field\n' %self.Q
		s       += '   SnPM.nPermUnique :  %s\n' %self.get_nPermUnique_asstr()
		return s


	def _cluster_inference(self, clusters, two_tailed=False):
		for cluster in clusters:
			cluster.inference(self.permuter.Z2, two_tailed)
		return clusters

	def _get_clusters(self, zstar, two_tailed, interp, circular, iterations, cluster_metric, z=None):
		clusters      = super(_SnPM1D, self)._get_clusters(zstar, two_tailed, interp, circular, z=z)
		metric        = metric_dict[cluster_metric]
		for c in clusters:
			c.set_metric(metric, iterations, self.nPermUnique, two_tailed)
		return clusters
	
	def inference(self, alpha=0.05, iterations=-1, two_tailed=False, interp=True, circular=False, force_iterations=False, cluster_metric='MaxClusterIntegral'):
		self._check_iterations(iterations, alpha, force_iterations)
		### build primary PDF:
		self.permuter.build_pdf(iterations)
		### compute critical threshold:
		a          = 0.5*alpha if two_tailed else alpha  #adjusted alpha (if two-tailed)
		zstar      = self.permuter.get_z_critical(a, two_tailed)
		zstar      = zstar[1] if np.size([zstar])==2 else zstar
		### build secondary PDF:
		self.permuter.set_metric( cluster_metric )
		self.permuter.build_secondary_pdf( zstar, circular )
		### assemble clusters and conduct cluster-level inference:
		clusters   = self._get_clusters(zstar, two_tailed, interp, circular, iterations, cluster_metric)
		clusters   = self._cluster_inference(clusters, two_tailed)
		return SnPMinference(self, alpha, zstar, two_tailed, clusters)

	def plot_design(self, **kwdargs):
		msg        = '\n'
		msg       += 'The "plot_design" method is not implemented for non-parametric SPMs. '
		msg       += 'To plot the design matrix use the corresponding parametric procedure and then call "plot_design".\n'
		msg       += 'For example:\n'
		msg       += '   >>>  spm = spm1d.stats.ttest2(yA, yB)\n' 
		msg       += '   >>>  spm.plot_design()\n\n' 
		raise( NotImplementedError(msg) )


class _SnPM1Donetailed(_SnPM1D):
	def inference(self, alpha=0.05, iterations=-1, interp=True, circular=False, force_iterations=False, cluster_metric='MaxClusterIntegral'):
		return super(_SnPM1Donetailed, self).inference(alpha=alpha, iterations=iterations, two_tailed=False, interp=interp, circular=circular, force_iterations=force_iterations, cluster_metric=cluster_metric)



class _SnPM1Dlist(_SnPM1D):
	# def __init__(self, z, perm):
	# 	self.permuter       = perm             #permuter (for conducting inference)
	# 	self.nPermUnique    = perm.nPermTotal  #number of unique permutations possible
	# 	self.z              = z                #test statistic

	def __repr__(self):
		stat     = self.STAT
		zs       = ''
		for zz in self.z:
			zs  += '%.3f, ' %zz
		zs       = zs[:-2]
		nPermU   = 'inf' if (self.nPermUnique==-1) else str(self.nPermUnique)
		s        = ''
		s       += 'SnPM{%s}\n' %stat
		s       += '   SPM.z            :  %s\n' %zs
		s       += '   SnPM.nPermUnique :  %s\n' %self.get_nPermUnique_asstr()
		return s

	# def _get_clusters(self, zstar, interp, circular, iterations, cluster_metric):
	# 	clusters      = super(_SnPM1D, self)._get_clusters(zstar, two_tailed, interp, circular)
	# 	metric        = metric_dict[cluster_metric]
	# 	for c in clusters:
	# 		c.set_metric(metric, iterations, self.nPermUnique, two_tailed)
	# 	return clusters


	# def _get_clusters(self, z, zstar, check_neg, interp, circular):
	# 	clusters      = self._cluster_geom(zstar, interp, circular, csign=+1)
	# 	if check_neg:
	# 		clustersn = self._cluster_geom(zstar, interp, circular, csign=-1)
	# 		clusters += clustersn
	# 		if len(clusters) > 1:
	# 			### reorder clusters left-to-right:
	# 			x         = [c.xy[0]  for c in clusters]
	# 			ind       = np.argsort(x).flatten()
	# 			clusters  = np.array(clusters)[ind].tolist()
	# 	return clusters

	def inference(self, alpha=0.05, iterations=-1, interp=True, circular=False, force_iterations=False, cluster_metric='MaxClusterIntegral'):
		self._check_iterations(iterations, alpha, force_iterations)
		self.permuter.build_pdf(iterations)
		### compute critical threshold:
		zstarlist = self.permuter.get_z_critical_list(alpha)
		### build secondary PDFs:
		self.permuter.set_metric( cluster_metric )
		self.permuter.build_secondary_pdfs( zstarlist, circular )
		### assemble clusters and conduct cluster-level inference:
		FF         = []
		two_tailed = False
		for i,(z,zstar) in enumerate( zip(self.z,zstarlist) ):
			clusters   = self._get_clusters(zstar, two_tailed, interp, circular, iterations, cluster_metric, z=z)
		# clusters   = self._cluster_inference(clusters, two_tailed)
		# return SnPMinference(self, alpha, zstar, two_tailed, clusters)
		
		
		
		# plist     = self.permuter.get_p_value_list(self.z, zstarlist, alpha)
		# spmilist  = []
		# for z,zstar,p in zip(self.z, zstarlist, plist):
		# 	spm   = SnPM_F(z, self.permuter)
		# 	spmi  = SnPM0Dinference(spm, alpha, zstar, p)
		# 	spmilist.append( spmi )
		# return spmilist


	# def inference(self, alpha=0.05, iterations=-1, two_tailed=False, interp=True, circular=False, force_iterations=False, cluster_metric='MaxClusterIntegral'):
	# 	self._check_iterations(iterations, alpha, force_iterations)
	# 	### build primary PDF:
	# 	self.permuter.build_pdf(iterations)
	#
	# 	### build secondary PDF:
	# 	self.permuter.set_metric( cluster_metric )
	# 	self.permuter.build_secondary_pdf( zstar, circular )
	# 	### assemble clusters and conduct cluster-level inference:
	# 	clusters   = self._get_clusters(zstar, two_tailed, interp, circular, iterations, cluster_metric)
	# 	clusters   = self._cluster_inference(clusters, two_tailed)
	# 	return SnPMinference(self, alpha, zstar, two_tailed, clusters)


class SnPM_T(_SnPM1D):
	STAT = 'T'
class SnPM_F(_SnPM1Donetailed):
	STAT = 'F'
	isinlist = False

	# def __init__(self, spm, alpha, zstar, p, two_tailed=False, isinlist=False):
	# 	super(SnPM0Dinference, self).__init__(spm.z, spm.permuter, isinlist=isinlist)
	# 	self.STAT           = spm.STAT
	# 	self.PDF            = self.permuter.Z       #permutation PDF
	# 	self.alpha          = alpha                 #Type I error rate
	# 	self.nPerm          = self.permuter.Z.size  #number of permutations
	# 	self.p              = p                     #P values for each cluster
	# 	self.two_tailed     = two_tailed            #two-tailed test boolean
	# 	self.h0reject       = None                  #null rejection decision
	# 	self.zstar          = zstar                 #critical threshold
	# 	self._check_null()


class SnPM_X2(_SnPM1Donetailed):
	STAT = 'X2'
class SnPM_T2(_SnPM1Donetailed):
	STAT = 'T2'
class SnPM_Flist(_SnPM1Dlist):
	STAT = 'F'





class SnPMinference(_SnPM1D, _spm._SPMinference):
	def __init__(self, spm, alpha, zstar, two_tailed, clusters):
		super(SnPMinference, self).__init__(spm.z, spm.permuter)
		self.STAT           = spm.STAT
		self.PDF0           = self.permuter.Z        #primary permutation PDF
		self.PDF1           = self.permuter.Z2       #secondary PDF (cluster-level)
		self.alpha          = alpha               #Type I error rate
		self.clusters       = clusters            #supra-threshold cluster information
		self.nClusters      = len(clusters)         #number of supra-threshold clusters
		self.p              = [c.P for c in clusters]  #P values for each cluster
		self.two_tailed     = two_tailed          #two-tailed test boolean
		self.zstar          = zstar               #critical threshold
		self.h0reject       = self.nClusters > 0  #null hypothesis rejection decision
		self.roi            = spm.roi


	def __repr__(self):
		s        = ''
		s       += 'SnPM{%s} inference field\n' %self.STAT
		s       += '   SPM.z              :  (1x%d) raw test stat field\n' %self.Q
		s       += '   SnPM.nPermUnique   :  %s\n' %self.get_nPermUnique_asstr()
		s       += 'Inference:\n'
		# s       += '   SnPM.nPermActual   :  (%d) actual permutations\n' %self.nPerm0
		s       += '   SPM.alpha          :  %.3f\n' %self.alpha
		s       += '   SPM.zstar          :  %.5f\n' %self.zstar
		# s       += '   SPM.cluster_metric :  %s\n'   %self.cluster_metric
		s       += '   SPM.p              :  (%s)\n' %plist2string(self.p)
		return s
		



