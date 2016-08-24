
import numpy as np
import spm1d



#(0) Create data:
dataset      = spm1d.data.uv0d.normality.ZarBiostatisticalAnalysis68()
dataset      = spm1d.data.uv0d.normality.KendallRandomNumbers()
y            = dataset.get_data()
print( dataset )



#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spm        = spm1d.stats.normality.ttest(y)
spmi       = spm.inference(alpha)
print( spmi )


