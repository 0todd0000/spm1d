
import numpy as np
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



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpmlist   = spm1d.stats.nonparam.anova2(y, A, B)
snpmilist  = snpmlist.inference(alpha, iterations=1000)
print( 'Non-parametric results:')
print( snpmilist )


#(2) Compare to parametric test:
spmlist    = spm1d.stats.anova2(y, A, B, equal_var=True)
spmilist   = spmlist.inference(alpha)
print( 'Parametric results:')
print( spmilist )


