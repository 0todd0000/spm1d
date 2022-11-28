
import spm1d



#(0) Load dataset:
dataset   = spm1d.data.uv0d.anova2.Mouse()       #2x2
dataset   = spm1d.data.uv0d.anova2.Detergent()     #2x3
# dataset   = spm1d.data.uv0d.anova2.Satisfaction()  #2x3
# dataset   = spm1d.data.uv0d.anova2.SouthamptonCrossed1()  #2x3
y,A,B     = dataset.get_data()
print( dataset )



#(1) Conduct normality test:

alpha      = 0.05
spmi       = spm1d.stats.normality.k2.anova2(y, A, B).inference(alpha)
print( spmi )


