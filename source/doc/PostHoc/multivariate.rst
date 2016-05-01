
.. _label-Examples-StatsPostHocMV:

Multivariate *post hoc* analysis
=====================================

*Post hoc* analyses are currently in development.

As a rule-of-thumb, **NEVER** report *post hoc* results which disagree with the main test results.  If the results disagree, the *post hoc* procedures are too simple.

If you report *post hoc* results for **spm1d** analyses please explicitly highlight the limitations described in this document.



.. warning:: Current *post hoc* procedures in **spm1d** are likely too simple. 

	The example belowe uses a simple Bonferroni correction, but this assumes that the *post hoc* tests are independent, which is usually not the case, especially for multivariate data.


.. danger:: Current *post hoc* procedures in **spm1d** are generally not valid.

	They are not valid because they involve separate smoothness assessments for each *post hoc* test.
	
	Although the resulting errors are expected to be small, we cannot guarantee validity.



Suggestions for conducting *post hoc* analyses for multivariate tests:

* For each *post hoc* test use a Bonferroni correction.

* For Hotelling's T\ :sup:`2` tests conduct separate t tests on each vector component, but acknowledge that this neglects vector component covariance.

* For CCA conduct separate regression tests on each vector component, but acknowledge that this neglects vector component covariance.

* For MANOVA conduct separate Hotelling's T\ :sup:`2` tests on each pair of groups, and if those tests reach significance then conduct additional *post hoc* t tests on each vector component, but acknowledge that this neglects vector component covariance.

