
.. _label-API-prob:

rft1d.prob
------------------

.. automodule:: rft1d.prob



Core RFT computations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: rft1d.prob.rft


High-level interface to RFT computations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: rft1d.prob.RFTCalculator

	.. automethod:: rft1d.prob.RFTCalculator.isf
	.. automethod:: rft1d.prob.RFTCalculator.sf

--------------------------------------
Expectations (RFTCalculator.expected)
--------------------------------------

	.. automethod:: rft1d.prob.expected.nodes_per_upcrossing
	.. automethod:: rft1d.prob.expected.number_of_upcrossings
	.. automethod:: rft1d.prob.expected.number_of_suprathreshold_nodes
	.. automethod:: rft1d.prob.expected.number_of_suprathreshold_resels
	.. automethod:: rft1d.prob.expected.resels_per_upcrossing

--------------------------------------
Probabilities (RFTCalculator.p)
--------------------------------------
	
	.. automethod:: rft1d.prob.p.cluster
	.. automethod:: rft1d.prob.p.set
	.. automethod:: rft1d.prob.p.upcrossing
	
Bonferroni correction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	.. automethod:: rft1d.prob.p_bonferroni



