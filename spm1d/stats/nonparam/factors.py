
from math import factorial
import numpy as np


class Factor(object):
    def __init__(self, A):
        self.A  = np.asarray(A)  # factor labels
        self.u  = np.unique(A)   # unique factor labels

    @property
    def n(self):  # num.observations (sample size)
        return self.A.shape[0]

    @property
    def ncomb(self):  # number of unique combinations
        a = factorial( self.n )
        b = 1
        for n in self.ns:
            b *= factorial(n)
        return int( a / b )

    @property
    def ns(self):  # num.observations for each factor level
        return np.array(  [(self.A==a).sum() for a in self.u]  )

    @property
    def nu(self): # number of factor levels
        return self.u.size
        
    def random_permutation(self):
        return np.random.permutation( self.A ).tolist()