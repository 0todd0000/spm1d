
'''
SPM module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)

This module contains class definitions for raw SPMs (raw test statistic continua)
and inference SPMs (thresholded test statistic).
'''

# Copyright (C) 2014  Todd Pataky
# _spm.py version: 0.2.0006 (2014/07/09)


import numpy as np
from scipy import ndimage,optimize,stats
from .. plot import plot_spm, plot_spm_design
from .. plot import plot_spmi, plot_spmi_p_values, plot_spmi_threshold_label
import rft1d



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
	childfn.__func__.__doc__ = docstr


eps    = np.finfo(float).eps   #smallest float, used to avoid divide-by-zero errors






'''
#################
(0)  CLUSTER CLASS DEFINITION
#################
'''
class Cluster(object):
	def __init__(self, m, mr, h, xy, p):
		self.extent  = m       #cluster size (absolute)
		self.extentR = mr      #cluster size (resels)
		self.h       = h       #cluster height (minimum above threshold)
		self.xy      = tuple(xy)      #cluster centroid
		self.P       = p       #probability value (based on h and extentR)
	def __repr__(self):
		s        = ''
		s       += 'Cluster at location: (%.3f, %.3f)\n' %self.xy
		s       += '   extent          :  %d\n' %self.extent
		s       += '   extent (resels) :  %.5f\n' %self.extentR
		s       += '   height (min)    :  %.5f\n' %self.h
		if self.P==None:
			s   += '   P               :  None\n\n'
		else:
			s   += '   P               :  %.5f\n\n' %self.P
		return s





'''
#################
(1)  SPM (0D) CLASS DEFINITIONS
#################
'''



class _SPM0D(object):
	def __init__(self, STAT, z, df):
		self.STAT           = STAT             #test statistic ("T" or "F")
		self.z              = float(z)         #test statistic
		self.df             = df               #degrees of freedom
		self.isanova        = False
		self.isregress      = False

	def __repr__(self):
		stat     = 't' if self.STAT=='T' else self.STAT
		s        = ''
		s       += 'SPM{%s} (0D)\n' %stat
		if self.isanova:
			s   += '   SPM.SS       : (%s,%s)\n' %self.ss
			s   += '   SPM.df       : (%s,%s)\n' %self.df
			s   += '   SPM.MS       : (%s,%s)\n' %self.ms
			s   += '   SPM.z        :  %.5f\n' %self.z
		else:
			s   += '   SPM.z      :  %.5f\n' %self.z
			s   += '   SPM.df     :  %s\n' %dflist2str(self.df)
		if self.isregress:
			s   += '   SPM.r      :  %.5f\n'   %self.r
		s       += '\n'
		return s


class _SPM0Dinference(_SPM0D):
	def __init__(self, spm, alpha, zstar, p, two_tailed=False):
		_SPM0D.__init__(self, spm.STAT, spm.z, spm.df)
		self.alpha       = alpha       #Type I error rate
		self.zstar       = zstar       #critical threshold
		self.h0reject    = abs(spm.z) > zstar if two_tailed else spm.z > zstar
		self.p           = p           #p value
		self.two_tailed  = two_tailed  #two-tailed test boolean
		self.isanova     = spm.isanova
		self.isregress   = spm.isregress
		if self.isanova:
			self.ss      = spm.ss
			self.ms      = spm.ms
		if self.isregress:
			self.r       = spm.r

	def __repr__(self):
		s        = ''
		s       += 'SPM{%s} (0D) inference\n'    %self.STAT
		s       += '   SPM.z        :  %.5f\n'   %self.z
		s       += '   SPM.df       :  %s\n'     %dflist2str(self.df)
		if self.isregress:
			s   += '   SPM.r        :  %.5f\n'   %self.r
		s       += 'Inference:\n'
		s       += '   SPM.alpha    :  %.3f\n'   %self.alpha
		s       += '   SPM.zstar    :  %.5f\n'   %self.zstar
		s       += '   SPM.h0reject :  %s\n'     %self.h0reject
		s       += '   SPM.p        :  %.5f\n'   %self.p
		return s
	


class SPM0D_F(_SPM0D):
	def __init__(self, z, df, ss=(0,0), ms=(0,0), eij=0, X0=None):
		_SPM0D.__init__(self, 'F', z, df)
		self.ss        = tuple( map(float, ss) )
		self.ms        = tuple( map(float, ms) )
		self.eij       = eij
		self.X0        = X0
		self.isanova   = True
	def inference(self, alpha=0.05):
		zstar  = stats.f.isf(alpha, self.df[0], self.df[1])
		p      = stats.f.sf(self.z, self.df[0], self.df[1])
		return SPM0Di_F(self, alpha, zstar, p)




