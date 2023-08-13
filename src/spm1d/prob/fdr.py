
'''
False discover rate (FDR) probabilities
'''

from copy import deepcopy
import numpy as np
from .. geom import assemble_clusters, ClusterList
eps    = np.finfo(float).eps  #smallest floating number greater than zero



class FDRResults(object):
	
	isparametric      = True
	method            = 'fdr'
	
	def __init__(self, alpha, dirn, zc, clusters, pu, pc):
		self.method        = 'fdr'
		self.alpha         = alpha
		self.dirn          = dirn
		self.zc            = zc
		self.clusters      = clusters
		self.p_set         = None
		self.p_max         = pc.min()
		self.p_uncorrected = pu
		self.p_corrected   = pc
		self.extras        = {}

	def __repr__(self):
		s  = 'FDRResults\n'
		s += '   method = %s\n'   %self.method
		s += '   alpha  = %s\n'   %self.alpha
		s += '   dirn   = %s\n'   %self.dirn
		s += '   zc     = %.5f\n' %self.zc
		s += '   p_mac  = %.5f\n' %self.p_max
		return s



def p_uncorrected(STAT, z, df):
	import rft1d
	if STAT=='T':
		p     = rft1d.t.sf0d(z, df[1])
	elif STAT=='F':
		p     = rft1d.f.sf0d(z, df)
	elif STAT=='T2':
		p     = rft1d.T2.sf0d(z, df)
	elif STAT=='X2':
		p     = rft1d.chi2.sf0d(z, df[1])
	return p



def fdr(STAT, z, df, alpha=0.05, dirn=1, circular=False, approach='bh'):
	'''
	Assumes that z-values and p-values are NOT sorted
	
	Modified from fdr1d.py:
	https://github.com/0todd0000/fdr1d
	
	Corrected p-values follow statsmodels.stats.multitest.fdrcorrection
	The "method" and "pc" parts of the code below are modifed from 
	statsmodels. The statsmodels source code is copied below under "statsmodels_fdrcorrection"
	'''
	if (STAT=='T') and (dirn==0):
		_z,a  = np.abs(z), 0.5 * alpha
	else:
		_z,a  = z, alpha
	
	Q         = z.size
	
		
	# sort p values:
	pu        = p_uncorrected(STAT, _z, df)   # uncorrected p-values
	pu        = (1-pu) if (dirn==-1) else pu
	ind       = np.argsort(pu)
	psorted   = pu[ind]
	
	# empirical CDF
	ec        = (np.arange(Q) + 1) / float(Q)
	if approach=='bh':  # Benjamini/Hochberg for independent or positively correlated tests
		pass
	elif approach=='by':  # Benjamini/Yekutieli for general or negatively correlated tests;  modified from statsmodels.stats.multitest.fdrcorrection
		cm    = np.sum( 1. / np.arange(1, Q+1) )
		ec    = ec / cm
	
	# test statistic threshold
	psortedth = a * ec   # sorted p value threshold:
	b         = psorted < psortedth
	if np.any(b):
		ii    = np.argwhere(b).ravel()[-1]
		zc    = _z[ind][ii] + eps
	else:
		zc    = None

	# corrected p-values (modified from statsmodels.stats.multitest.fdrcorrection):
	pc        = psorted / ec
	pc        = np.minimum.accumulate(  pc[::-1]  )[::-1]
	pc[pc>1]  = 1
	pc_       = np.empty_like(pc)
	pc_[ind]  = pc
	
	# assemble clusters:
	if zc is None:
		clusters = ClusterList([])
	else:
		clusters  = assemble_clusters(z, zc, dirn=dirn, circular=circular)
		for i,c in enumerate( clusters ):
			clusters[i] = c.as_inference_cluster(None, None)

	results   = FDRResults( alpha, dirn, zc, clusters, pu, pc_ )
	return results





# def statsmodels_fdrcorrection(pvals, alpha=0.05, method='indep', is_sorted=False):
# 	'''
# 	Modified from statsmodels.stats.multitest.fdrcorrection
#
# 	Copyright (C) 2006, Jonathan E. Taylor
# 	All rights reserved.
#
# 	Copyright (c) 2006-2008 Scipy Developers.
# 	All rights reserved.
#
# 	Copyright (c) 2009-2018 statsmodels Developers.
# 	All rights reserved.
#
#
# 	Redistribution and use in source and binary forms, with or without
# 	modification, are permitted provided that the following conditions are met:
#
# 	  a. Redistributions of source code must retain the above copyright notice,
# 	     this list of conditions and the following disclaimer.
# 	  b. Redistributions in binary form must reproduce the above copyright
# 	     notice, this list of conditions and the following disclaimer in the
# 	     documentation and/or other materials provided with the distribution.
# 	  c. Neither the name of statsmodels nor the names of its contributors
# 	     may be used to endorse or promote products derived from this software
# 	     without specific prior written permission.
#
#
# 	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# 	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# 	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# 	ARE DISCLAIMED. IN NO EVENT SHALL STATSMODELS OR CONTRIBUTORS BE LIABLE FOR
# 	ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# 	DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# 	SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# 	CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# 	LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# 	OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# 	DAMAGE.
# 	'''
#
# 	def _ecdf(x):  # no frills empirical cdf used in fdrcorrection
# 		n = len(x)
# 		return np.arange(1,n+1) / float(n)
#
# 	pvals = np.asarray(pvals)
# 	assert pvals.ndim == 1, "pvals must be 1-dimensional, that is of shape (n,)"
#
# 	if not is_sorted:
# 		pvals_sortind = np.argsort(pvals)
# 		pvals_sorted = np.take(pvals, pvals_sortind)
# 	else:
# 		pvals_sorted = pvals  # alias
#
# 	if method in ['i', 'indep', 'p', 'poscorr']:
# 		ecdffactor = _ecdf(pvals_sorted)
# 	elif method in ['n', 'negcorr']:
# 		cm = np.sum(1./np.arange(1, len(pvals_sorted)+1))   #corrected this
# 		ecdffactor = _ecdf(pvals_sorted) / cm
# 	##    elif method in ['n', 'negcorr']:
# 	##        cm = np.sum(np.arange(len(pvals)))
# 	##        ecdffactor = ecdf(pvals_sorted)/cm
# 	else:
# 		raise ValueError('only indep and negcorr implemented')
# 	reject = pvals_sorted <= ecdffactor*alpha
# 	if reject.any():
# 		rejectmax = max(np.nonzero(reject)[0])
# 		reject[:rejectmax] = True
#
# 	pvals_corrected_raw = pvals_sorted / ecdffactor
# 	pvals_corrected = np.minimum.accumulate(pvals_corrected_raw[::-1])[::-1]
# 	del pvals_corrected_raw
# 	pvals_corrected[pvals_corrected>1] = 1
# 	if not is_sorted:
# 		pvals_corrected_ = np.empty_like(pvals_corrected)
# 		pvals_corrected_[pvals_sortind] = pvals_corrected
# 		del pvals_corrected
# 		reject_ = np.empty_like(reject)
# 		reject_[pvals_sortind] = reject
# 		return reject_, pvals_corrected_
# 	else:
# 		return reject, pvals_corrected


