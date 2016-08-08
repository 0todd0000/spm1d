
import numpy as np
import scipy.stats
import spm1dNP
import spm1d



#(0) Load dataset:
dataset = spm1d.data.uv0d.anova1.Cars()
dataset = spm1d.data.uv0d.anova1.Sound()
dataset = spm1d.data.uv0d.anova1.Southampton1()
dataset = spm1d.data.uv0d.anova1.ConstructionUnequalSampleSizes()
dataset = spm1d.data.uv0d.anova1.RSUnequalSampleSizes()
y,A     = dataset.get_data()
print dataset




# ### prepare stat computer:
# calculators = spm1dNP.calculators
# calc           = calculators.CalculatorANOVA1(A)
# z              = calc.get_test_stat(y)
# print z
#
#
# ### prepare permuter:
# permuters = spm1dNP.permuters
# perm      = permuters.PermuterANOVA1(y, A)
# z0        = perm.get_test_stat_original()
# perm.build_pdf(iterations=1000)
# print z0




### test high-level function:
#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
spm        = spm1dNP.anova1(y, A)
spmi       = spm.inference(alpha, iterations=1000)
print(spmi)



