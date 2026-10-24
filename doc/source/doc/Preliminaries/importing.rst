
.. _label-Examples-IO:


Importing data
-------------------------------------------

To conduct univariate **spm1d** analysis the data should be arranged as a (J x Q) array, where J is the number of 1D responses (i.e. trials or subjects) and Q is the number of nodes in the 1D continuum.

To conduct multivariate **spm1d** analysis the data should be arranged as a (J x Q X I) array, where I is the number of vector components in the 1D continuum.

.. danger:: **spm1d** no longer directly supports data importing.

	Users are instead encouraged to use the following data importing tools (see examples below):
	
	* **numpy.load**
	* **numpy.loadtxt**
	* **scipy.io.loadmat**


.. warning:: **WINDOWS USERS** --- File names in Python should be constructed using one of the following forms:

     >>> fname = 'C:\\Temp\\MyData\\ex_kinematics.txt'

     >>> import os
     >>> fname = os.path.join('C:\Temp', 'MyData', 'ex_kinematics.txt')




Importing ASCII data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``./spm1d/examples/io/ex_import_txt.py``

If ASCII data are arranged in a (J x Q) tab-delimited array:

.. plot:: pyplots/ex_import_txt.py
   :include-source:



Importing MATLAB data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``./spm1d/examples/io/ex_import_mat.py``

MATLAB data files containing arbitrary variables can be imported as follows:

	>>> from scipy.io import loadmat
	>>> M = loadmat('myfile.mat')
	>>> a = M['VariableA']
	>>> b = M['VariableB']
	>>> c = M['VariableC']

Example script:

.. plot:: pyplots/ex_import_mat.py
   :include-source:



Importing HDF5 data (deprecated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(HDF5 is no longer supported)










