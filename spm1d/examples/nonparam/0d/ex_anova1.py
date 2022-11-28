
import numpy as np
import spm1d



#(0) Load dataset:
# dataset = spm1d.data.uv0d.anova1.Cars()
# dataset = spm1d.data.uv0d.anova1.Sound()
# dataset = spm1d.data.uv0d.anova1.Southampton1()
# dataset = spm1d.data.uv0d.anova1.ConstructionUnequalSampleSizes()
dataset = spm1d.data.uv0d.anova1.RSUnequalSampleSizes()
y,A     = dataset.get_data()
print( dataset )




#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
F          = spm1d.stats.nonparam.anova1(y, A)
Fi         = F.inference(alpha, iterations=1000)
print(Fi)


#(2) Compare to parametric test:
Fparam     = spm1d.stats.anova1(y, A, equal_var=True)
Fparami    = Fparam.inference(alpha)



#(3) Print results:
print
print( 'Non-parametric results:' )
print( '   t=%.3f, p=%.5f' %(Fi.z, Fi.p) )
print
print( 'Parametric results:' )
print( '   t=%.3f, p=%.5f' %(Fparami.z, Fparami.p) )
print



