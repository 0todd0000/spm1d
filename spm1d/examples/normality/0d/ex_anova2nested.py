
import spm1d



#(0) Load dataset:
dataset    = spm1d.data.uv0d.anova2nested.QIMacros()
# dataset    = spm1d.data.uv0d.anova2nested.SouthamptonNested1()
y,A,B      = dataset.get_data()
print( dataset )




#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.anova2nested(y, A, B).inference(alpha)
print( spmi )



