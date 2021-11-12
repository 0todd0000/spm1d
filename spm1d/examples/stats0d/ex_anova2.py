
import spm1d






#(0) Load dataset:
# dataset   = spm1d.data.uv0d.anova2.Mouse()       #2x2
dataset   = spm1d.data.uv0d.anova2.Detergent()     #2x3
# dataset   = spm1d.data.uv0d.anova2.Satisfaction()  #2x3
# dataset   = spm1d.data.uv0d.anova2.SouthamptonCrossed1()  #2x3
# dataset   = spm1d.data.uv0d.anova2.SPM1D3x3()
# dataset   = spm1d.data.uv0d.anova2.SPM1D3x4()
# dataset   = spm1d.data.uv0d.anova2.SPM1D3x5()
# dataset   = spm1d.data.uv0d.anova2.SPM1D4x4()
# dataset   = spm1d.data.uv0d.anova2.SPM1D4x5()
y,A,B     = dataset.get_data()
print( dataset )



#(1) Run ANOVA:
FF        = spm1d.stats.anova2(y, A, B, equal_var=True)
FFi       = FF.inference(0.05)
print( FFi )



