

import numpy as np
from matplotlib import pyplot




class Contrast(object):
	def __init__(self, C):
		self.C          = np.matrix(C)     #contrast matrix
		self.isrm       = False            #repeated measures flag
		self.isub       = False            #unbalanced flag

	def plot(self, ax=None):
		ax  = pyplot.gca() if ax==None else ax
		ax.imshow(self.C, interpolation='nearest', cmap='gray', vmin=-1, vmax=1, aspect='auto')
		xskip   = self.C.shape[1] / 10 + 1
		yskip   = self.C.shape[0] / 10 + 1
		pyplot.setp(ax, xticks=range(0, self.C.shape[1], xskip), yticks=range(0, self.C.shape[0], yskip))


class ContrastUnbalanced(Contrast):
	def __init__(self, C):
		self.C          = C                #list of columns for unbalanced regression
		self.isub       = True             #repeated measures flag
	def plot(self):
		pass


class CompoundContrast(Contrast):
	def __init__(self, C, n):
		self.C          = np.matrix(C)     #contrast matrix
		self.isrm       = True             #repeated measures flag
		self.n          = int(n)
	
	def get_compound_matrices(self):
		return self.C, self.C[self.n:]
	

