
RFT Overview
============================================


RFT describes the probabilities that smooth, random fields will:

	(1)  reach particular heights, and 
	(2)  produce upcrossings which extend beyond particular heights and which have particular geometric features.

The random fields can lie in arbitrary *n*-dimensional spaces, but **rft1d** considers
only the relatively simple cases of broken (piecewise continuous) and unbroken (continuous) 1D fields.
RFT probabilities stem from the expected Euler characteristic of thresholded Guassian random fields
:ref:`(Adler and Hasofer, 1976)  <label-RFTliterature>`, and this expectation leads to
probabilistic descriptions of various geometric features of upcrossings 
:ref:`(see the Literature section for for other key papers)<label-RFTliterature>`.
Since RFT extends the Gaussian distribution to 1D (and *n*\ D) fields, it allows one to generalize
common parametric procedures like regression and ANOVA to the field level.





Gaussian random fields
-----------------------------------

Gaussian fields (figure below) are Gaussian at each point in the field,
and have arbitrary smoothness. To generate a 1D Gaussian field:

	* Produce a sequence of uncorrelated Gaussian values [Panel (a)]
	* Convolve the uncorrelated Gaussian values with a Gaussian kernel of known FWHM
	* Rescale the convolved field to unit variance based on the expected kernel variance.

The FWHM is full-width-at-half-maximum of the smoothing kernel
and is related to the standard deviation (:math:`\sigma`) of the kernel via the identity:

	.. math::

		FWHM =  \sqrt{8 \log 2} \sigma \approx 2.4 \sigma

Inifinitely smooth Gaussian fields [Panel (f) below] are equivalent to Gaussian scalars.
In Python uncorrelated Gaussan fields can be produced using **numpy.random.randn**
and they can be smoothed conveniently using **scipy.ndimage.gaussian_filter1d**
as demonstrated in the :ref:`random field generation scripts  <label-Scripts-RFs>`.


.. note:: Whereas a 0D Gaussian process is parameterized by only the mean :math:`\mu` and standard deviation :math:`\sigma`, a smooth 1D Gaussian process is fully parameterized by just one additional parameter: the FHWM.



.. plot:: pyplots/fig_continua1d.py







Expected field maximum
-----------------------------------

In the figure above it is apparent that random field extrema tend to become less extreme
as the field gets smoother.
The figure below emphasizes that the probability that the field maximum (z_max)
reaches a particular height depends on field smoothness.

.. plot:: pyplots/fig_val_maxima_fwhm.py




.. _label-Theory-Upcrossings:

Upcrossings
-----------------------------------

After thresholding a random field at a particular height *u*,
one or more "upcrossings" may survive that threshold as depicted in the figure below.
An upcrossing may be described as a connected set or "cluster" of supra-threshold nodes.
Each upcrossing possesses a number of geometrical features including especially: maximum height and extent.


.. plot:: pyplots/fig_upcrossing.py



Expected upcrossing geometry
-----------------------------------

RFT describes not only the expected random field maxima, but also expected upcrossing geometry.
Through those expectations RFT yields probabilities regarding various upcrossing features
including extent. The figure below depicts the probability that Gaussian fields
(*FWHM* = 10.0) will produce upcrossings with an extent (k) when thresholded at *u*. 

**rft1d** contains functions and classes for exploring a variety of RFT probabilities
and expectations. It also contains a number of scripts which validate
these probabilities through simulation. Last, it demonstrates how these probabilities
can be applied to make a variety of statistical inferences regarding experimental
univariate and multivariate test statistic fields.

.. plot:: pyplots/fig_expected_extents.py



