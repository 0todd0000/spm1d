
.. _label-DocumentationMatlab:

======================
Documentation (Matlab)
======================

.. danger:: Unbalanced two- and three-way repeated-measures ANOVA results have not been verified.
	
	Example: more subjects in Group 1 than in Group 2.
	
	Please interpret results for these designs with caution, and recognize that they might not be valid.


:ref:`Installing for MATLAB <label-installationMatlab>`

:ref:`Link to Python documentation <label-Documentation>`

.. warning:: There are a few key differences between the MATLAB and Python versions of **spm1d**.

	The main version of **spm1d** is the Python version.  The MATLAB version incorporates much but not all of the functionaly of the Python version.
	
	There will be discrepancies between the Python and MATLAB versions for two main reasons:
	
	1. The MATLAB version of **spm1d** does not yet employ non-sphericity corrections, which are employed by default in the Python version.
	2. The MATLAB version of **spm1d** does not interpolate supra-threshold clusters, thereby generating somewhat inaccurate measurements of cluster size.
	
	Practically the differences are likely to be small, but users should be aware that non-sphericity corrections, by definition, drive the critical threshold higher.
	
	**MATLAB results which just reach the critical threshold must therefore be interpreted with caution**.
	
	The second issue will result in slightly underestimated cluster-level p values.



Examples
-----------------
Inside the **./spm1d/examples** folder you will find Matlab scripts which implement a variety of statistical tests.

These examples correspond to the Python scripts of the same name, which are described in: :ref:`the main documentation <label-Documentation>`.

Statistical theory underlying the examples is documented here: :ref:`label-Theory`


Support
-----------------
We do not provide detailed documentation for the MATLAB version of **spm1d**.

If you require support consider the following options:

#. Running the example scripts in `+spm1d/examples`.
#. Checking the :ref:`Python documentation <label-Documentation>` (the syntax is nearly identical).
#. Submitting a support request to **spm1d**'s `MATLAB github site <http://0todd0000.github.io/spm1dmatlab>`_.
#. Contacting us to request an :ref:`educational workshop <label-Workshops>`.



