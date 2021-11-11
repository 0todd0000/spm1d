
import numpy as np
import spm1d




#(0) Load dataset:
dataset = spm1d.data.mv0d.manova1.AnimalDepression()
# dataset = spm1d.data.mv0d.manova1.Stevens2002()
y,A     = dataset.Y, dataset.A
print( dataset )



#(1) Conduct non-parametric test:
np.random.seed(0)
X2n     = spm1d.stats.nonparam.manova1(y, A)
X2ni    = X2n.inference(alpha=0.05, iterations=500)
print( 'Non-parametric result:')
print( X2ni)



#(2) Compare to parametric result:
X2      = spm1d.stats.manova1(y, A)
X2i     = X2.inference(alpha=0.05)
print( 'Parametric result:')
print( X2i)



