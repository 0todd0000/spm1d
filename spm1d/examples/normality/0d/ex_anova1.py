
import spm1d



#(0) Load dataset:
dataset = spm1d.data.uv0d.anova1.Cars()
# dataset = spm1d.data.uv0d.anova1.Sound()
# dataset = spm1d.data.uv0d.anova1.Southampton1()
dataset = spm1d.data.uv0d.anova1.ConstructionUnequalSampleSizes()
# dataset = spm1d.data.uv0d.anova1.RSUnequalSampleSizes()
y,A     = dataset.get_data()



#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.anova1(y, A).inference(alpha)
print( spmi )