class SPM0D_T(_SPM0D):
	def __init__(self, z, df):
		_SPM0D.__init__(self, 'T', z, df)
	def inference(self, alpha=0.05, two_tailed=True):
		a      = 0.5*alpha if two_tailed else alpha
		zstar  = stats.t.isf(a, self.df[1])
		p      = stats.t.sf( abs(self.z), self.df[1])
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
	def __init__(self, z, df):
		_SPM0D.__init__(self, 'X2', z, df)
	def inference(self, alpha=0.05):
		zstar  = rft1d.chi2.isf0d(alpha, self.df[1])
		p      = rft1d.chi2.sf0d( self.z, self.df[1])
		return SPM0Di_X2(self, alpha, zstar, p)



class SPM0Di_F(_SPM0Dinference):
	'''An SPM{F} (0D) inference object.'''
	pass
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


class _SPM(object):
	'''Parent class for all SPM.'''
	def __init__(self, STAT, z, df, fwhm, resels, X, beta, residuals):
		z[np.isnan(z)]      = 0
		self.STAT           = STAT             #test statistic ("T" or "F")
		self.Q              = z.size           #number of nodes (field size = Q-1)
		self.X              = X                #design matrix
		self.beta           = beta             #fitted parameters
		self.residuals      = residuals        #model residuals
		self.z              = z                #test statistic
		self.df             = df               #degrees of freedom
		self.fwhm           = fwhm             #smoothness
		self.resels         = resels           #resel counts


	def __repr__(self):
		stat     = self.STAT
		if stat == 'T':
			stat = 't'
		s        = ''
		s       += 'SPM{%s}\n' %stat
		s       += '   SPM.z      :  (1x%d) test stat field\n' %self.Q
		s       += '   SPM.df     :  %s\n' %dflist2str(self.df)
		s       += '   SPM.fwhm   :  %.5f\n' %self.fwhm
		s       += '   SPM.resels :  (%d, %.5f)\n\n\n' %tuple(self.resels)
		return s


	def inference(self, alpha=0.05, cluster_size=0, two_tailed=False, interp=True, circular=False, withBonf=True):
		a         = 0.5*alpha if two_tailed else alpha
		if self.STAT == 'T':
			zstar = rft1d.t.isf(a, self.df[1], self.Q, self.fwhm, withBonf=withBonf)
		elif self.STAT == 'F':
			zstar = rft1d.f.isf(a, self.df, self.Q, self.fwhm, withBonf=withBonf)
		elif self.STAT == 'T2':
			zstar = rft1d.T2.isf(a, self.df, self.Q, self.fwhm, withBonf=withBonf)
		elif self.STAT == 'X2':
			zstar = rft1d.chi2.isf(a, self.df[1], self.Q, self.fwhm, withBonf=withBonf)
		### compute suprathreshold cluster characteristics:
		ccalc     = rft1d.geom.ClusterMetricCalculatorInitialized(self.z, zstar, interp=interp, wrap=circular)
		extents,minima,centroids,L = ccalc.get_all()
		signs     = [1]*ccalc.n
		### compute negative cluster characteristics:
		if two_tailed:
			ccalc      = rft1d.geom.ClusterMetricCalculatorInitialized(-self.z, zstar, interp=interp, wrap=circular)
			if ccalc.n > 0:
				extents1,minima1,centroids1,L1 = ccalc.get_all()
				extents   += extents1
				minima    += (-1*np.array(minima1)).tolist()
				centroids += (np.array(centroids1)*[1,-1]).tolist()
				L         += L1
				signs     += [-1]*ccalc.n
		### set-level inference:
		nUpcrossings  = len(extents)
		p_set         = 1.0
		if nUpcrossings>0:
			minextent     = min(extents)/self.fwhm
			if self.STAT == 'T':
				p_set = rft1d.t.p_set(nUpcrossings, minextent, zstar, self.df[1], self.Q, self.fwhm, withBonf=withBonf)
			elif self.STAT == 'F':
				p_set = rft1d.f.p_set(nUpcrossings, minextent, zstar, self.df, self.Q, self.fwhm, withBonf=withBonf)
			elif self.STAT == 'T2':
				p_set = rft1d.T2.p_set(nUpcrossings, minextent, zstar, self.df, self.Q, self.fwhm, withBonf=withBonf)
			elif self.STAT == 'X2':
				p_set = rft1d.chi2.p_set(nUpcrossings, minextent, zstar, self.df[1], self.Q, self.fwhm, withBonf=withBonf)
		### cluster-level inference:
		clusters  = []
		for extent,minimum,centroid,sign in zip(extents, minima, centroids, signs):
			xR    = extent / self.fwhm
			if self.STAT == 'T':
				p = rft1d.t.p_cluster(xR, sign*minimum, self.df[1], self.Q, self.fwhm, withBonf=withBonf)
			elif self.STAT == 'F':
				p = rft1d.f.p_cluster(xR, minimum, self.df, self.Q, self.fwhm, withBonf=withBonf)
			elif self.STAT == 'T2':
				p = rft1d.T2.p_cluster(xR, minimum, self.df, self.Q, self.fwhm, withBonf=withBonf)
			elif self.STAT == 'X2':
				p = rft1d.chi2.p_cluster(xR, minimum, self.df[1], self.Q, self.fwhm, withBonf=withBonf)
			c     = Cluster(extent, xR, minimum, centroid, p)
			clusters.append(c)
		
		### assemble p values:
		nClusters = len(clusters)
		p         = [c.P for c in clusters]
		if self.STAT == 'T':
			return SPMi_T(self, alpha, zstar, nClusters, clusters, L, p_set, p, two_tailed)
		elif self.STAT == 'F':
			return SPMi_F(self, alpha, zstar, nClusters, clusters, L, p_set, p, two_tailed)
		elif self.STAT == 'T2':
			return SPMi_T2(self, alpha, zstar, nClusters, clusters, L, p_set, p, two_tailed)
		elif self.STAT == 'X2':
			return SPMi_X2(self, alpha, zstar, nClusters, clusters, L, p_set, p, two_tailed)
	
	def plot(self, **kwdargs):
		return plot_spm(self, **kwdargs)
		
	def plot_design(self, **kwdargs):
		plot_spm_design(self, **kwdargs)
		
	def toarray(self):
		return self.z.copy()










