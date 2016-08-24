
import spm1d




#(0) Load data:
dataset   = spm1d.data.uv0d.anova3nested.SouthamptonNested3()
y,A,B,C   = dataset.get_data()
print( dataset )


#(1) Run ANOVA:
FF        = spm1d.stats.anova3nested(y, A, B, C)
FFi       = FF.inference(0.05)
print( FFi )

