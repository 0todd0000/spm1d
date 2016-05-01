
.. _label-VersionHistory:

.. note:: Legacy versions of **spm1d** (0.1, 0.2 and M.0.1) are neither supported not available for download. 

	This document simply provides release information for users interested in **spm1d**'s developmental history.


------------------------

Version 0.3  (Python and MATLAB)
-----------------------------------

Released **2015.07.01**

:ref:`Click here <label-NewFeatures>` for descriptions of new features.

As of version 0.3 all version history notes now exist on `spm1d's github site <https://github.com/0todd0000/spm1d/>`_.


------------------------

Version 0.2  (Python)
-----------------------------------

Released **2014.08.25**

* Two-way ANOVA
* Non-sphericity corrections
* Improved plotting
* Detailed inference information



**Version 0.2.0006**  (2014.07.09):   Added a "h0reject" attribute to SPM inference objects to specify null hypothesis rejection decision.

**Version 0.2.0005**  (2014.06.24):   Fixed a plotting bug which generated a "No paths provided" error if (a) an SPM object contains no suprathreshold clusters and (b) plotting is conducted in Spyder for Windows.

**Version 0.2.0004**  (2014.06.11):   Added data check to all stats routines, including checks for zero variance nodes.

**Version 0.2.0003**  (2014.06.04):   Updated to be be compatible with scipy version 0.14

**Version 0.2.0002**  (2014.05.27):   Fixed a bug which returned p values of 2.0 when the entire field exceeds the threshold

**Version 0.2.0001**  (2014.05.25)

- plotting functions now automatically scale the axis y limits by default
- fixed a bug in one-way ANOVA which produced an error when testing more than three treatments/groups
- fixed a bug in two-way ANOVA (main effects model) which produced an error when testing more than two levels of Factor A


------------------------

Version M.0.1  (MATLAB)
-----------------------------------

Released **2014.05.25**


**Version M0.2.0005**  (2014.11.28):   Fixed an infinite value bug in ./spm1d/spm8/inference/spm_uc_RF.m to be compatible with recent Matlab versions.

**Version M0.1.0004** (2014.07.09):   Added a "h0reject" field to SPM inference structures to specify null hypothesis rejection decision.

**Version M0.1.0003** (2014.06.27):   Fixed an "extents" error that can appear when running ANOVA.

**Version M0.1.0002** (2014.06.10):   Added a feature:  SPM inference structures now include cluster extents.

**Version M0.1.0001** (2014.05.29):   Fixed a bug which returned p values of NaN when the entire field exceeds the threshold



------------------------

Version 0.1  (Python)
-----------------------------------

Released **2010.12.01**

Basic data IO, plotting, and statistical tests (t tests, regression, one-way ANOVA, and general linear modelling).