class SPM_F(_SPM):
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
	def __init__(self, z, df, fwhm, resels, X, beta, residuals, X0=None):
		_SPM.__init__(self, 'F', z, df, fwhm, resels, X, beta, residuals)
		self.X0 = X0
		
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
	def __init__(self, z, df, fwhm, resels, X, beta, residuals):
		_SPM.__init__(self, 'T', z, df, fwhm, resels, X, beta, residuals)
		
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
	def __init__(self, z, df, fwhm, resels, X, beta, residuals):
		super(SPM_T2, self).__init__('T2', z, df, fwhm, resels, X, beta, residuals)
		
	
	# def __repr__(self):
	# 	stat     = 'T2'
	# 	s        = ''
	# 	s       += 'SPM{%s}\n' %stat
	# 	s       += '   SPM.z      :  (1x%d) test stat field\n' %self.Q
	# 	s       += '   SPM.df     :  %s\n' %dflist2str(self.df)
	# 	s       += '   SPM.fwhm   :  %.5f\n' %self.fwhm
	# 	s       += '   SPM.resels :  (%d, %.5f)\n' %tuple(self.resels)
	# 	return s
	


class SPM_X2(_SPM):
	def __init__(self, z, df, fwhm, resels, X, beta, residuals):
		super(SPM_X2, self).__init__('X2', z, df, fwhm, resels, X, beta, residuals)








'''
#################
(2)  SPM INFERENCE CLASS DEFINITIONS
#################
'''


class _SPMinference(_SPM):
	'''Parent class for SPM inference objects.'''
	def __init__(self, spm, alpha, zstar, nClusters, clusters, L, p_set, p, two_tailed=False):
		_SPM.__init__(self, spm.STAT, spm.z, spm.df, spm.fwhm, spm.resels, spm.X, spm.beta, spm.residuals)
		self.alpha       = alpha       #Type I error rate
		self.zstar       = zstar       #critical threshold
		self.h0reject    = nClusters > 0
		self.nClusters   = nClusters   #number of supra-threshold clusters
		self.clusters    = clusters    #supra-threshold cluster information
		self.L           = L           #cluster labels
		self.p_set       = p_set       #set-level p value
		self.p           = p           #P values for each cluster
		self.two_tailed  = two_tailed  #two-tailed test boolean

	def __repr__(self):
		s        = ''
		s       += 'SPM{%s} inference field\n' %self.STAT
		s       += '   SPM.z         :  (1x%d) raw test stat field\n' %self.Q
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
	'''An SPM{T} inference continuum.'''
	pass
class SPMi_F(_SPMinference):
	'''An SPM{F} inference continuum.'''
	pass
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




