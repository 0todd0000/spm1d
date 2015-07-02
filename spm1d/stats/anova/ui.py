
import numpy as np
import designs,solvers
from .. import _datachecks, _reml


### ONE-WAY DESIGNS ##############

def anova1(Y, A=None, equal_var=False):
	'''
	One-way ANOVA.
	
	:Parameters (Option 1):
		- *Y* --- A list or tuple of (J x Q) numpy arrays
		- *equal_var* --- If *True*, equal group variance will be assumed


	:Parameters (Option 2):
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer group labels
		- *equal_var* --- If *True*, equal group variance will be assumed

	
	:Returns:
		- F : An **spm1d._spm.SPM_F** instance
	
	:Example:
	
	>>> F = spm1d.stats.anova1((Y0,Y1,Y2))
	>>> Fi = F.inference(alpha=0.05)
	>>> Fi.plot()
	'''
	if isinstance(Y, (list,tuple)):
		_datachecks.check('anova1', Y)
		A   = np.array([[i]*y.shape[0] for i,y in enumerate(Y)]).flatten()
		Y   = np.hstack(Y) if Y[0].ndim==1 else np.vstack(Y)
	design  = designs.ANOVA1(A)
	### simplified design matrix:
	# design.set_simplified_design(with_const=False, difference_contrasts=True)
	### this is here just for reference and future use:
	### it is possible to compute the F statistic using a simpler alternative
	### design matrix, but this matrix complicates non-sphericity corrections
	solver  = solvers.ANOVA1(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()[0]
	if not equal_var:
		Y,X,r = solver.Y, solver.X, solver.eij
		Q,C   = design.A.get_Q(), design.contrasts[0].C.T
		f.df  = _reml.estimate_df_anova1(Y, X, r, Q, C)
	return f



def anova1rm(Y, A, SUBJ, equal_var=False):
	'''
	One-way repeated-measures ANOVA.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer group labels
		- *SUBJ* --- (J x 1) vector of subject labels
		- *equal_var* --- If *True*, equal group variance will be assumed

	
	:Returns:
		- F : An **spm1d._spm.SPM_F** instance
	
	:Example:
	
	>>> Y = np.random.randn(9, 101)
	>>> A = np.array([1,1,1, 2,2,2, 3,3,3])
	>>> SUBJ = np.array([1,2,3, 1,2,3, 1,2,3])
	>>> F = spm1d.stats.anova1(Y, A, SUBJ)
	>>> Fi = F.inference(alpha=0.05)
	>>> Fi.plot()
	'''
	design  = designs.ANOVA1rm(A, SUBJ)
	solver  = solvers.ANOVA1rm(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()[0]
	if not equal_var:
		Y,X,r = solver.Y, solver.X, solver.eij
		Q,C   = design.A.get_Q(), design.contrasts[0].C.T
		f.df  =  _reml.estimate_df_anova1(Y, X, r, Q, C)
		# QS    = design.S.get_Q()
		# QQ    = Q+ QS
		# f.df  = _reml.estimate_df_anova1(Y, X, r, QQ, C)
	return f






### TWO-WAY DESIGNS ##############


def anova2(Y, A, B, equal_var=False):
	'''
	Two-way ANOVA.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of three **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B
			3. Interaction AB
	'''
	design  = designs.ANOVA2(A, B)
	solver  = solvers.ANOVA2(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	if not equal_var:
		Y,X,r   = solver.Y, solver.X, solver.eij
		QA,QB,C = design.A.get_Q(), design.B.get_Q(), [c.C.T for c in design.contrasts]
		Q       = QA + QB
		u1,u2   = _reml.estimate_df_anova2(Y, X, r, Q, C)
		for ff,u in zip(f,u1):
			ff.df = u,u2
	return f


def anova2nested(Y, A, B, equal_var=False):
	'''
	Two-way nested ANOVA.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B (nested in A)
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of two **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B

	:Note:
		- there is no interaction term in nested designs.
	'''
	design  = designs.ANOVA2nested(A, B)
	solver  = solvers.ANOVA2nested(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	if not equal_var:
		Y,X,r   = solver.Y, solver.X, solver.eij
		QA,QB,C = design.A.get_Q(), design.B.get_Q(), [c.C.T for c in design.contrasts]
		Q       = QA + QB
		u1,u2   = _reml.estimate_df_anova2(Y, X, r, Q, C)
		f[0].df = u1[0], u1[1]
		f[1].df = u1[1], u2
	return f


def anova2rm(Y, A, B, SUBJ, equal_var=True):
	'''
	Two-way repeated-measures ANOVA.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B
		- *SUBJ* --- (J x 1) vector of integer subject labels
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of three **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B
			3. Interaction AB
			
	:Note:
		- Non-sphericity correction not implemented. Equal variance must be assumed by setting "equal_var=True".
	'''
	if equal_var is not True:
		raise( UserWarning('Non-sphericity correction not implemented. To continue you must assume equal variance and set "equal_var=True".') )
	design  = designs.ANOVA2rm(A, B, SUBJ)
	solver  = solvers.ANOVA2rm(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	# if not equal_var:
	# 	Y,X,r   = solver.Y, solver.X, solver.eij
	# 	QA,QB,C = design.A.get_Q(), design.B.get_Q(), [c.C.T for c in design.contrasts]
	# 	Q       = QA + QB
	# 	u1,u2   = _reml.estimate_df_anova2(Y, X, r, Q, C)
	# 	for ff,u in zip(f,u1):
	# 		ff.df = u,u2
	return f


def anova2onerm(Y, A, B, SUBJ, equal_var=True):
	'''
	Two-way ANOVA with repeated-measures on one factor.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B (the repeated-measures factor)
		- *SUBJ* --- (J x 1) vector of integer subject labels
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of three **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B
			3. Interaction AB
			
	:Note:
		- Non-sphericity correction not implemented. Equal variance must be assumed by setting "equal_var=True".
	'''
	if equal_var is not True:
		raise( UserWarning('Non-sphericity correction not implemented. To continue you must assume equal variance and set "equal_var=True".') )
	design  = designs.ANOVA2onerm(A, B, SUBJ)
	solver  = solvers.ANOVA2onerm(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	return f


### THREE-WAY DESIGNS ##############


def anova3(Y, A, B, C, equal_var=False):
	'''
	Three-way ANOVA.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B
		- *C* --- (J x 1) vector of integer labels for Factor C
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of seven **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B
			3. Main effect C
			4. Interaction AB
			5. Interaction AC
			6. Interaction BC
			7. Interaction ABC
	'''
	design  = designs.ANOVA3(A, B, C)
	solver  = solvers.ANOVA3(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	if not equal_var:
		Y,X,r   = solver.Y, solver.X, solver.eij
		QA,QB,QC,C = design.A.get_Q(), design.B.get_Q(), design.C.get_Q(), [c.C.T for c in design.contrasts]
		Q       = QA + QB + QC
		u1,u2   = _reml.estimate_df_anova2(Y, X, r, Q, C)
		for ff,u in zip(f,u1):
			ff.df = u,u2
	return f

def anova3nested(Y, A, B, C, equal_var=False):
	'''
	Three-way fully nested ANOVA.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B (nested in A)
		- *C* --- (J x 1) vector of integer labels for Factor C (nested in B)
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of three **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B
			3. Main effect C

	:Note:
		- there are no interaction terms in fully-nested designs.
	'''

	design  = designs.ANOVA3nested(A, B, C)
	solver  = solvers.ANOVA3nested(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	if not equal_var:
		Y,X,r   = solver.Y, solver.X, solver.eij
		QA,QB,QC,C = design.A.get_Q(), design.B.get_Q(), design.C.get_Q(), [c.C.T for c in design.contrasts]
		Q       = QA + QB + QC
		u1,uE   = _reml.estimate_df_anova2(Y, X, r, Q, C)
		uA,uB,uC = u1
		f[0].df = uA, uB
		f[1].df = uB, uC
		f[2].df = uC, uE
	return f

	
def anova3onerm(Y, A, B, C, SUBJ, equal_var=True):
	'''
	Three-way ANOVA with repeated-measures on one factor.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B
		- *C* --- (J x 1) vector of integer labels for Factor C (the repeated-measures factor)
		- *SUBJ* --- (J x 1) vector of integer subject labels
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of seven **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B
			3. Main effect C
			4. Interaction AB
			5. Interaction AC
			6. Interaction BC
			7. Interaction ABC
			
	:Note:
		- Non-sphericity correction not implemented. Equal variance must be assumed by setting "equal_var=True".
	'''
	
	if equal_var is not True:
		raise( UserWarning('Non-sphericity correction not implemented. To continue you must assume equal variance and set "equal_var=True".') )
	design  = designs.ANOVA3onerm(A, B, C, SUBJ)
	solver  = solvers.ANOVA3onerm(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	return f

def anova3tworm(Y, A, B, C, SUBJ, equal_var=True):
	'''
	Three-way ANOVA with repeated-measures on two factors.
	
	:Parameters:
		- *Y* --- (J x Q) numpy array
		- *A* --- (J x 1) vector of integer labels for Factor A
		- *B* --- (J x 1) vector of integer labels for Factor B (a repeated-measures factor)
		- *C* --- (J x 1) vector of integer labels for Factor C (a repeated-measures factor)
		- *SUBJ* --- (J x 1) vector of integer subject labels
		- *equal_var* --- If *True*, equal group variance will be assumed

	:Returns:
		- List of seven **spm1d._spm.SPM_F** instances in the following order:
			1. Main effect A
			2. Main effect B
			3. Main effect C
			4. Interaction AB
			5. Interaction AC
			6. Interaction BC
			7. Interaction ABC
			
	:Note:
		- Non-sphericity correction not implemented. Equal variance must be assumed by setting "equal_var=True".
	'''
	if equal_var is not True:
		raise( UserWarning('Non-sphericity correction not implemented. To continue you must assume equal variance and set "equal_var=True".') )
	design  = designs.ANOVA3tworm(A, B, C, SUBJ)
	solver  = solvers.ANOVA3tworm(Y, design.X, design.contrasts)
	f       = solver.compute_test_statistics()
	return f