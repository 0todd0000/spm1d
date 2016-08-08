
import numpy as np
import spm1dNP
import spm1d

#(0) Load dataset:
dataset = spm1d.data.mv0d.cca.FitnessClub()
# dataset = spm1d.data.mv0d.cca.StackExchange()
y,x     = dataset.Y, dataset.x
# x      *= -1
# print dataset

y,x     = [a[:10]  for a in [y,x]]



#(1) Conduct non-parametric test:
alpha      = 0.05
x2         = spm1dNP.cca(y, x)
x2i        = x2.inference(alpha, iterations=1000)
print(x2i)



#(2) Compare to parametric inference:
x2param    = spm1d.stats.cca(y, x)
x2parami   = x2param.inference(alpha)



### report results:
print 'Non-parametric t test:'
print '   T2=%.3f, p=%.5f' %(x2i.z, x2i.p)
print
print 'Parametric t test:'
print '   T2=%.3f, p=%.5f' %(x2parami.z, x2parami.p)
print
