.. _label-NewFeatures:


New Features (version 0.3.2)
=====================================

Region-of-Interest (ROI) analysis.

All statistical routines in **spm1d.stats** now accept a keyword "roi" for conducting ROI analysis.

More details will be released after peer review.





New Features (version 0.3.1)
=====================================

This update contains major edits to the ANOVA code.

1. Newly supported ANOVA models:

* **spm1d.stats.anova3rm**  (three-way design with repeated-measures on all three factors)
* **spm1d.stats.anova2onerm**  (now supports unbalanced designs:  i.e. different numbers of subjects for each level of factor A)


2. WARNING:  Repeated-measures ANOVA

* IF (a) the data are 1D and (b) there is only one observation per subject and per condition...
* THEN inference is approximate, based on approximated residuals.
* TO AVOID THIS PROBLEM:  use multiple observations per subject per condition, and the same number of observations across all subjects and conditions.

3. WARNING:  Non-sphericity corrections

* Now only available for two-sample t tests and one-way ANOVA.
* The correction for one-way ANOVA is approximate and has not been validated.
* Non-sphericity corrections for other designs are currently being checked.




.. plot::
	:include-source:
	
	import numpy as np
	from matplotlib import pyplot

	x = np.random.randn(10)
	pyplot.plot(x)





