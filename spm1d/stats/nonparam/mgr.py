
import numpy as np

percentile = lambda x,perc: np.percentile(x, perc, method='linear')



class _PermutationTestManager(object):
    def __init__(self, y, mv=False):
        self._two_tailed    = False
        self.J              = y.shape[0]
        self.Z              = None  # permutation teststat distribution
        self.calc           = None  # test statistic calculator
        self.ismultivariate = mv
        self.permuter       = None  # permuter object
        self.y              = y     # dv array
       
    @property
    def dim(self):
        return self.y.ndim - 1

    @property
    def minp(self):  # minimum possible p-value given the number of permutations
        p = None if (self.Z is None) else (1 / self.nPermActual)
        if self._two_tailed:
            p /= 2
        return p

    @property
    def nfactors(self):
        return self.permuter.nfactors

    @property
    def nPermActual(self):
        return None if (self.Z is None) else self.Z.shape[0]

    def _constrain_p(self, alpha, zstar, z, p):
        two_tailed    = isinstance(zstar, tuple)
        # set miminum and maximum p values:
        minp     = 1 / self.Z.size
        maxp     = 1 - minp
        # adjust the p value to alpha if (z > z*) but (p > alpha)
        zc0,zc1       = zstar if two_tailed else (-np.inf, zstar)
        if (z > zc1) and (p > alpha):
            p         = alpha
        elif (z < zc0) and (p > alpha):
            p         = alpha
        # substitute with min/max p value if applicable:
        p = min( max(p, minp), maxp )
        return p

    def set_calculator(self, calc):
        self.calc = calc
    
    def set_permuter(self, obj):
        self.permuter = obj



class PermutationTestManager0D(_PermutationTestManager):
    def __init__(self, y, mv=False):
        super().__init__(y, mv)
        self.I = y.shape[1] if mv else 1

    def inference(self, alpha, two_tailed=False):
        self._two_tailed = two_tailed
        if two_tailed:
            zc0,zc1 = percentile(self.Z, [100*0.5*alpha,100*(1-0.5*alpha)])
            return float(zc0), float(zc1)
        else:
            return float( percentile(self.Z, 100*(1-alpha)) )
    
    def get_p_value(self, z, zstar, alpha):
        if isinstance(zstar, tuple):  # two-tailed
            if z>0:
                p = 2 * (self.Z > z).mean()
            else:
                p = 2 * (self.Z < z).mean()
        else:
            p = (self.Z > z).mean()
        p = self._constrain_p(alpha, zstar, z, p)
        return p
        

    def permute(self, niter=-1, two_tailed=False):
        self._two_tailed = two_tailed
        perm = self.permuter
        if niter == -1:
            self.Z = np.array([self.calc.teststat(self.y, *c)  for c in perm.combinations])
        else:
            self.Z = np.array([self.calc.teststat(self.y, *perm.random())  for i in range(niter)])




class PermutationTestManager1D(_PermutationTestManager):
    def __init__(self, y, mv=False, roi=None):
        super().__init__(y, mv)
        self.I        = y.shape[2] if mv else 1
        self.Q        = y.shape[1]
        self.ZZ       = None  # all permuted test statistic fields
        self.Z2       = None  # secondary (cluster metric) permutation distribution
        self.metric   = None  # metric for secondary distribution
        self.msk      = None
        self.roi      = None
        # self._roin    = None
        self._set_roi( roi )
        
    @property
    def hasroi(self):
        return self.roi is not None

    # def _mask_dv(self):
    #     y = self.y
    #     if self.roi is not None:
    #         roi = self.roi
    #         if self.ismultivariate:
    #             roi     = np.dstack( [roi]*self.I )
    #         y = np.ma.masked_array( y, np.logical_not(roi)  )
    #     return y
            
    
    def _set_roi(self, roi):
        if roi is not None:
            self.roi    = np.asarray(roi, dtype=bool)
            # self._roin  = np.logical_not( self.roi )
            self.msk    = np.logical_not(self.roi)
            msk         = np.asarray( [self.msk]*self.J, dtype=bool )
            if self.ismultivariate:
                msk     = np.dstack( [msk]*self.I )
            self.y      = np.ma.masked_array( self.y, msk  )
    
    def build_secondary_pdf(self, zstar, circular=False):
        self.Z2 = np.array([self.metric.get_max_metric(z, zstar, circular)   for z in np.array(self.ZZ)])
    
    def inference(self, alpha, two_tailed=False):
        self._two_tailed = two_tailed
        if two_tailed:
            # since abs(z) is used alpha mustn't be multiplied by 0.5
            # self.Z = np.abs(self.ZZ).max(axis=1)
            self.Z = np.array(  np.ma.abs(self.ZZ).max(axis=1)  ) # convert masked array to array if needed
        else:
            self.Z = np.array( self.ZZ.max(axis=1) ) # convert masked array to array if needed
        zc = percentile(self.Z, 100*(1-alpha))
        return zc
            
    def permute(self, niter=-1, two_tailed=False):
        self._two_tailed = two_tailed
        perm = self.permuter
        if niter == -1:
            if two_tailed:
                ZZ = [self.calc.teststat(self.y, *c)  for c in perm.combinations_half]
            else:
                ZZ = [self.calc.teststat(self.y, *c)  for c in perm.combinations]
        else:
            ZZ = [self.calc.teststat(self.y, *perm.random())  for i in range(niter)]
        if self.hasroi:
            msk     = np.asarray( [self.msk]*len(ZZ), dtype=bool )
            self.ZZ = np.ma.masked_array( ZZ, msk )
        else:
            self.ZZ = np.array(ZZ)
            
            

    def set_metric(self, metric_name):
        from . metrics import metric_dict
        self.metric     = metric_dict[metric_name]



def get_perm_mgr(y, mv=False, roi=None):
    is0d = y.ndim==2 if mv else y.ndim==1
    mgr  = PermutationTestManager0D(y, mv) if is0d else PermutationTestManager1D(y, mv, roi)
    return mgr

    

    