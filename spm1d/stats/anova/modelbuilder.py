

import numpy as np
from matplotlib import pyplot
from contrasts import Contrast,ContrastUnbalanced,CompoundContrast


class ModelBuilder(object):
	def __init__(self, labels=[], labels_subj=[]):
		self.labels  = list(labels)
		self.slabels = list(labels_subj)
		self.n       = len(self.labels)   #number of main factors
		self.nS      = len(self.slabels)  #number of subject factors
		self.ncol    = 0  #number of main columns
		self.ncolS   = 0  #number of subject columns
		self.ncolT   = 0  #total number of columns
		self.colD    = dict(zip(self.labels,  [None]*self.n))
		self.colSD   = dict(zip(self.slabels, [None]*self.nS))
		self.XD      = dict(zip(self.labels,  [None]*self.n))
		self.XSD     = dict(zip(self.slabels, [None]*self.n))


	def add_main_columns(self, label, X):
		self.XD[label]   = X
		i0,n             = self.ncol, X.shape[1]
		self.colD[label] = np.arange(i0, i0+n)
		self.ncol       += n
		self.ncolT      += n



	def add_subj_columns(self, label, X):
		self.XSD[label]   = X
		i0,n              = self.ncolS, X.shape[1]
		self.colSD[label] = np.arange(i0, i0+n)
		self.ncolS       += n
		self.ncolT       += n


	def get_contrast(self, label):
		cols      = self.colD[label]
		n         = len(cols)
		C         = np.zeros( (n,self.ncolT) )
		C[:,cols] = np.eye(n)
		return Contrast(C)

	def get_contrast_compound(self, label, slabel):
		if isinstance(slabel,list):
			return self.get_contrast_compound3(label, slabel)
		cols,scols  = self.colD[label], self.colSD[slabel] + self.ncol
		n,ns        = len(cols), len(scols)
		C,CS        = np.zeros( (n,self.ncolT) ), np.zeros( (ns,self.ncolT) )
		C[:,cols]   = np.eye(n)
		CS[:,scols] = np.eye(ns)
		return CompoundContrast(np.vstack([C,CS]), n)

	def get_contrast_compound3(self, label, slabels):
		slabel0,slabel1    = slabels
		cols,scols0,scols1 = self.colD[label], self.colSD[slabel0] + self.ncol, self.colSD[slabel1] + self.ncol
		n,ns0,ns1          = len(cols), len(scols0), len(scols1)
		C,CS0,CS1          = np.zeros( (n,self.ncolT) ), np.zeros( (ns0,self.ncolT) ), np.zeros( (ns1,self.ncolT) )
		C[:,cols]          = np.eye(n)
		CS0[:,scols0]      = np.eye(ns0)
		CS1[:,scols1]      = np.eye(ns1)
		CS                 = CS0 + CS1
		return CompoundContrast(np.vstack([C,CS]), n)

	def get_contrast_difference(self, label):
		cols      = self.colD[label]
		n         = len(cols)
		C         = np.zeros( (n-1,self.ncolT) )
		for i in range(n-1):
			i0,i1 = cols[i], cols[i+1]
			C[i,[i0,i1]] = [1,-1]
		return Contrast(C)

	def get_contrast_unbalanced(self, label):
		return ContrastUnbalanced( self.colD[label].tolist()  )
	
	def get_design_matrix(self):
		X   = np.hstack([self.XD[label]  for label in self.labels])
		if self.nS>0:
			XS  = np.hstack([self.XSD[label] for label in self.slabels])
			X   = np.hstack([X,XS])
		return X
		
		


	