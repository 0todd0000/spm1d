
Test statistic field maxima
============================================

The basic procedure for RFT validations is outlined in
:ref:`Examples/Basic/Validating  <label-Examples-ValidatingRFTExpectations>`.
This section presents code details for validating the probability with which
test statistic field maxima survive particular thresholds.

	See **./rft1d/examples/val_max_1_onesample_t_1d.py** and other "val_max*.py" scripts

Validations for test statistic set-level and cluster-level inference are
available in scripts titled **./rft1d/examples/val_upx*.py**

.. note:: To see details of test statistic computation click on the "Source code" links above each figure.
	
	

Univariate
-------------------------------------------


One-sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_1_onesample_t_1d.py



Two-sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_2_twosample_t_1d.py



Regression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_3_regress_1d.py


One-way ANOVA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_4_anova1_1d.py




-----


Multivariate
-------------------------------------------

One-sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_5_onesample_T2_1d.py

.. note:: Increasing the number of iterations will cause the results to converge to RFT expectations.


Two-sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_6_twosample_T2_1d.py


Canonical correlation analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_7_cca_1d.py




MANOVA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. plot:: pyplots/val_max_8_manova1_1d.py
