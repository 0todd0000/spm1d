
import numpy as np


class PermutationTestManager(object):
    def __init__(self, y, roi=None):
        self.I        = 1
        self.J        = y.shape[0]
        self.Q        = y.shape[1]
        self.ZZ       = None  # all permuted test statistic fields
        self.Z        = None  # permutation teststat distribution
        self.Z2       = None  # secondary (cluster metric) permutation distribution
        self.calc     = None  # test statistic calculator
        self.metric   = None  # metric for secondary distribution
        self.permuter = None  # permuter object
        self.roi      = None
        self._roin    = None
        self.y        = y     # dv array
        self._set_roi( roi )

        
    @property
    def dim(self):
        return self.y.ndim - 1

    @property
    def hasroi(self):
        return self.roi is not None

    def ismultivariate(self):
        return self.y.ndim == 3

    def _constrain_p(self, alpha, zstar, z, p):
        two_tailed    = isinstance(zstar, tuple)
        ### set miminum and maximum p values:
        minp     = 1 / self.Z.size
        maxp     = 1 - minp
        ### adjust the p value to alpha if (z > z*) but (p > alpha)
        zc0,zc1       = zstar if two_tailed else (-np.inf, zstar)
        if (z > zc1) and (p > alpha):
            p         = alpha
        elif (z < zc0) and (p > alpha):
            p         = alpha
        ### substitute with min/max p value if applicable:
        p = min( max(p, minp), maxp )
        return p


    def _inference_0d(self, alpha):
        return np.percentile(self.Z, 100*(1-alpha), interpolation='midpoint')

    def _inference_0d_twotailed(self, alpha):
        print("_inference_0d_twotailed")
        zc0,zc1 = np.percentile(self.Z, [100*0.5*alpha,100*(1-0.5*alpha)], interpolation='midpoint')
        return float(zc0), float(zc1)

    def _inference_1d(self, alpha):
        self.Z = self.ZZ.max(axis=1)
        return np.percentile(self.Z, 100*(1-alpha), interpolation='midpoint')

    def _inference_1d_twotailed(self, alpha):
        # since abs(z) is used alpha mustn't be multiplied by 0.5
        self.Z = np.abs(self.ZZ).max(axis=1)
        return np.percentile(self.Z, 100*(1-alpha), interpolation='midpoint')


    def _set_roi(self, roi):
        print("_set_roi", roi)
        if roi is not None:
            self.roi    = np.asarray(roi, dtype=bool)
            self._roin  = np.logical_not( self.roi )
            roi         = np.asarray( [self.roi]*self.J, dtype=bool )
            if self.ismultivariate:
                roi     = np.dstack( [roi]*self.I )
            self.y      = np.ma.masked_array( self.y, np.logical_not(roi)  )

    def build_secondary_pdf(self, zstar, circular=False):
        self.Z2 = np.array([self.metric.get_max_metric(z, zstar, circular)   for z in self.ZZ])
    
    def get_p_value_0d(self, z, zstar, alpha):
        if isinstance(zstar, tuple):  # two-tailed
            if z>0:
                p = 2 * (self.Z > z).mean()
            else:
                p = 2 * (self.Z < z).mean()
        else:
            p = (self.Z > z).mean()
        p = self._constrain_p(alpha, zstar, z, p)
        return p
        
    
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
    
    def permute(self, niter=-1, two_tailed=False):
        perm = self.permuter
        if niter == -1:
            if two_tailed and self.dim==1:
                Z = np.array([self.calc.teststat(self.y, *c)  for c in perm.combinations_half])
            else:
                Z = np.array([self.calc.teststat(self.y, *c)  for c in perm.combinations])
        else:
            Z = np.array([self.calc.teststat(self.y, *perm.random())  for i in range(niter)])
        if self.dim == 1:
            self.ZZ = Z
        else:
            self.Z  = Z
    
    def set_calculator(self, calc):
        self.calc = calc
    
    def set_metric(self, metric_name):
        from . metrics import metric_dict
        self.metric     = metric_dict[metric_name]
    
    def set_permuter(self, obj):
        self.permuter = obj
        

    