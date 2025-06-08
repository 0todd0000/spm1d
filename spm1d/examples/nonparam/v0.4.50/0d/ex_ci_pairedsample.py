
import numpy as np
import spm1d
import spm1d.stats.nonparam_old  # version of nonparam before spm1d v0.4.50


def print_ci(obj, note=None):
    x0,x1 = obj.ci
    s     = 'CI' if note is None else f'CI ({note})'
    print( f'{s:<20} = ({x0:.5f}, {x1:.5f})' )


# load dataset:
dataset = spm1d.data.uv0d.cipaired.FraminghamSystolicBloodPressure()
y0,y1   = dataset.get_data()



# calculate parametric and non-parametric cis:
np.random.seed(0)
alpha      = 0.05
iterations = 1000
mu         = 0
ci         = spm1d.stats.ci_pairedsample(y0, y1, alpha, mu=mu)
np.random.seed(0)
cinp       = spm1d.stats.nonparam.ci_pairedsample(y0, y1, alpha, mu=mu, iterations=iterations)
np.random.seed(0)
cinpo      = spm1d.stats.nonparam_old.ci_pairedsample(y0, y1, alpha, mu=mu, iterations=iterations)


# print results:
print_ci( dataset, 'Expected' )
print_ci( ci, 'Param' )
print_ci( cinp, 'Nonparam' )
print_ci( cinpo, 'Nonparam old' )
