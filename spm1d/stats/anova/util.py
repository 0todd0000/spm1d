
import numpy as np


def flatten0d(Y):
	y   = np.hstack(Y.T)
	A   = np.hstack(  [ [i]*Y.shape[0] for i in range(Y.shape[1]) ]  )
	return y,A
	
def flatten0d_rm(Y):
	y    = np.hstack(Y.T)
	# A    = np.hstack(  [ [i]*Y.shape[0] for i in range(Y.shape[1]) ]  )
	A    = np.hstack(  range(Y.shape[1])*Y.shape[0]  )
	SUBJ = np.hstack(  [ [i]*Y.shape[1] for i in range(Y.shape[0]) ]  )
	return y,A,SUBJ

def flatten0d_ub(Y):
	A   = np.hstack(  [ [i]*y.size for i,y in enumerate(Y) ]  )
	y   = np.hstack(Y.T)
	return y,A


def stack1d(YY):
	Y   = np.vstack(YY)
	# nA  = len(YY)
	# nnA = [len(y) for y in YY]
	A   = np.hstack(  [ [i]*len(y) for i,y in enumerate(YY) ]  )
	return Y,A
	# self.GROUP    = np.array([[i]*j for i,j in enumerate(self.JJ)]).flatten()
	
def stack1d_rm(YY):
	nCond = len(YY)
	nSubj = YY[0].shape[0]
	Y     = np.vstack(YY)
	A     = np.hstack(  [ [i]*nSubj for i in range(nCond) ]  )
	SUBJ  = np.hstack(  range(nSubj) * nCond  )
	return Y,A,SUBJ
	




