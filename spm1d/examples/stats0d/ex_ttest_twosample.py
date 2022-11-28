
import numpy as np
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.t2.RSFlavor()
# dataset = spm1d.data.uv0d.t2.ColumbiaPlacebo()
yA,yB   = dataset.get_data()
print( dataset )


#(1) Conduct t test using spm1d:
spmt    = spm1d.stats.ttest2(yA, yB, equal_var=False)
spmti   = spmt.inference(0.05, two_tailed=False)
print( spmti )


