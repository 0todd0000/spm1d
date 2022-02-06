
'''
SPM module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
'''

# Copyright (C) 2022  Todd Pataky


import sys
import numpy as np
from scipy import stats
from .. import rft1d
from .. plot import plot_spm, plot_spm_design
from .. plot import plot_spmi, plot_spmi_p_values, plot_spmi_threshold_label
from . _clusters import Cluster



def df2str(df):
	return str(df) if not df%1 else '%.3f'%df
def dflist2str(dfs):
	return '(%s, %s)' %(df2str(dfs[0]), df2str(dfs[1]))
def p2string(p):
	return '<0.001' if p<0.0005 else '%.03f'%p
def plist2string(pList):
	s      = ''
	if len(pList)>0:
		for p in pList:
			s += p2string(p)
			s += ', '
		s  = s[:-2]
	return s
def _set_docstr(childfn, parentfn, args2remove=None):
	docstr      =  parentfn.__doc__
	if args2remove!=None:
		docstrlist0 = docstr.split('\n\t')
		docstrlist1 = []
		for s in docstrlist0:
			if not np.any([s.startswith('- *%s*'%argname) for argname in args2remove]):
				docstrlist1.append(s)
		docstrlist1 = [s + '\n\t'  for s in docstrlist1]
		docstr  = ''.join(docstrlist1)
	if sys.version_info.major==2:
		childfn.__func__.__doc__ = docstr
	elif sys.version_info.major==3:
		childfn.__doc__ = docstr







class _SPMParent(object):
	'''Parent class for all parametric SPM classes.'''
	isanova       = False
	isinference   = False
	isregress     = False
	isparametric  = True
	dim           = 0



class _SPMF(object):
	'''Additional attrubutes and methods specific to SPM{F} objects.'''
	effect        = 'Main A'
	effect_short  = 'A'
	isanova       = True
	def set_effect_label(self, label=""):
		self.effect        = str(label)
		self.effect_short  = self.effect.split(' ')[1]







'''
#################
(1)  SPM (0D) CLASS DEFINITIONS
#################
'''



class _SPM0D(_SPMParent):
	def __init__(self, STAT, z, df, beta=None, residuals=None, sigma2=None):
		self.STAT           = STAT             #test statistic ("T" or "F")
		self.z              = float(z)         #test statistic
		self.df             = df               #degrees of freedom
		self.beta           = beta             #fitted parameters
		self.residuals      = residuals        #model residuals
		self.sigma2         = sigma2           #variance


	def __repr__(self):
		stat     = 't' if self.STAT=='T' else self.STAT
		s        = ''
		s       += 'SPM{%s} (0D)\n' %stat
		if self.isanova:
			s   += '   SPM.effect   :  %s\n'      %self.effect
			s   += '   SPM.SS       : (%s, %s)\n' %self.ss
			s   += '   SPM.df       : (%s, %s)\n' %self.df
			s   += '   SPM.MS       : (%s, %s)\n' %self.ms
			s   += '   SPM.z        :  %.5f\n'    %self.z
		else:
			s   += '   SPM.z      :  %.5f\n'      %self.z
			s   += '   SPM.df     :  %s\n'        %dflist2str(self.df)
		if self.isregress:
			s   += '   SPM.r      :  %.5f\n'      %self.r
		s       += '\n'
		return s


