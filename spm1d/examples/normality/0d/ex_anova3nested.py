
import numpy as np
import spm1d



#(0) Load dataset:
dataset   = spm1d.data.uv0d.anova3nested.SouthamptonNested3()
y,A,B,C   = dataset.get_data()
print( dataset )




#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spmi       = spm1d.stats.normality.anova3nested(y, A, B, C).inference(alpha)
print( spmi )


