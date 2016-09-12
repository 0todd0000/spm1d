
import spm1d



#(0) Load dataset:
dataset   = spm1d.data.uv0d.anova3.RSItalian()
dataset   = spm1d.data.uv0d.anova3.SouthamptonFullyCrossedMixed()
y,A,B,C   = dataset.get_data()
print( dataset )



#(1) Conduct normality test:
alpha      = 0.05
spmi       = spm1d.stats.normality.k2.anova3(y, A, B, C).inference(alpha)
print( spmi )
