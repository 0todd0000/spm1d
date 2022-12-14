
.. _label-API-geom:

rft1d.geom
-------------

.. automodule:: rft1d.geom



Basic geometry functions:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

----------------------------------
bwlabel
----------------------------------

.. autofunction:: rft1d.geom.bwlabel


----------------------------------
estimate_fwhm
----------------------------------

.. autofunction:: rft1d.geom.estimate_fwhm

-----

Field geometry (resel counts)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

----------------------------------
resel_counts
----------------------------------

.. autofunction:: rft1d.geom.resel_counts

-----

----------------------------------
resel conversion functions
----------------------------------

.. autofunction:: rft1d.geom.resels2fwhm
.. autofunction:: rft1d.geom.resels2fwhm_masked
.. autofunction:: rft1d.geom.resels2nelements
.. autofunction:: rft1d.geom.resels2nnodes
.. autofunction:: rft1d.geom.resels2fieldsize

-----

Upcrossing metric calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

----------------------------------
rft1d.geom.ClusterMetricCalculator
----------------------------------

.. autoclass:: rft1d.geom.ClusterMetricCalculator

	.. automethod:: rft1d.geom.ClusterMetricCalculator.cluster_extents
	.. automethod:: rft1d.geom.ClusterMetricCalculator.cluster_minima
	.. automethod:: rft1d.geom.ClusterMetricCalculator.max_cluster_extent
	.. automethod:: rft1d.geom.ClusterMetricCalculator.mean_cluster_extent
	.. automethod:: rft1d.geom.ClusterMetricCalculator.nMaxima
	.. automethod:: rft1d.geom.ClusterMetricCalculator.nSuprathresholdNodes
	.. automethod:: rft1d.geom.ClusterMetricCalculator.nSuprathresholdResels
	.. automethod:: rft1d.geom.ClusterMetricCalculator.nUpcrossings
	.. automethod:: rft1d.geom.ClusterMetricCalculator.nUpcrossingsByExtent
	.. automethod:: rft1d.geom.ClusterMetricCalculator.total_excursion_set_extent

