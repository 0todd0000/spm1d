
import numpy as np
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


