
import numpy as np
from scipy import stats
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.tpaired.RSWeightClinic()
dataset = spm1d.data.uv0d.tpaired.ColumbiaMileage()
print( dataset )
yA,yB   = dataset.get_data()


#(1) Conduct t test using spm1d:
spmt    = spm1d.stats.ttest_paired(yA, yB)
spmti   = spmt.inference(0.05, two_tailed=False)
print( spmti )


#(2) Compare to scipy.stats result:
t,p     = stats.ttest_rel(yA, yB)
p       = 0.5*p  #one-tailed inference
print( 'scipy.stats result:\n   t = %.5f\n   p = %.5f' %(t,p) )


