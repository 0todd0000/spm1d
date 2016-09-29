
import numpy as np
from scipy import stats
import spm1d




#(0) Load dataset:
dataset = spm1d.data.uv0d.regress.RSRegression()
dataset = spm1d.data.uv0d.regress.ColumbiaHeadCircumference()
y,x     = dataset.get_data()
print( dataset )


#(1) Conduct test using spm1d:
spmt    = spm1d.stats.regress(y, x)
spmti   = spmt.inference(0.05, two_tailed=True)
print( spmti )


#(2) Compare to scipy.stats result:
slope,intercept,r,p,se = stats.linregress(x, y)
t       = r * ((y.size-2)/(1-r*r) )**0.5
print( 'scipy.stats result:\n   r = %.5f\n   t = %.5f\n   p = %.5f' %(r,t,p) )


