from matplotlib import pyplot
color_node = 'k'
color_element = 'r'
pyplot.figure(figsize=(4.3,0.8))
ax = pyplot.axes([0,0,1,1])
ax.plot([0,1,2], [0, 0, 0], '-', markersize=10, color=color_element)
ax.plot([0,1,2], [0, 0, 0], 'o', markersize=10, color=color_node)
ax.axis('off')
tx0  = [ax.text(i-0.1,  0.8, 'Node %d'%i, color=color_node)  for i in [0,1,2]]
tx1  = [ax.text(i+0.3, -0.5, 'Element %d'%i, color=color_element)  for i in [0,1]]
pyplot.setp(tx0+tx1, ha='left', va='center', size=12)
pyplot.setp(ax, xlim=(-0.15,2.25), ylim=(-1,1))