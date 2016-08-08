
import numpy as np
import scipy.stats
import spm1dNP
import spm1d



#(0) Load dataset:
dataset   = spm1d.data.uv0d.anova3.RSItalian()
dataset   = spm1d.data.uv0d.anova3.SouthamptonFullyCrossedMixed()
y,A,B,C   = dataset.get_data()
print dataset




# ### prepare stat computer:
# calculators = spm1dNP.calculators
# calc           = calculators.CalculatorANOVA2(A, B)
# z              = calc.get_test_stat(y)
# print z
#
#
# ### prepare permuter:
# permuters = spm1dNP.permuters
# perm      = permuters.PermuterANOVA2(y, A, B)
# z0        = perm.get_test_stat_original()
# perm.build_pdf(iterations=1000)
# print z0




### test high-level function:
#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
spmlist    = spm1dNP.anova3(y, A, B, C)
spmilist   = spmlist.inference(alpha, iterations=100)
for spmi in spmilist:
	print 'F = %.3f, p = %.3f' %(spmi.z, spmi.p)



