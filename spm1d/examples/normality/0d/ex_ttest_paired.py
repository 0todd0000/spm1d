
import numpy as np
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.tpaired.RSWeightClinic()
dataset = spm1d.data.uv0d.tpaired.ColumbiaMileage()
yA,yB   = dataset.get_data()



#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spmi       = spm1d.stats.normality.ttest_paired(yA, yB).inference(alpha)
print( spmi )




