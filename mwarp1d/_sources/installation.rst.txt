
Installation
===================================



Anaconda
---------------------

.. code::

	conda install -c toddp mwarp1d

Link to **mwarp1d** in the `Anaconda Cloud <https://anaconda.org/toddp/mwarp1d>`_


Dependencies
---------------------

- `NumPy 1.16 <https://numpy.org>`_
- `SciPy 1.3 <https://www.scipy.org>`_
- `Matplotlib 3.1 <https://matplotlib.org>`_

These dependencies are included with the Anaconda distribution.

If, for some reason, you have removed these dependencies from Anaconda, installing :code:`mwarp1d` using :code:`conda` (see above) will automatically handle their installation.


Source code
---------------------

Source code is available in this project's `GitHub repository <https://github.com/0todd0000/mwarp1d>`_



New to Python?
---------------------

Refer to the instructions below and also the :ref:`Installation <Installation (screencast)>` and :ref:`Launching <Launching mwarp1d (screencast)>` screencasts.


The easiest way to use **mwarp1d** is to:

1. Install `Anaconda <https://anaconda.org>`_  (detailed instructions `here <https://docs.anaconda.com/anaconda/install/>`_)
2. Open the Anaconda Prompt (`Windows <https://docs.anaconda.com/anaconda/user-guide/getting-started/#write-a-python-program-using-anaconda-prompt-or-terminal>`_) or a Terminal (Mac, Linux), then enter:

.. code::

	conda install -c toddp mwarp1d
	
3. Run Python by entering :code:`python` in the Anaconda Prompt (Windows) or Terminal (Mac, Linux)

4. Enter the commands below to launch **mwarp1d**

.. code::

	>>> import mwarp1d
	>>> mwarp1d.launch_gui()
	
If the **mwarp1d** GUI launches without errors, proceed to the :ref:`Example data <Example data (screencast)>` screencast.
