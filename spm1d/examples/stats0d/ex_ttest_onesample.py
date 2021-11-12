
import numpy as np
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.t1.RSWeightReduction()
# dataset = spm1d.data.uv0d.t1.ColumbiaSalmonella()
y,mu    = dataset.get_data()
print( dataset )



#(1) Conduct t test using spm1d:
spmt    = spm1d.stats.ttest(y, mu)
spmti   = spmt.inference(0.05, two_tailed=False)
print( spmti )



