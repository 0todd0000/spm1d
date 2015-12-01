from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *

import spm1d




#(0) Load dataset:
dataset = spm1d.data.mv0d.cca.FitnessClub()
dataset = spm1d.data.mv0d.cca.StackExchange()
y,x     = dataset.Y, dataset.x
print(dataset)



#(1) Conduct T2 test using spm1d:
X2      = spm1d.stats.cca(y, x)
X2i     = X2.inference(alpha=0.05)
print(X2i)



