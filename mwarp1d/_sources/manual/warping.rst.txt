
Warping
===================================

Landmark warping
----------------------------

Step 1:  Define template landmarks
_____________________________________

* Add landmark:   Left-click outside template

* Delete landmark:  Right-click on a landmark

* Move landmark:  Left-click and drag landmark

* Finish:  L to lock template (Points cannot be added after locking template!)



Step 2:  Adjust source templates
_____________________________________

* Move landmarks to homologous locations on each source

* Select source:  left-click on line  OR use arrow keys to cycle through sources OR click on relevant row from the table

* Move landmark:  Left-click and drag landmark



Manual warping
----------------------------

Manual (Gaussian-kernel-based) warps are defined using four parameters:

* **y** --- original 1D data
* **center** --- warp kernel center, relative to its feasible range (between 0 and 1)
* **amp** --- warp kernel amplitude, relative to its feasible range (between -1 and 1)
* **head** --- warp kernel head width, relative to its feasible range (between 0 and 1)
* **tail** --- warp kernel tail width, relative to its feasible range (between 0 and 1)

The meaning of these four parameters is depicted in the figure below.

.. plot::

	import numpy as np
	from matplotlib import pyplot as plt
	import mwarp1d

	#plot:
	plt.close('all')
	plt.figure()
	ax     = plt.axes()

	#plot example pulse:
	w = mwarp1d.ManualWarp1D(100)
	w.set_center(0.20)
	w.set_amp(0.25)
	w.set_head(0.9)
	w.set_tail(0.3)
	dq = w.get_displacement_field()
	ax.plot(dq, color='b')
	ax.set_xlabel('Domain position  (%)', size=13)
	ax.set_ylabel('Displacement  (%)', size=13)
	# label parameters:
	c = w.center
	ax.plot([0,c], [0,0], color='k', ls=':')
	ax.plot([c]*2, [0,dq.max()], color='k', ls=':')
	xh,xt = 10,58
	ax.plot([xh,c], [dq[xh]]*2, color='k', ls=':')
	ax.plot([c,xt], [dq[xt]]*2, color='k', ls=':')
	# print(dq[xh]/dq.max(), dq[xt]/dq.max())


	bbox = dict(facecolor='w', edgecolor='0.7', alpha=0.9)
	ax.text(0.5*c, 0, 'center', ha='center', bbox=bbox)
	ax.text(c, 0.8*dq.max(), 'amp', ha='center', bbox=bbox)
	ax.text(0.5*(xh+c), dq[xh], 'head', ha='center', bbox=bbox)
	ax.text(c + 0.5*(xt-c), dq[xt], 'tail', ha='center', bbox=bbox)
	ax.legend(['Displacement field'])

	plt.show()


In order to conduct manual warping, follow the steps below.

See also the :ref:`manual warping <Manual warping (screencast)>` screencast.


Step 1:  Position the mouse 
_____________________________________

* Move the mouse on the axes to the position at which you wish to initiate the warp. This will set the ``center`` parameter.



Step 2:  Initiate the warp
_____________________________________

* Press the "W" key to initiate a manual warp.


Step 3:  Adjust the warp
_____________________________________

* Drag the mouse left-and-right to adjust the ``amp`` parameter.

* Drag the mouse up-and-down to adjust the ``head`` and ``tail`` parameters.


Step 4:  Finalize the warp
_____________________________________

* Press "Enter" to apply the warp.  Alternatively press "ESC" to cancel the warp.


Step 5:  Restore to original data
_____________________________________

* If you are unhappy with the warp results, press "R" to restore the original data.

* This will delete all existing warps for the currently selected curve.






Restoring previous sessions
----------------------------

If something went wrong during warping (e.g. a software crash), or if you would like to revisit previous warping sessions, then:

1. Launch **mwarp1d**

2. Drag a previous session's :ref:`output (NPZ) <Specifying output directory>` file on to the main window's :ref:`Drop Data box <Importing data>`. 


This will restore the previous session, allowing you to adjust and/or reset the previously saved warps.






