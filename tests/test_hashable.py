
import numpy as np
import spm1d
import rft1d



def test_ttest_0d():
	np.random.seed(0)
	y       = np.random.randn( 8 )
	spm0    = spm1d.stats.ttest(y, 0).inference(0.05)
	spm1    = spm1d.stats.ttest(y, 0).inference(0.05)
	assert spm0 == spm1

def test_ttest_1d():
	np.random.seed(1)
	y       = rft1d.randn1d( 8, 101, 20 )
	spm0    = spm1d.stats.ttest(y, 0).inference(0.05)
	spm1    = spm1d.stats.ttest(y, 0).inference(0.05)
	assert spm0 == spm1




def test_ttest2_0d():
	np.random.seed(0)
	y0      = np.random.randn( 8 )
	y1      = np.random.randn( 12 )
	spm0    = spm1d.stats.ttest2(y0, y1).inference(0.05)
	spm1    = spm1d.stats.ttest2(y0, y1).inference(0.05)
	assert spm0 == spm1

def test_ttest2_1d():
	np.random.seed(1)
	y0      = rft1d.randn1d( 8, 101, 20 )
	y1      = rft1d.randn1d( 12, 101, 20 )
	spm0    = spm1d.stats.ttest2(y0, y1).inference(0.05)
	spm1    = spm1d.stats.ttest2(y0, y1).inference(0.05)
	assert spm0 == spm1




def test_regress_0d():
	np.random.seed(0)
	y       = np.random.randn( 8 )
	x       = np.random.randn( 8 )
	spm0    = spm1d.stats.regress(y, x).inference(0.05)
	spm1    = spm1d.stats.regress(y, x).inference(0.05)
	assert spm0 == spm1

def test_regress_1d():
	np.random.seed(1)
	y       = rft1d.randn1d( 8, 101, 20 )
	x       = np.random.randn( 8 )
	spm0    = spm1d.stats.regress(y, x).inference(0.05)
	spm1    = spm1d.stats.regress(y, x).inference(0.05)
	assert spm0 == spm1




def test_anova1_0d():
	np.random.seed(0)
	y       = np.random.randn( 24 )
	A       = np.asarray(  [0]*8 + [1]*8 + [2]*8  )
	spm0    = spm1d.stats.anova1(y, A).inference(0.05)
	spm1    = spm1d.stats.anova1(y, A).inference(0.05)
	assert spm0 == spm1

def test_anova1_1d():
	np.random.seed(0)
	y       = rft1d.randn1d( 24, 101, 20 )
	A       = np.asarray(  [0]*8 + [1]*8 + [2]*8  )
	spm0    = spm1d.stats.anova1(y, A).inference(0.05)
	spm1    = spm1d.stats.anova1(y, A).inference(0.05)
	assert spm0 == spm1
	



def test_anova1rm_0d():
	np.random.seed(0)
	j,n     = 8, 3
	A       = np.hstack(   [ [i]*j for i in range(n) ]   )
	S       = np.hstack(   [ np.arange(j) ] * n   )
	y       = np.random.randn( A.size )
	spm0    = spm1d.stats.anova1rm(y, A, S).inference(0.05)
	spm1    = spm1d.stats.anova1rm(y, A, S).inference(0.05)
	assert spm0 == spm1
	
	
def test_anova1rm_1d():
	np.random.seed(0)
	j,n     = 8, 3
	A       = np.hstack(   [ [i]*j for i in range(n) ]   )
	S       = np.hstack(   [ np.arange(j) ] * n   )
	y       = rft1d.randn1d( A.size, 101, 20 )
	spm0    = spm1d.stats.anova1rm(y, A, S).inference(0.05)
	spm1    = spm1d.stats.anova1rm(y, A, S).inference(0.05)
	assert spm0 == spm1




def test_anova2_0d():
	np.random.seed(0)
	JJ      = np.array(  [[8,8],[8,8],[12,11]]  )
	nA,nB   = JJ.shape
	AA      = np.vstack([list(range(nA))  for i in range(nB)] ).T
	BB      = np.vstack([list(range(nB))  for i in range(nA)] )
	A       = np.hstack([[x]*j  for x,j in zip(AA.ravel(), JJ.ravel())])
	B       = np.hstack([[x]*j  for x,j in zip(BB.ravel(), JJ.ravel())])
	y       = np.random.randn( A.size )
	spm0    = spm1d.stats.anova2(y, A, B, equal_var=True).inference(0.05)
	spm1    = spm1d.stats.anova2(y, A, B, equal_var=True).inference(0.05)
	assert spm0 == spm1

def test_anova2_1d():
	np.random.seed(0)
	JJ      = np.array(  [[8,8],[8,8],[12,11]]  )
	nA,nB   = JJ.shape
	AA      = np.vstack([list(range(nA))  for i in range(nB)] ).T
	BB      = np.vstack([list(range(nB))  for i in range(nA)] )
	A       = np.hstack([[x]*j  for x,j in zip(AA.ravel(), JJ.ravel())])
	B       = np.hstack([[x]*j  for x,j in zip(BB.ravel(), JJ.ravel())])
	y       = rft1d.randn1d( A.size, 101, 20 )
	spm0    = spm1d.stats.anova2(y, A, B, equal_var=True).inference(0.05)
	spm1    = spm1d.stats.anova2(y, A, B, equal_var=True).inference(0.05)
	assert spm0 == spm1





