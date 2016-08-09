
import numpy as np
import scipy.stats
import spm1d
import spm1d



#(0) Load dataset:
dataset   = spm1d.data.uv0d.anova2.Mouse()       #2x2
dataset   = spm1d.data.uv0d.anova2.Detergent()     #2x3
# dataset   = spm1d.data.uv0d.anova2.Satisfaction()  #2x3
# dataset   = spm1d.data.uv0d.anova2.SouthamptonCrossed1()  #2x3
# dataset   = spm1d.data.uv0d.anova2.SPM1D3x3()
# dataset   = spm1d.data.uv0d.anova2.SPM1D3x4()
# dataset   = spm1d.data.uv0d.anova2.SPM1D3x5()
# dataset   = spm1d.data.uv0d.anova2.SPM1D4x4()
# dataset   = spm1d.data.uv0d.anova2.SPM1D4x5()
y,A,B     = dataset.get_data()
print dataset



#(1) Conduct non-parametric test:
np.random.seed(0)
alpha      = 0.05
snpmlist   = spm1d.stats.nonparam.anova2(y, A, B)
snpmilist  = snpmlist.inference(alpha, iterations=1000)
F,p        = np.array(   [(s.z, s.p)  for s in snpmilist]   ).T



#(2) Compare to parametric test:
FF         = spm1d.stats.anova2(y, A, B, equal_var=True)
FFi        = [F.inference(alpha)  for F in FF]



#(3) Print results:
for spmi,snpmi in zip(FFi, snpmilist):
	print 'Parametric:      (F = %.3f, p = %.3f)' %(spmi.z, spmi.p)
	print 'Non-parametric:  (F = %.3f, p = %.3f)\n' %(snpmi.z, snpmi.p)



