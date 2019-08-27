
API
===================================

(To navigate this page use the menu on the left)


ManualWarp1D
---------------------------------

.. autoclass:: mwarp1d.ManualWarp1D


Properties
___________

    .. autoproperty:: mwarp1d.ManualWarp1D.amp_r
    .. autoproperty:: mwarp1d.ManualWarp1D.center_r
    .. autoproperty:: mwarp1d.ManualWarp1D.head_r
    .. autoproperty:: mwarp1d.ManualWarp1D.tail_r
    
Methods
___________
    
    .. automethod:: mwarp1d.ManualWarp1D.__init__
    .. automethod:: mwarp1d.ManualWarp1D.apply_warp
    .. automethod:: mwarp1d.ManualWarp1D.get_displacement_field
    .. automethod:: mwarp1d.ManualWarp1D.get_warped_domain
    .. automethod:: mwarp1d.ManualWarp1D.reset
    .. automethod:: mwarp1d.ManualWarp1D.set_amp
    .. automethod:: mwarp1d.ManualWarp1D.set_center
    .. automethod:: mwarp1d.ManualWarp1D.set_head
    .. automethod:: mwarp1d.ManualWarp1D.set_tail


:ref:`Back to top <API>`


Example
___________

.. plot::
	:include-source:

	import numpy as np
	from matplotlib import pyplot as plt
	import mwarp1d

	#define warp:
	Q    = 101                      #domain size
	warp = mwarp1d.ManualWarp1D(Q)  #constrained Gaussian kernel warp object
	warp.set_center(0.25)           #relative warp center (0 to 1)
	warp.set_amp(0.5)               #relative warp amplitude (-1 to 1)
	warp.set_head(0.2)              #relative warp head (0 to 1)
	warp.set_tail(0.2)              #relative warp tail (0 to 1)

	#apply warp:
	y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
	yw   = warp.apply_warp(y)                    #warped 1D observation

	#plot:
	plt.figure()
	ax = plt.axes()
	ax.plot(y, label='Original')
	ax.plot(yw, label='Warped')
	ax.legend()
	ax.set_xlabel('Domain position  (%)', size=13)
	ax.set_ylabel('Dependent variable value', size=13)
	plt.show()



:ref:`Back to top <API>`


SequentialManualWarp
---------------------------------

.. autoclass:: mwarp1d.SequentialManualWarp



Methods -
_____________

    .. automethod:: mwarp1d.SequentialManualWarp.append
    .. automethod:: mwarp1d.SequentialManualWarp.apply_warp_sequence
    .. automethod:: mwarp1d.SequentialManualWarp.reset


Example -
_____________

.. plot::
	:include-source:

	import numpy as np
	from matplotlib import pyplot as plt
	import mwarp1d


	#define first warp:
	Q     = 101                      #domain size
	warp0 = mwarp1d.ManualWarp1D(Q)  #constrained Gaussian kernel warp object
	warp0.set_center(0.10)           #relative warp center (0 to 1)
	warp0.set_amp(0.3)               #relative warp amplitude (-1 to 1)
	warp0.set_head(0.0)              #relative warp head (0 to 1)
	warp0.set_tail(0.0)              #relative warp tail (0 to 1)

	#define second warp:
	warp1 = mwarp1d.ManualWarp1D(Q)
	warp1.set_center(0.90)
	warp1.set_amp(-0.3)
	warp1.set_head(0.0)
	warp1.set_tail(0.0)

	#create and apply sequential warps
	seq   = mwarp1d.SequentialManualWarp()
	seq.append( warp0 )
	seq.append( warp1 )
	y     = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
	yw    = seq.apply_warp_sequence(y)            #sequentially warped 1D observation

	#plot:
	plt.figure()
	ax = plt.axes()
	ax.plot(y, label='Original')
	ax.plot(yw, label='Warped')
	ax.legend()
	ax.set_xlabel('Domain position  (%)', size=13)
	ax.set_ylabel('Dependent variable value', size=13)
	plt.show()




:ref:`Back to top <API>`




gaussian_half_kernel
---------------------------------

.. autofunction:: mwarp1d.gaussian_half_kernel



.. plot::

	>>> from matplotlib import pyplot as plt
	>>> import mwarp1d
	>>> 
	>>> k = mwarp1d.gaussian_half_kernel(10, 3, 51, reverse=True)
	>>> 
	>>> plt.figure()
	>>> plt.plot(k)
	>>> plt.show()




:ref:`Back to top <API>`




interp1d
---------------------------------

.. autofunction:: mwarp1d.interp1d

.. plot::

	>>> from matplotlib import pyplot as plt
	>>> import mwarp1d
	>>> 
	>>> k = mwarp1d.gaussian_half_kernel(10, 3, 51, reverse=True)
	>>> ki = mwarp1d.interp1d(k, 200)
	>>> 
	>>> plt.figure()
	>>> plt.plot(k, label='Original')
	>>> plt.plot(ki, label='Interpolated')
	>>> plt.legend()
	>>> plt.show()




:ref:`Back to top <API>`




launch_gui
---------------------------------

.. autofunction:: mwarp1d.launch_gui


:ref:`Back to top <API>`


loadnpz
---------------------------------

.. autofunction:: mwarp1d.loadnpz


:ref:`Back to top <API>`



warp_landmark
---------------------------------

.. autofunction:: mwarp1d.warp_landmark

.. plot::

	import numpy as np
	from matplotlib import pyplot as plt
	import mwarp1d
	
	#define landmarks:
	Q    = 101         #domain size
	x0   = [38, 63]    #initial landmark locations
	x1   = [25, 68]    #final landmark locations
	
	#apply warp:
	y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
	yw   = mwarp1d.warp_landmark(y, x0, x1)      #warped 1D observation
	
	#plot:
	plt.figure()
	ax    = plt.axes()
	c0,c1 = 'blue', 'orange'
	ax.plot(y,  color=c0, label='Original')
	ax.plot(yw, color=c1, label='Warped')
	[ax.plot(xx, y[xx],  'o', color=c0)  for xx in x0]
	[ax.plot(xx, yw[xx], 'o', color=c1)    for xx in x1]
	ax.legend()
	ax.set_xlabel('Domain position  (%)', size=13)
	ax.set_ylabel('Dependent variable value', size=13)
	plt.show()



:ref:`Back to top <API>`



warp_manual
---------------------------------

.. autofunction:: mwarp1d.warp_manual

.. plot::

	from matplotlib import pyplot as plt
	import mwarp1d

	#define warp:
	Q      = 101
	center = 0.25
	amp    = 0.5
	head   = 0.2
	tail   = 0.2

	#apply warp:
	y    = np.sin( np.linspace(0, 4*np.pi, Q) )  #an arbitary 1D observation
	yw   = mwarp1d.warp_manual(y, center, amp, head, tail) #warped 1D observation

	#plot:
	plt.figure()
	ax = plt.axes()
	ax.plot(y, label='Original')
	ax.plot(yw, label='Warped')
	ax.legend()
	ax.set_xlabel('Domain position  (%)', size=13)
	ax.set_ylabel('Dependent variable value', size=13)
	plt.show()



:ref:`Back to top <API>`


