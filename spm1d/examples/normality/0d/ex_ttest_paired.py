
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.tpaired.RSWeightClinic()
dataset = spm1d.data.uv0d.tpaired.ColumbiaMileage()
yA,yB   = dataset.get_data()



#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.ttest_paired(yA, yB).inference(alpha)
print( spmi )




