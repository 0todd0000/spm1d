
import numpy as np
import spm1d



#(0) Load dataset:
dataset = spm1d.data.uv0d.regress.RSRegression()
dataset = spm1d.data.uv0d.regress.ColumbiaHeadCircumference()
y,x     = dataset.get_data()



#(1) Conduct normality test:
np.random.seed(0)
alpha      = 0.05
spmi       = spm1d.stats.normality.regress(y, x).inference(alpha)
print( spmi )


