
import numpy as np
import scipy.stats
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



#(2) Compare to SciPy result:
results    = scipy.stats.normaltest(y)
print
print( 'scipy.stats.normaltest result:' )
print( '   K2=%.5f, p=%.5f' %(results.statistic, results.pvalue) )
print
print( 'spm1d result:' )
print( '   K2=%.5f, p=%.5f' %(spmi.z, spmi.p) )
print