class _SPM0Dinference(_SPM0D):
	
	isinference = True
	
	def __init__(self, spm, alpha, zstar, p, two_tailed=False):
		_SPM0D.__init__(self, spm.STAT, spm.z, spm.df, beta=spm.beta, residuals=spm.residuals, sigma2=spm.sigma2)
		self.alpha       = alpha       #Type I error rate
		self.zstar       = zstar       #critical threshold
		self.h0reject    = abs(spm.z) > zstar if two_tailed else spm.z > zstar
		self.p           = p           #p value
		self.two_tailed  = two_tailed  #two-tailed test boolean
		self.isanova     = spm.isanova
		self.isregress   = spm.isregress
		if self.isanova:
			self.set_effect_label( spm.effect )
			self.ss      = spm.ss
			self.ms      = spm.ms
		if self.isregress:
			self.r       = spm.r

	def __repr__(self):
		s        = ''
		s       += 'SPM{%s} (0D) inference\n'     %self.STAT
		if self.isanova:
			s   += '   SPM.effect   :  %s\n'      %self.effect
			s   += '   SPM.SS       : (%s, %s)\n' %self.ss
			s   += '   SPM.df       : (%s, %s)\n' %self.df
			s   += '   SPM.MS       : (%s, %s)\n' %self.ms
			s   += '   SPM.z        :  %.5f\n'    %self.z
		else:
			s   += '   SPM.z        :  %.5f\n'    %self.z
			s   += '   SPM.df       :  %s\n'      %dflist2str(self.df)
		if self.isregress:
			s   += '   SPM.r        :  %.5f\n'    %self.r
		s       += 'Inference:\n'
		s       += '   SPM.alpha    :  %.3f\n'    %self.alpha
		s       += '   SPM.zstar    :  %.5f\n'    %self.zstar
		s       += '   SPM.h0reject :  %s\n'      %self.h0reject
		s       += '   SPM.p        :  %.5f\n'    %self.p
		s       += '\n'
		return s
	



class SPM0D_F(_SPMF, _SPM0D):
	def __init__(self, z, df, ss=(0,0), ms=(0,0), eij=0, X0=None):
		_SPM0D.__init__(self, 'F', z, df)
		self.ss        = tuple( map(float, ss) )
		self.ms        = tuple( map(float, ms) )
		self.eij       = eij
		self.residuals = np.asarray(eij).flatten()
		self.X0        = X0

	def _repr_summ(self):
		return '{:<5} F = {:<8} df = {}\n'.format(self.effect_short,  '%.3f'%self.z, dflist2str(self.df))

	def inference(self, alpha=0.05):
		zstar  = stats.f.isf(alpha, self.df[0], self.df[1])
		p      = stats.f.sf(self.z, self.df[0], self.df[1])
		return SPM0Di_F(self, alpha, zstar, p)




class SPM0D_T(_SPM0D):
	def __init__(self, z, df, beta=None, residuals=None, sigma2=None):
		_SPM0D.__init__(self, 'T', z, df, beta=beta, residuals=residuals, sigma2=sigma2)
	def inference(self, alpha=0.05, two_tailed=True):
		a      = 0.5*alpha if two_tailed else alpha
		z      = abs(self.z) if two_tailed else self.z
		zstar  = stats.t.isf(a, self.df[1])
		p      = stats.t.sf( z, self.df[1])
		p      = min(1, 2*p) if two_tailed else p
		return SPM0Di_T(self, alpha, zstar, p, two_tailed)

class SPM0D_T2(_SPM0D):
	def __init__(self, z, df):
		_SPM0D.__init__(self, 'T2', z, df)
	def inference(self, alpha=0.05):
		zstar  = rft1d.T2.isf0d(alpha, self.df)
		p      = rft1d.T2.sf0d( self.z, self.df)
		return SPM0Di_T2(self, alpha, zstar, p)

class SPM0D_X2(_SPM0D):
	def __init__(self, z, df, residuals=None):
		_SPM0D.__init__(self, 'X2', z, df, residuals=residuals)
	def inference(self, alpha=0.05):
		zstar  = rft1d.chi2.isf0d(alpha, self.df[1])
		p      = rft1d.chi2.sf0d( self.z, self.df[1])
		return SPM0Di_X2(self, alpha, zstar, p)



class SPM0Di_F(_SPMF, _SPM0Dinference):
	'''An SPM{F} (0D) inference object.'''
	def _repr_summ(self):
		return '{:<5} F = {:<8} df = {:<9} p = {}\n'.format(self.effect.split(' ')[1],  '%.3f'%self.z, dflist2str(self.df), p2string(self.p))
class SPM0Di_T(_SPM0Dinference):
	'''An SPM{T} (0D) inference object.'''
	pass
class SPM0Di_T2(_SPM0Dinference):
	'''An SPM{T2} (0D) inference object.'''
	pass
class SPM0Di_X2(_SPM0Dinference):
	'''An SPM{X2} (0D) inference object.'''
	pass






'''
#################
(3)  SPM CLASS DEFINITIONS
#################
'''


