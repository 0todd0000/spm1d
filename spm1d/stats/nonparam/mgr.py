
import numpy as np


class PermutationTestManager(object):
    def __init__(self, y, roi=None):
        self.ZZ       = None  # all permuted test statistic fields
        self.Z        = None  # permutation teststat distribution
        self.Z2       = None  # secondary (cluster metric) permutation distribution
        self.calc     = None  # test statistic calculator
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
        self.Z = self.ZZ.max(axis=1)
        return np.percentile(self.Z, 100*(1-alpha), interpolation='midpoint')

    def _inference_1d_twotailed(self, alpha):
        self.Z = np.abs(self.ZZ).max(axis=1)
        return np.percentile(self.Z, 100*(1-alpha), interpolation='midpoint')


    def build_secondary_pdf(self, zstar, circular=False):
        self.Z2 = np.array([self.metric.get_max_metric(z, zstar, circular)   for z in self.ZZ])
    
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
    
    # def permute(self, niter=-1, two_tailed=False):
    #     perm = self.permuter
    #     if niter == -1:
    #         if two_tailed:
    #             self.ZZ = np.array([self.fn(self.y, *c)  for c in perm.combinations_half])
    #         else:
    #             self.ZZ = np.array([self.fn(self.y, *c)  for c in perm.combinations])
    #     else:
    #         self.ZZ = np.array([self.fn(self.y, *perm.random())  for i in range(niter)])
    
    
    def permute(self, niter=-1, two_tailed=False):
        perm = self.permuter
        if niter == -1:
            if two_tailed:
                self.ZZ = np.array([self.calc.get_test_stat(self.y, *c)  for c in perm.combinations_half])
            else:
                self.ZZ = np.array([self.calc.get_test_stat(self.y, *c)  for c in perm.combinations])
        else:
            self.ZZ = np.array([self.calc.get_test_stat(self.y, *perm.random())  for i in range(niter)])
    
    def set_calculator(self, calc):
        self.calc = calc
    
    def set_metric(self, metric_name):
        from . metrics import metric_dict
        self.metric     = metric_dict[metric_name]
    
    def set_permuter(self, obj):
        self.permuter = obj
        
    def set_teststat_fn(self, fn):
        self.fn = fn

    