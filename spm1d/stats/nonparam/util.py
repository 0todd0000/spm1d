
import numpy as np


def permutations_without_repetition(labels):
    '''
    Modified from:
    https://stackoverflow.com/questions/38544460/how-to-generate-permutations-without-generating-repeating-results-but-with-a-fix
    Thank you nneonneo!
    '''
    from collections import Counter
    from itertools import combinations

    if isinstance(labels, np.ndarray):
        labels = labels.tolist()
    partitions = list(  Counter(labels).items()  )
    partitions.sort()
    k = len(partitions)
    def _helper(idxset, i):
        if len(idxset) == 0:
            yield ()
            return
        for pos in combinations(idxset, partitions[i][1]):
            for res in _helper(sorted(set(idxset) - set(pos)), i+1):
                yield (pos,) + res

    n = len(labels)
    for poses in _helper(list(range(n)), 0):
        out = [None] * n
        for i, pos in enumerate(poses):
            for idx in pos:
                out[idx] = partitions[i][0]
        yield out