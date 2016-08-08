
import numpy as np
import scipy.stats
import spm1dNP
import spm1d



#(0) Load dataset:
dataset  = spm1d.data.uv0d.anova1rm.Abdi2010()
# dataset  = spm1d.data.uv0d.anova1rm.Groceries()
# dataset  = spm1d.data.uv0d.anova1rm.Imacelebrity()
# dataset  = spm1d.data.uv0d.anova1rm.Southampton1rm()
y,A,SUBJ = dataset.get_data()
print dataset




# ### prepare stat computer:
# calculators = spm1dNP.calculators
# calc           = calculators.CalculatorANOVA1rm(A, SUBJ)
# z              = calc.get_test_stat(y)
# print z
#
#
# ### prepare permuter:
# permuters = spm1dNP.permuters
# perm      = permuters.PermuterANOVA1rm(y, A, SUBJ)
# z0        = perm.get_test_stat_original()
# perm.build_pdf(iterations=1000)
# print z0




### test high-level function:
#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
spm        = spm1dNP.anova1rm(y, A, SUBJ)
spmi       = spm.inference(alpha, iterations=1000)
print(spmi)



