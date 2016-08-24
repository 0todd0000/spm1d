
import numpy as np
from scipy import stats
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.t2.RSFlavor()
dataset = spm1d.data.uv0d.t2.ColumbiaPlacebo()
yA,yB   = dataset.get_data()
print( dataset )


#(1) Conduct t test using spm1d:
spmt    = spm1d.stats.ttest2(yA, yB, equal_var=False)
spmti   = spmt.inference(0.05, two_tailed=False)
print( spmti )


#(2) Compare to scipy.stats result:
t,p     = stats.ttest_ind(yA, yB, equal_var=False)
p       = 0.5*p  #one-tailed inference
print( 'scipy.stats result:\n   t = %.5f\n   p = %.5f' %(t,p) )


