#######################################################################
# Trigonometric graphs v1.0
#
#   This program plots standard trigonometric functions with different
#   resolution, using matplotlib and numpy libraries.
#   Users can specify by command line:
#		- number of graphs to plot
#   	- number of graphs for every column to plot
#		- minimum number of samples
#		- increasing step from one graph to each other
#
# Author: Davide Valeriani
#         University of Essex
# 
#######################################################################

# Import needed libraries
import matplotlib.pyplot as plt
from numpy import *
import sys

# Default configuration
mx = 10		# Number of graphs to plot
cols = 4	# Number of graphs for every column
start = 5	# Minimum number of points
step = 5	# Step for every graph

# Load user configuration
if len(sys.argv) > 1:
	mx = int(sys.argv[1])
if len(sys.argv) > 2:
	cols = int(sys.argv[2])
if len(sys.argv) > 3:
	start = int(sys.argv[3])
if len(sys.argv) > 4:
	step = int(sys.argv[4])
if len(sys.argv) > 5:	
	print "Using "+str(sys.argv[0])+" [# graphs] [# graphs for every column] [minimum # of samples] [sample step]"
	exit()
	
# Calculate the number of needed rows
if (mx % cols == 0):
	rows = mx / cols
else:
	rows = mx / cols + 1

# Separate one graph to each other by 0.7 cm
plt.subplots_adjust(hspace=.7)

# Iterate on graphs to plot
for i in range(mx):
	# Calculate the sample values
	x = linspace(0,2*pi,start+i*step)
	# Functions to plot with relative labels and colors
	funct = array([(sin(x), cos(x), sin(x)*sin(x), cos(x)*cos(x), sin(x)*cos(x)),
			 ('$sin(x)$', '$cos(x)$', '$sin^2(x)$', '$cos^2(x)$', '$sin(x)*cos(x)$'),
			 ('red', 'blue', 'green', 'purple', 'magenta')])
	# Arrange the plot
	plt.subplot(rows,cols,i+1)
	# Set axis
	plt.axis([0,start+i*step,-2.5,2.5])
	# Set title of the graph
	plt.title('# points = '+str(start+i*step))
	# For every function to plot
	for j in range(funct.shape[1]):
		# Insert legend value
		plt.text(0.2,(-2.3+j*0.3),funct[1,j],color=funct[2,j])
		# Plot the respective function
		plt.plot(funct[0,j],funct[2,j])

# Show the figure
plt.show()
