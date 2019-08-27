
Command line UI launching
===================================

The function **mwarp1d.launch_gui** can be used to launch the GUI from the command line.
Five argument patterns are supported:

1. launch_gui( )
2. launch_gui( fnameCSV )
3. launch_gui( fnameNPZ )
4. launch_gui( fnameCSV, mode )
5. launch_gui( fnameCSV, mode, fnameNPZ )


The arguments include:

+----------+--------------------------------------------------------------------------+
| **Arg**  | **Description**                                                          |
+==========+==========================================================================+
| fnameCSV |  CSV file name (rows = observations, columns = domain nodes)             |
+----------+--------------------------------------------------------------------------+
| fnameNPZ |  numpy zipped file name into which results will be saved                 |
+----------+--------------------------------------------------------------------------+
| mode     |  “landmark” or “manual”                                                  |
+----------+--------------------------------------------------------------------------+


:Example:

.. code-block::

	import mwarp1d
	
	fnameCSV = "/Users/username/Desktop/mydata.csv"
	mode     = "manual"
	
	mwarp1d.launch_gui( fnameCSV, mode )