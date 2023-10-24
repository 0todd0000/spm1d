
import numpy as np


def perm(stat, z, alpha=0.05, testname=None, args=None, nperm=10000, dim=0, **kwargs):
	if alpha < 1/nperm:
		from math import ceil
		n  = ceil( 1/alpha )
		raise ValueError( f'nperm={nperm} is too small. For alpha={alpha}, nperm must be at least {n}.' )
	
	_nprandstate = np.random.get_state()
	
	if dim==0:
		if isinstance(z, (int,float)):
			from . perm0d import inference0d
			results = inference0d(stat, z, alpha=alpha, testname=testname, args=args, nperm=nperm, **kwargs)
		else:
			from . perm0d import inference0d_multi
			results = inference0d_multi(stat, z, alpha=alpha, testname=testname, args=args, nperm=nperm, **kwargs)
	
	elif dim==1:
		if z.ndim==1:
			from . perm1d import inference1d
			results = inference1d(stat, z, alpha=alpha, testname=testname, args=args, nperm=nperm, **kwargs)
		else:
			from . perm1d import inference1d_multi
			results = inference1d_multi(stat, z, alpha=alpha, testname=testname, args=args, nperm=nperm, **kwargs)

	results.extras.update( _nprandstate=_nprandstate )
	
	return results












