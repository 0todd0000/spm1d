'''
Linear algebra module

(This and all modules whose names start with underscores
are not meant to be accessed directly by the user.)
'''

# Copyright (C) 2023  Todd Pataky

import numpy as np


def rank(A, tol=None):
	'''
	This is a slight modification of np.linalg.matrix_rank whose
	default tolerance yields poor results for some matrices.
	Here the tolerance is boosted by a factor of ten for improved performance.
	'''
	M = np.asarray(A)
	S = np.linalg.svd(M, compute_uv=False)
	if tol is None:
		tol = 10 * S.max() * max(M.shape) * np.finfo(M.dtype).eps
	rnk = sum(S > tol)
	return rnk
