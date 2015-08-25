
import spm1d





#(0) Load dataset:
dataset   = spm1d.data.uv0d.anova3.RSItalian()
dataset   = spm1d.data.uv0d.anova3.SouthamptonFullyCrossedMixed()
y,A,B,C   = dataset.get_data()
print dataset



#(1) Run ANOVA:
F = spm1d.stats.anova3(y, A, B, C, equal_var=True)
Fvalues = [f.z for f in F]
print Fvalues

