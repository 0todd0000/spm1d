

import itertools
from . factors import Factor
from . util import permutations_without_repetition


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

    