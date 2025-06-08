

import itertools
from math import factorial
import numpy as np
from . factors import Factor
from . util import permutations_without_repetition



class RegressionPermuter(object):
    def __init__(self, n):
        self.n        = n
        self.nfactors = 1

    @property
    def ncomb(self):
        return factorial( self.n )

    @property
    def nPermTotal(self):
        return self.ncomb

    @property
    def combinations(self):
        for c in itertools.permutations( range(self.n) ):
            yield (list(c),) 

    @property
    def combinations_half(self):
        for i,c in enumerate( itertools.permutations( range(self.n) ) ):
            if i < self.ncomb/2:
                yield (list(c),)
                
    def random(self):
        return (np.random.permutation( self.n ),)


class SingleSamplePermuter(object):
    def __init__(self, n):
        self.n        = n
        self.nfactors = 1

    @property
    def ncomb(self):
        return 2**self.n

    @property
    def nPermTotal(self):
        return self.ncomb

    @property
    def combinations(self):
        for c in itertools.product((1,-1), repeat=self.n):
            yield (c,) 

    @property
    def combinations_half(self):
        for i,c in enumerate( itertools.product((1,-1), repeat=self.n) ):
            if i < self.ncomb/2:
                yield (c,)
                
    def random(self):
        return (2*np.random.binomial(1, 0.5, self.n) - 1, )


class MultiFactorPermuter(object):
    def __init__(self, *args):
        self._factors = [Factor(x) for x in args]

    @property
    def ncomb(self):
        n = 1
        for f in self._factors:
            n *= f.ncomb
        return n

    @property
    def nfactors(self):
        return len(self._factors)


    @property
    def nPermTotal(self):
        return self.ncomb

    @property
    def combinations(self):
        iters    = [permutations_without_repetition(f.A) for f in self._factors]
        for a in itertools.product( *iters ):
            yield a
            
    @property
    def combinations_half(self):
        iters    = [permutations_without_repetition(f.A) for f in self._factors]
        for i,a in enumerate( itertools.product( *iters ) ):
            if i < self.ncomb/2:
                yield a
        

    def random(self):
        return tuple(f.random_permutation() for f in self._factors)


if __name__ == '__main__':
    import numpy as np
    
    # perm = SingleSamplePermuter( 5 )
    # for i,c in enumerate(perm.combinations):
    #     print( i, c )
    # print( perm.ncomb )
    # print( perm.random() )
    # print( perm.random() )
    # print( perm.random() )
    
    
    A        = np.array([0, 0, 0, 0,    1, 1, 1, 1])
    B        = np.array([0, 0, 1, 1,    0, 0, 1, 1])
    permuter = MultiFactorPermuter(A)
    permuter = MultiFactorPermuter(A, B)

    # for i,c in enumerate( permuter.combinations ):
    #     print(i, c)
        
    for i in range(5):
        print( permuter.random() )
    # print(i+1)
    print(permuter.ncomb)

    