class _SPM(_SPMParent):
	dim                     = 1
	'''Parent class for all 1D SPM classes.'''
	def __init__(self, STAT, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
		# z[np.isnan(z)]      = 0              #this produces a MaskedArrayFutureWarning in Python 3.X
		self.STAT           = STAT             #test statistic ("T" or "F")
		self.Q              = z.size           #number of nodes (field size = Q-1)
		self.Qmasked        = z.size           #number of nodes in mask (if "roi" is not None)
		self.X              = X                #design matrix
		self.beta           = beta             #fitted parameters
		self.residuals      = residuals        #model residuals
		self.sigma2         = sigma2           #variance
		self.z              = z                #test statistic
		self.df             = df               #degrees of freedom
		self.fwhm           = fwhm             #smoothness
		self.resels         = resels           #resel counts
		self.roi            = roi              #region of interest
		self._ClusterClass  = Cluster          #class definition for parametric / non-parametric clusters
		if roi is not None:
			self.Qmasked    = self.z.count()


	def __repr__(self):
		stat     = self.STAT
		if stat == 'T':
			stat = 't'
		s        = ''
		s       += 'SPM{%s}\n' %stat
		if self.isanova:
			s   += '   SPM.effect :   %s\n' %self.effect
		s       += '   SPM.z      :  %s\n' %self._repr_teststat()
		if self.isregress:
			s   += '   SPM.r      :  %s\n' %self._repr_corrcoeff()
		s       += '   SPM.df     :  %s\n' %dflist2str(self.df)
		s       += '   SPM.fwhm   :  %.5f\n' %self.fwhm
		s       += '   SPM.resels :  (%d, %.5f)\n\n\n' %tuple(self.resels)
		return s
	
	@property
	def R(self):
		return self.residuals
	@property
	def nNodes(self):
		return self.Q
	
	
	def _repr_corrcoeff(self):
		return '(1x%d) correlation coefficient field' %self.Q
	def _repr_teststat(self):
		return '(1x%d) test stat field' %self.Q
	def _repr_teststat_short(self):
		return '(1x%d) array' %self.Q
		# return '(1x%d) %s field' %(self.Q, self.STAT)
	

	def _build_spmi(self, alpha, zstar, clusters, p_set, two_tailed):
		p_clusters  = [c.P for c in clusters]
		if self.STAT == 'T':
			spmi    = SPMi_T(self, alpha,  zstar, clusters, p_set, p_clusters, two_tailed)
		elif self.STAT == 'F':
			spmi    = SPMi_F(self, alpha,  zstar, clusters, p_set, p_clusters, two_tailed)
		elif self.STAT == 'T2':
			spmi    = SPMi_T2(self, alpha, zstar, clusters, p_set, p_clusters, two_tailed)
		elif self.STAT == 'X2':
			spmi    = SPMi_X2(self, alpha, zstar, clusters, p_set, p_clusters, two_tailed)
		return spmi
		
	def _cluster_geom(self, u, interp, circular, csign=+1, z=None):
		Q        = self.Q
		Z        = self.z if z is None else z
		X        = np.arange(Q)
		if np.ma.is_masked(Z):
			i    = Z.mask
			Z    = np.array(Z)
			B    = (csign*Z) >= u
			B[i] = False
			Z[i] = np.nan
		else:
			B    = (csign*Z) >= u
		Z        = csign*Z
		L,n      = rft1d.geom.bwlabel(B)
		clusters = []
		for i in range(n):
			b    = L==(i+1)
			x,z  = X[b].tolist(), Z[b].tolist()
			# interpolate to threshold u using similar triangles method
			# (interpolate for plotting whether or not "interp" is true)
			if (x[0]>0) and not np.isnan( Z[x[0]-1] ):  #first cluster point not continuum edge && previous point not outside ROI
				z0,z1  = Z[x[0]-1], Z[x[0]]
				dx     = (z1-u) / (z1-z0)
				x      = [x[0]-dx] + x
				z      = [u] +z
			if (x[-1]<Q-1) and not np.isnan( Z[x[-1]+1] ):  #last cluster point not continuum edge && next point not outside ROI
				z0,z1  = Z[x[-1]], Z[x[-1]+1]
				dx     = (z0-u) / (z0-z1)
				x     += [x[-1]+dx]
				z     += [u]
			# create cluster:
			x,z  = np.array(x), csign*np.array(z)
			clusters.append(  self._ClusterClass(x, z, csign*u, interp) )
		#merge clusters if necessary (circular fields only)
		if circular and (clusters!=[]):
			xy         = np.array([c.endpoints  for c in clusters])
			i0,i1      = xy[:,0]==0, xy[:,1]==Q-1
			ind0,ind1  = np.argwhere(i0), np.argwhere(i1)
			if (len(ind0)>0) and (len(ind1)>0):
				ind0,ind1 = ind0[0][0], ind1[0][0]
				if (ind0!=ind1) and (clusters[ind0].csign == clusters[ind1].csign):
					clusters[ind0].merge( clusters[ind1] )
					clusters.pop( ind1 )
		return clusters
	
	def _cluster_inference(self, clusters, two_tailed, withBonf):
		for cluster in clusters:
			cluster.inference(self.STAT, self.df, self.fwhm, self.resels, two_tailed, withBonf, self.Q)
		return clusters

	def _get_clusters(self, zstar, check_neg, interp, circular, z=None):
		clusters      = self._cluster_geom(zstar, interp, circular, csign=+1, z=z)
		if check_neg:
			clustersn = self._cluster_geom(zstar, interp, circular, csign=-1, z=z)
			clusters += clustersn
			if len(clusters) > 1:
				### reorder clusters left-to-right:
				x         = [c.xy[0]  for c in clusters]
				ind       = np.argsort(x).flatten()
				clusters  = np.array(clusters)[ind].tolist()
		return clusters

	def _isf(self, a, withBonf):   #Inverse survival function (random field theory)
		if self.STAT == 'T':
			zstar = rft1d.t.isf_resels(a, self.df[1], self.resels, withBonf=withBonf, nNodes=self.Q)
		elif self.STAT == 'F':
			zstar = rft1d.f.isf_resels(a, self.df, self.resels, withBonf=withBonf, nNodes=self.Q)
		elif self.STAT == 'T2':
			zstar = rft1d.T2.isf_resels(a, self.df, self.resels, withBonf=withBonf, nNodes=self.Q)
		elif self.STAT == 'X2':
			zstar = rft1d.chi2.isf_resels(a, self.df[1], self.resels, withBonf=withBonf, nNodes=self.Q)
		return zstar

	def _setlevel_inference(self, zstar, clusters, two_tailed, withBonf):
		nUpcrossings  = len(clusters)
		p_set         = 1.0
		if nUpcrossings>0:
			extents       = [c.extentR for c in clusters]
			minextent     = min(extents)
			if self.STAT == 'T':
				p_set = rft1d.t.p_set_resels(nUpcrossings, minextent, zstar, self.df[1], self.resels, withBonf=withBonf, nNodes=self.Q)
				p_set = min(1, 2*p_set) if two_tailed else p_set
			elif self.STAT == 'F':
				p_set = rft1d.f.p_set_resels(nUpcrossings, minextent, zstar, self.df, self.resels, withBonf=withBonf, nNodes=self.Q)
			elif self.STAT == 'T2':
				p_set = rft1d.T2.p_set_resels(nUpcrossings, minextent, zstar, self.df, self.resels, withBonf=withBonf, nNodes=self.Q)
			elif self.STAT == 'X2':
				p_set = rft1d.chi2.p_set_resels(nUpcrossings, minextent, zstar, self.df[1], self.resels, withBonf=withBonf, nNodes=self.Q)
		return p_set
	
	def inference(self, alpha=0.05, cluster_size=0, two_tailed=False, interp=True, circular=False, withBonf=True):
		check_neg  = two_tailed
		### check ROI and "two_tailed" compatability:
		if self.roi is not None:
			if self.roi.dtype != bool:
				if two_tailed:
					raise( ValueError('If the ROI contains directional predictions two_tailed must be FALSE.') )
				else:
					check_neg  = np.any( self.roi == -1 )
		### conduct inference:
		a          = 0.5*alpha if two_tailed else alpha  #adjusted alpha (if two-tailed)
		zstar      = self._isf(a, withBonf)  #critical threshold (RFT inverse survival function)
		clusters   = self._get_clusters(zstar, check_neg, interp, circular)  #assemble all suprathreshold clusters
		clusters   = self._cluster_inference(clusters, two_tailed, withBonf)  #conduct cluster-level inference
		p_set      = self._setlevel_inference(zstar, clusters, two_tailed, withBonf)  #conduct set-level inference
		spmi       = self._build_spmi(alpha, zstar, clusters, p_set, two_tailed)    #assemble SPMi object
		return spmi

	def plot(self, **kwdargs):
		return plot_spm(self, **kwdargs)
		
	def plot_design(self, **kwdargs):
		plot_spm_design(self, **kwdargs)
		
	def toarray(self):
		return self.z.copy()










class SPM_F(_SPMF, _SPM):
	'''
	Create an SPM{F} continuum.
	SPM objects are instantiated in the **spm1d.stats** module.
	
	:Parameters:
	
	y : the SPM{F} continuum
	
	fwhm: estimated field smoothness (full-width at half-maximium)
	
	df : 2-tuple specifying the degrees of freedom (interest,error)
	
	resels : 2-tuple specifying the resel counts
	
	X : experimental design matrix
	
	beta : array of fitted model parameters
	
	residuals : array of residuals (used for smoothness estimation)
	
	:Returns:
	
	A **spm1d._spm.SPM_F** instance.
	
	:Methods:
	'''
	def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, X0=None, sigma2=None, roi=None):
		_SPM.__init__(self, 'F', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)
		self.X0 = X0
		
	def _repr_summ(self):
		return '{:<5} z = {:<18} df = {}\n'.format(self.effect_short,  self._repr_teststat_short(), dflist2str(self.df))

	def inference(self, alpha=0.05, cluster_size=0, interp=True, circular=False):
		'''
		Conduct statistical inference using random field theory.
		
		:Parameters:
		
		alpha        : Type I error rate (default: 0.05)
		
		cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
		:Returns:
		
		A **spm1d._spm.SPMi_F** instance.
		'''
		return _SPM.inference(self, alpha, cluster_size, two_tailed=False, interp=interp, circular=circular)



