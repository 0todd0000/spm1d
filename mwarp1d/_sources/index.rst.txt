
mwarp1d
===================================


Manual one-dimensional data warping and nonlinear registration in `Python <https://www.python.org>`_ and `PyQt <https://www.riverbankcomputing.com/software/pyqt/intro>`_.

Source code is available in this project's `GitHub repository <https://github.com/0todd0000/mwarp1d>`_

.. image:: _static/ss0.png
   :height: 679 px
   :width: 970 px
   :scale: 40 %
   :alt: screenshot
   :align: center

**mwarp1d** provides a collection of GUI and scripting tools for manually warping 1D data,
mainly for the purpose of nonlinear registration. As alternatives, a variety of algorithmic
approaches to nonlinear 1D registration are available including:

* `Minimium eigenvalue <http://www.psych.mcgill.ca/misc/fda/>`_ (Ramsay & Silverman 2005)
* `Fisher-Rao square root velocity transform <http://ssamg.stat.fsu.edu/software>`_ (Srivastava, Jermyn, & Joshi 2007)
* `K-mean alignment <https://cran.r-project.org/web/packages/fdakma/index.html>`_ (Parodi et al. 2014)
* `Multi-level clusters <https://github.com/julia-wrobel/registr>`_ (Wrobelm 2018)

**Please cite**:

Pataky TC, Naouma H, Donnelly CJ (in review). mwarp1d: Manual one-dimensional data warping in Python and PyQt. Journal of Open Source Software. `Journal of Open Source Software <https://joss.theoj.org>`_.



Contents
---------------------

.. toctree::
   :maxdepth: 2
   
   installation.rst
   quickstart.rst
   usermanual.rst
   examples.rst
   api.rst
   support.rst


.. Indices and tables
.. ---------------------
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
