
import spm1d





#(0) Load dataset:
dataset   = spm1d.data.uv0d.anova3.RSItalian()
dataset   = spm1d.data.uv0d.anova3.SouthamptonFullyCrossedMixed()
y,A,B,C   = dataset.get_data()
print( dataset )



#(1) Run ANOVA:
FF        = spm1d.stats.anova3(y, A, B, C, equal_var=True)
FFi       = FF.inference(0.05)
print( FFi )

