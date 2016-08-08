
import itertools
import numpy as np
from scipy import stats
import spm1d



#(0) Load dataset:
dataset = spm1d.data.uv0d.anova1.Cars()
# dataset = spm1d.data.uv0d.anova1.Sound()
# dataset = spm1d.data.uv0d.anova1.Southampton1()
# dataset = spm1d.data.uv0d.anova1.ConstructionUnequalSampleSizes()
# dataset = spm1d.data.uv0d.anova1.RSUnequalSampleSizes()
y,A     = dataset.get_data()
print dataset



alpha      = 0.05
F = spm1d.stats.anova1(y, A, equal_var=True)
Fi = F.inference(alpha)
z0 = F.z
print Fi







# if isinstance(Y, (list,tuple)):
# 	_datachecks.check('anova1list', Y)
# 	A   = np.hstack([[i]*y.shape[0] for i,y in enumerate(Y)])
# 	Y   = np.hstack(Y) if Y[0].ndim==1 else np.vstack(Y)
# else:
# 	_datachecks.check('anova1', Y, A)



Y = y


from spm1d.stats.anova import designs,models
from spm1d.stats.anova.ui import aov

design  = designs.ANOVA1(A)


Z   = []
for i in range(5000):
	ind  = np.random.permutation( A.size )
	model   = models.LinearModel(Y[ind], design.X)
	model.fit()
	F       = aov(model, design.contrasts, design.f_terms)[0]
	Z.append( F.z )

Z          = np.array(Z)


### conduct inference

p          = np.mean( Z>z0 )
zstar      = np.percentile(Z, 100*(1-alpha))

print p






# #(3) Compare to parametric inference:
# p_para     = stats.t.sf(t0, df)
# tCrit_para = stats.t.isf(alpha, df)
#
#
#
# ### report results:
# print 'Non-parametric t test:'
# print '   t=%.3f, p=%.5f, tCritical=%.3f' %(t0,p,tCrit)
# print
# print 'Parametric t test:'
# print '   t=%.3f, p=%.5f, tCritical=%.3f' %(t0,p_para,tCrit_para)
# print


