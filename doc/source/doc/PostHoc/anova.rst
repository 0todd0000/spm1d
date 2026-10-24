
.. _label-Examples-StatsPostHoc:

ANOVA *post hoc* analysis
=====================================

*Post hoc* analyses are currently in development.

.. Due to their complexity they are not yet automated in **spm1d**.

The simple approaches described below will approximate appropriate *post hoc* results.

As a rule-of-thumb, **NEVER** report *post hoc* results which disagree with the main test results.  If the results disagree, the *post hoc* procedures are too simple.

If you report *post hoc* results for **spm1d** analyses please explicitly highlight the limitations described in this document.



.. warning:: Current *post hoc* procedures in **spm1d** are likely too simple. 

	The example belowe uses a simple Bonferroni correction, but this assumes that the *post hoc* tests are independent, which is usually not the case.


.. danger:: Current *post hoc* procedures in **spm1d** are generally not valid.

	They are not valid because they involve separate smoothness assessments for each *post hoc* test.
	
	Although the resulting errors are expected to be small, we cannot guarantee validity.

	Users are encouraged to explore other *post hoc* correction methods.






.. _label-Stats-anova_post hoc:

One-way ANOVA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This examples revisits the :ref:`one-way <label-Stats-anova>` example.

Since the :ref:`one-way ANOVA results <label-Stats-anova>` reached significance, we may justifiably conduct *post hoc* analyses.

For one-way ANOVA, *post hoc* analyses consist of two-sample t tests conducted on all group pairs.

Since there are three groups in our one-way ANOVA example, there are three pairs to test (1v2, 1v3, and 2v3).



A simple way to correct for multiple tests across these three group pairs is to use the Bonferroni correction:

   >>> alpha = 0.05
   >>> nTests = 3
   >>> p_critical = spm1d.util.p_critical_bonf(alpha, nTests)

The resulting critical *p* value is **0.016952**.

*Post hoc* tests will be deemed significant if they reach the critical *t* value implied by the p = 0.016952.

Test statistics may be computed for the three group pairs as follows:

.. note:: The *equal_var* option should be the same as was selected for ANOVA.

   >>> t12   = spm1d.stats.ttest2(Y1, Y2, equal_var=False)
   >>> t13   = spm1d.stats.ttest2(Y1, Y3, equal_var=False)
   >>> t23   = spm1d.stats.ttest2(Y2, Y3, equal_var=False)



After computing the test statistics we can conduct inference using the corrected critical *p* value:

.. warning:: The *two_tailed* option must always be *True* in *post hoc* analyses; one-tailed inference is inconsistent with the null-hypothesis implied by ANOVA.

   >>> t12i  = t12.inference(alpha=p_critical, two_tailed=True)
   >>> t13i  = t13.inference(alpha=p_critical, two_tailed=True)
   >>> t23i  = t23.inference(alpha=p_critical, two_tailed=True)

In this case all tests reach significance.

These results may be interpreted exactly as in the case of a single t test: if there were truly no group differences, then smooth, random 1D continua would produce SPM{t}s that reaches the critical *t* threshold in fewer than *alpha* = 5% of many repeated experiments.


.. _label-Stats-multipletests_pvalues:

.. warning:: p values for *post hoc* tests.

	If desired, you may report exact *p* values for each suprathreshold cluster, but in this case the p values must be adjusted for multiple comparisons. 
	
	To compute appropriate *p* values, use the inverse to the Bonferroni correction through **spm1d.util.p_corrected_bonf**, as described below.

Let's consider the following result from one of the *post hoc* tests conducted above:

.. code-block:: python

   SPM{T} inference field
      SPM.z      :  (1x101) raw test stat field
      SPM.df     :  (1, 33.641)
      SPM.fwhm   :  4.82031
      SPM.resels :  (1, 20.74555)
   Inference:
      SPM.alpha  :  0.017
      SPM.zstar  :  4.05216
      SPM.p      :  (<0.001, <0.001, <0.001, 0.008, <0.001)

.. note:: When multiple *p* values exist, they are listed in the following order: (1) upper threshold left-to-right, (2) lower threshold left-to-right. In the "t23i" case above (rightmost panel of the figure) there are five *p* values. The first corresponds to the single upper-threshold cluster. The next four correspond to the four lower-threshold clusters.



The five *p* values listed in the results above correspond to this test's five supra-threshold clusters.

Corrected *p* values may be computed as follows:

   >>> p_value = 0.008
   >>> nTests  = 3
   >>> p_value_corrected = spm1d.util.p_corrected_bonf(p_value, nTests)

**The corrected p value is 0.028**.  If this cluster had precisely touched the threshold, its *p* value would have been *alpha*.