class SPM_T(_SPM):
	'''
	Create an SPM{T} continuum.
	SPM objects are instantiated in the **spm1d.stats** module.
	
	:Parameters:
	
	y : the SPM{T} continuum
	
	fwhm: estimated field smoothness (full-width at half-maximium)
	
	df : a 2-tuple specifying the degrees of freedom (interest,error)
	
	resels : a 2-tuple specifying the resel counts
	
	X : experimental design matrix
	
	beta : array of fitted model parameters
	
	residuals : array of residuals (used for smoothness estimation)
	
	:Returns:
	
	A **spm1d._spm.SPM_t** instance.
	
	:Methods:
	'''
	def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
		_SPM.__init__(self, 'T', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)
		
	def inference(self, alpha=0.05, cluster_size=0, two_tailed=True, interp=True, circular=False):
		'''
		Conduct statistical inference using random field theory.
		
		:Parameters:
		
		alpha        : Type I error rate (default: 0.05)
		
		cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
		
		two_tailed   : Conduct two-tailed inference (default: False)
		
		:Returns:
		
		A **spm1d._spm.SPMi_T** instance.
		'''
		return _SPM.inference(self, alpha, cluster_size, two_tailed, interp, circular)




class SPM_T2(_SPM):
	def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
		super(SPM_T2, self).__init__('T2', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)
		
	def inference(self, alpha=0.05, cluster_size=0, interp=True, circular=False):
		'''
		Conduct statistical inference using random field theory.
		
		:Parameters:
		
		alpha        : Type I error rate (default: 0.05)
		
		cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
		:Returns:
		
		A **spm1d._spm.SPMi_F** instance.
		'''
		return _SPM.inference(self, alpha, cluster_size, two_tailed=False, interp=interp, circular=circular)
	


