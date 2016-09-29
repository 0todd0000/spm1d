
import numpy as np
import scipy.stats
import spm1d



#(0) Load dataset:
# dataset    = spm1d.data.uv0d.ci1.MinnesotaGeyerRate()
dataset    = spm1d.data.uv0d.ci1.WebsterSleep()
y,mu       = dataset.get_data()



#(1) Compute confidence interval:
alpha      = 0.05            #Type I error rate
J          = y.size          #sample size
df         = J - 1           #degrees of freedom
m          = y.mean()        #sample mean
s          = y.std(ddof=1)   #sample standard deviation
zstar      = scipy.stats.t.isf(0.5*alpha, df)    #critical t value
hstar      = zstar * s / J**0.5    #confidence interval height
ci         = m - hstar, m + hstar  #confidence interval



#(2) Compare to spm1d result:
ci_spm1d   = spm1d.stats.ci_onesample(y, alpha, mu)
print( ci_spm1d )
print
print( 'Manually computed CI:' )
print( ci )
