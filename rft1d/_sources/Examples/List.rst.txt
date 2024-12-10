
.. _label-Scripts:

Scripts (overview)
========================================================================================

All scripts are located in **./rft1d/examples**,
and below are listed alphabetically, and also bundled into categories.
Details regarding particular concepts are available
:ref:`in the main Examples section<label-Examples>`. 

Categories:

	1. :ref:`Random field generation <label-Scripts-RFs>`
	#. :ref:`Validation --- field smoothness estimation <label-Scripts-Smoothness>`
	#. :ref:`Validation --- conjunction analysis <label-Scripts-ValidationConjunction>`
	#. :ref:`Validation --- field maxima <label-Scripts-ValidationMax>`
	#. :ref:`Validation --- upcrossing extent <label-Scripts-UPX>`
	#. :ref:`Example application --- weather dataset <label-Scripts-Application>`

.. role:: red


.. _label-Scripts-RFs:

Random field generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	* :red:`random_fields_0.py` --- verbose random field generation
	* :red:`random_fields_1.py` --- using **rft1d.randn1d**
	* :red:`random_fields_2.py` --- using **rft1d.random.Generator1D**



.. _label-Scripts-BrokenRFs:

Broken random field generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	* :red:`random_fields_broken_0.py` --- verbose broken random field generation
	* :red:`random_fields_broken_1.py` --- using **rft1d.randn1d**
	* :red:`random_fields_broken_2.py` --- using **rft1d.random.Generator1D**


.. _label-Scripts-Smoothness:

Field smoothness estimation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	* :red:`smoothness_estimation.py` ---  continous field FWHM estimation validation
	* :red:`smoothness_estimation_broken.py` --- piecewise continuous field FWHM estimation validation



.. _label-Scripts-ValidationConjunction:

Validation (conjunction analysis)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	* :red:`val_conj_0_gauss` --- standard normal distribution
	* :red:`val_conj_1_t` --- Student's t distribution
	* :red:`val_conj_1_F` --- Fisher-Snedecor F
	* :red:`val_conj_1_T2` --- Hotelling's T-squared
	* :red:`val_conj_1_X2` --- chi-squared
	
	
	
.. _label-Scripts-ValidationMax:

Validation (field maxima)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	* :red:`val_max_0_gaussian_0d.py` --- standard normal distribution
	* :red:`val_max_0_gaussian_1d.py` --- standard normal 1D Gaussian fields

	* :red:`val_max_1_onesampleT_0d.py` --- Student's t distribution, from one-sample statistic
	* :red:`val_max_1_onesampleT_1d.py` --- Student's t distribution (1D), from one-sample statistic
	
	* :red:`val_max_2_twosampleT_0d.py` --- Student's t distribution, from one-sample statistic
	* :red:`val_max_2_twosampleT_1d.py` --- Student's t distribution (1D), from two-sample statistic
	
	* :red:`val_max_3_regress_0d.py` --- Student's t distribution, from linear regression
	* :red:`val_max_3_regress_1d.py` --- Student's t distribution (1D), from linear regression
	
	* :red:`val_max_4_anova1_0d.py` --- Fisher-Snedecor F distribution, from one-way design
	* :red:`val_max_4_anova1_1d.py` --- Fisher-Snedecor F distribution (1D), from one-way design
	
	* :red:`val_max_5_onesampleT2_0d.py` --- Hotelling's T-squared distribution, from one-way design
	* :red:`val_max_5_onesampleT2_1d.py` --- Hotelling's T-squared distribution (1D), from one-way design
	
	* :red:`val_max_6_twosampleT2_0d.py` --- Hotelling's T-squared distribution, from two-way design
	* :red:`val_max_6_twosampleT2_1d.py` --- Hotelling's T-squared distribution (1D), from two-way design
	
	* :red:`val_max_7_cca_0d.py` --- chi-squared distribution, from CCA
	* :red:`val_max_7_cca_1d.py` --- chi-squared distribution (1D), from CCA
	
	* :red:`val_max_8_manova1_0d.py` --- chi-squared distribution, from one-way MANOVA
	* :red:`val_max_8_manova1_1d.py` --- chi-squared distribution (1D), from one-way MANOVA
	


.. _label-Scripts-UPX:

Validation (upcrossing extents)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	* :red:`val_upx_0_gauss_cluster.py` --- cluster-level inference (Gaussian fields)
	* :red:`val_upx_0_gauss_set.py` --- set-level inference (Gaussian fields)

	* :red:`val_upx_1_t_cluster.py` --- cluster-level inference (t fields)
	* :red:`val_upx_1_t_set.py` --- set-level inference (t fields)

	* :red:`val_upx_2_F_cluster.py` --- cluster-level inference (F fields)
	* :red:`val_upx_2_F_set.py` --- set-level inference (F fields)

	* :red:`val_upx_3_T2_cluster.py` --- cluster-level inference (T-squared fields)
	* :red:`val_upx_3_T2_set.py` --- set-level inference (T-squared fields)

	* :red:`val_upx_4_X2_cluster.py` --- cluster-level inference (chi-squared fields)
	* :red:`val_upx_4_X2_set.py` --- set-level inference (chi-squared fields)


.. _label-Scripts-Application:

Example application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	* :red:`weather_0_plotdata.py` --- plot of all experimental temperature fields 
	* :red:`weather_1_rft.py` --- parametric inference using RFT
	* :red:`weater_2_nonparam.py` --- non-parametric inference using permutation
	* :red:`weater_3_wrapped.py` --- parametric inference, assuming a circular field




