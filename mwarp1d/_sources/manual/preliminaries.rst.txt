
Preliminaries
===================================

Launching
----------------------------

The easiest way to launch the GUI is from Python or iPython:

	>>> import mwarp1d
	>>> mwarp1d.launch_gui()

``launch_gui`` optionally accepts various input arguments as described :ref:`here <Command line UI launching>`.

Alternatively you can launch the GUI using ``./mwwarp1d/ui/main.py`` as follows:


.. code-block::

	python main.py



Importing data
----------------------------

After launching **mwarp1d**, its main window will appear:

.. image:: ../_static/ss1.png
   :height: 1482 px
   :width: 1938 px
   :scale: 30 %
   :alt: screenshot1
   :align: center

To import data, drag-and-drop a CSV file on the "Drop Data File Here" box.

The CSV file must be formatted as follows:

* Only numbers (no column or row headers)
* Rows = observations
* Columns = domain nodes

Thus eight observations, each with 100 domain nodes, would require an (8 x 100) CSV file.




Specifying output directory
----------------------------



After dropping a CSV data file on the "Drop Data File Here" box, the output (Results) file will be automatically set to ``mwarp1d.npz``, in the same directory as the CSV folder, like this:

.. image:: ../_static/ss2.png
   :height: 1482 px
   :width: 1938 px
   :scale: 30 %
   :alt: screenshot2
   :align: center

To change the output directory and/or results file name, simply click on the label.  A file dialog will appear.

Note that all warping results are automatically saved to the NPZ file.

This NPZ file can be used to :ref:`restore previous sessions <Restoring previous sessions>`.



