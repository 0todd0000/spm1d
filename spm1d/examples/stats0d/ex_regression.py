
import numpy as np
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.regress.RSRegression()
dataset = spm1d.data.uv0d.regress.ColumbiaHeadCircumference()
y,x     = dataset.get_data()
print( dataset )


#(1) Conduct test using spm1d:
spmt    = spm1d.stats.regress(y, x)
spmti   = spmt.inference(0.05, two_tailed=True)
print( spmti )