class SPM_X2(_SPM):
	def __init__(self, z, df, fwhm, resels, X=None, beta=None, residuals=None, sigma2=None, roi=None):
		super(SPM_X2, self).__init__('X2', z, df, fwhm, resels, X, beta, residuals, sigma2=sigma2, roi=roi)

	def inference(self, alpha=0.05, cluster_size=0, interp=True, circular=False):
		'''
		Conduct statistical inference using random field theory.
		
		:Parameters:
		
		alpha        : Type I error rate (default: 0.05)
		
		cluster_size : Minimum cluster size of interest (default: 0), smaller clusters will be ignored
		:Returns:
		
		A **spm1d._spm.SPMi_F** instance.
		'''
		return _SPM.inference(self, alpha, cluster_size, two_tailed=False, interp=interp, circular=circular)








'''
#################
(2)  SPM INFERENCE CLASS DEFINITIONS
#################
'''


class _SPMinference(_SPM):
	'''Parent class for SPM inference objects.'''
	
	isinference = True
	
	def __init__(self, spm, alpha, zstar, clusters, p_set, p, two_tailed=False):
		_SPM.__init__(self, spm.STAT, spm.z, spm.df, spm.fwhm, spm.resels, X=spm.X, beta=spm.beta, residuals=spm.residuals, sigma2=spm.sigma2, roi=spm.roi)
		self.alpha       = alpha               #Type I error rate
		self.zstar       = zstar               #critical threshold
		self.clusters    = clusters            #supra-threshold cluster information
		self.isregress   = spm.isregress       #propagate regression flag
		self.nClusters   = len(clusters)       #number of supra-threshold clusters
		self.h0reject    = self.nClusters > 0  #null hypothesis rejection decision
		self.p_set       = p_set               #set-level p value
		self.p           = p                   #cluster-level p values
		self.two_tailed  = two_tailed          #two-tailed test boolean
		if self.isregress:
			self.r       = spm.r
		if self.isanova:
			self.set_effect_label( spm.effect )

	def __repr__(self):
		stat     = 't' if self.STAT == 'T' else self.STAT
		s        = ''
		s       += 'SPM{%s} inference field\n' %stat
		if self.isanova:
			s   += '   SPM.effect    :   %s\n' %self.effect
		s       += '   SPM.z         :  (1x%d) raw test stat field\n' %self.Q
		if self.isregress:
			s   += '   SPM.r         :  %s\n' %self._repr_corrcoeff()
		s       += '   SPM.df        :  %s\n' %dflist2str(self.df)
		s       += '   SPM.fwhm      :  %.5f\n' %self.fwhm
		s       += '   SPM.resels    :  (%d, %.5f)\n' %tuple(self.resels)
		s       += 'Inference:\n'
		s       += '   SPM.alpha     :  %.3f\n' %self.alpha
		s       += '   SPM.zstar     :  %.5f\n' %self.zstar
		s       += '   SPM.h0reject  :  %s\n' %self.h0reject
		s       += '   SPM.p_set     :  %s\n' %p2string(self.p_set)
		s       += '   SPM.p_cluster :  (%s)\n\n\n' %plist2string(self.p)
		return s
	
	def plot(self, **kwdargs):
		return plot_spmi(self, **kwdargs)

	def plot_p_values(self, **kwdargs):
		plot_spmi_p_values(self, **kwdargs)
	
	def plot_threshold_label(self, **kwdargs):
		return plot_spmi_threshold_label(self, **kwdargs)
	
	





class SPMi_T(_SPMinference):
	'''An SPM{t} inference continuum.'''
	pass
class SPMi_F(_SPMF, _SPMinference):
	'''An SPM{F} inference continuum.'''
	def _repr_summ(self):
		return '{:<5} z={:<18} df={:<9} h0reject={}\n'.format(self.effect_short,  self._repr_teststat_short(), dflist2str(self.df), self.h0reject)
	
class SPMi_T2(_SPMinference):
	'''An SPM{T2} inference continuum.'''
	pass
class SPMi_X2(_SPMinference):
	'''An SPM{X2} inference continuum.'''
	pass




#set docstrings:
_set_docstr(_SPM.plot, plot_spm, args2remove=['spm'])
_set_docstr(_SPMinference.plot, plot_spmi, args2remove=['spmi'])
_set_docstr(_SPMinference.plot_p_values, plot_spmi_p_values, args2remove=['spmi'])
_set_docstr(_SPMinference.plot_threshold_label, plot_spmi_threshold_label, args2remove=['spmi'])




