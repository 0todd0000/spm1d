
import spm1d



#(0) Create data:
dataset      = spm1d.data.uv0d.normality.ZarBiostatisticalAnalysis68()
dataset      = spm1d.data.uv0d.normality.KendallRandomNumbers()
dataset      = spm1d.data.uv0d.normality.RFaithful()
# dataset      = spm1d.data.uv0d.normality.RSAge()
# dataset      = spm1d.data.uv0d.normality.RSShapiroWilk1()
# dataset      = spm1d.data.uv0d.normality.RSShapiroWilk2()
# dataset      = spm1d.data.uv0d.normality.RSShapiroWilk3()
y            = dataset.get_data()
print( dataset )



#(1) Conduct normality tests:
alpha      = 0.05
spm        = spm1d.stats.normality.k2.ttest(y)
spmi       = spm.inference(alpha)
print( "D'Agostino-Pearson K2 test:" )
print( spmi )
print( "\nShapiro Wilk test:" )
w,p        = spm1d.stats.normality.sw.ttest(y)
print( 'W=%.5f, p=%.5f' %(w,p) )