
import numpy as np


class PermutationTestManager(object):
    def __init__(self, y, roi=None):
        self.Z        = None  # permutation teststat distribution
        self.Z2       = None  # secondary permutation distribution
        self.metric   = None  # metric for secondary distribution
        self.permuter = None  # permuter object
        self.fn       = None  # test stat calculation function
        self.roi      = roi
        self.y        = y     # dv array

        
    @property
    def dim(self):
        return self.y.ndim - 1
    
    def _inference_0d(self, alpha):
        pass
    def _inference_0d_twotailed(self, alpha):
        pass
    def _inference_1d(self, alpha):
        return np.percentile(self.Z.max(axis=1), 100*(1-alpha), interpolation='midpoint')
    def _inference_1d_twotailed(self, alpha):
        return np.percentile(np.abs(self.Z).max(axis=1), 100*(1-alpha), interpolation='midpoint')
        
        
    
    def inference(self, alpha, two_tailed=False):
        if self.dim == 0:
            if two_tailed:
                return self._inference_0d_twotailed(alpha)
            else:
                return self._inference_0d(alpha)
        elif self.dim == 1:
            if two_tailed:
                return self._inference_1d_twotailed(alpha)
            else:
                return self._inference_1d(alpha)
    
    def permute(self, niter=-1):
        perm = self.permuter
        if niter == -1:
            self.Z = np.array([self.fn(self.y, *c)  for c in perm.combinations])
        else:
            self.Z = np.array([self.fn(self.y, *perm.random())  for i in range(niter)])
    
    def set_permuter(self, obj):
        self.permuter = obj
        
    def set_teststat_fn(self, fn):
        self.fn = fn

    