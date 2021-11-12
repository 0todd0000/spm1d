
import numpy as np
import spm1d



#(0) Load dataset:
# dataset   = spm1d.data.uv0d.anova3.RSItalian()
dataset   = spm1d.data.uv0d.anova3.SouthamptonFullyCrossedMixed()
y,A,B,C   = dataset.get_data()
print( dataset )



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpmlist   = spm1d.stats.nonparam.anova3(y, A, B, C)
snpmilist  = snpmlist.inference(alpha, iterations=1000)
print( 'Non-parametric results:')
print( snpmilist )



#(2) Compare to parametric test:
spmlist    = spm1d.stats.anova3(y, A, B, C, equal_var=True)
spmilist   = spmlist.inference(alpha)
print( 'Parametric results:')
print( spmilist )
