#!/usr/bin/python

from scipy import *
from numpy import *
from pylab import *
import os, sys
from scipy.optimize import curve_fit

# Fitting Curve | 
def func(x, a, b, c, d):
	return a*exp(-(((x-b)**2)/((2*c)**2))) + d

# Fitting Curve | 
def func2(x, a, b, c):
	return a + b*x*exp(-c*x)
	
# Fitting Curve | 
def func1(x, a, b, c, d):
	return a + b*exp(-c*x+d)

tableau10 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40), (148, 103, 189), 
			(140, 86, 75), (227, 119, 194), (127, 127, 127), (188, 189, 34), (23, 190, 207)]  

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau10)):
	r, g, b = tableau10[i]  
	tableau10[i] = (r / 255., g / 255., b / 255.) 

colorScheme = 'white'
if colorScheme == 'black':
	txtcolor = 'white'
	axiscolor = '#777777'
	lw = 0.4
elif colorScheme == 'white':
	txtcolor = 'black'
	axiscolor = 'black'
	lw = 0.5

rcParams['figure.figsize'] = 5,6
params = {'legend.fontsize': 12, 'legend.linewidth': 1, 'xtick.major.size': 2, 'xtick.major.width': 0.5, 'legend.frameon':False,
		  'axes.linewidth':lw, 'axes.labelsize':12, 'xtick.labelsize':12, 'ytick.labelsize':12, 'font.size':14}
rcParams.update(params)
nSubPlots = 2

# smoothing
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth



resultsdir = "results/RP20V80/"
modelfolders = os.listdir(resultsdir)
modelfolders = [e for e in modelfolders if os.path.isdir(resultsdir+e)]
if 'Plots' in modelfolders:
	modelfolders.remove('Plots')

#outputdir = "output/RyR/"
#outmodels = os.listdir(outputdir)
#outmodels = [f for f in outmodels if os.path.isdir(outputdir+f)]

outfilename = "P2_plot.dat"

all_rels_unp = []
all_rels = []
all_rels_p = []
x_data = []
y_data = []
p2_data = [[],[]]

for k in range(len(modelfolders)):
	all_rels_p.append(np.genfromtxt(resultsdir+modelfolders[k]+"/all_rels/rel_all_assorted.dat", skip_header=1))
	
	all_rels_unp.append(np.genfromtxt(resultsdir+modelfolders[k]+"/all_rels/rel_all_assorted.dat", skip_header=1, unpack=1))

for l in range(len(all_rels_unp)):
	x_data.append(all_rels_unp[l][0])
	p2_data[0].append(all_rels_unp[0])

for m in range(len(all_rels_unp)):
	y_data.append(all_rels_unp[m][12])

popt, pcov = curve_fit(func, x_data, y_data, (0.08, 250, 100, 0.15))
x = linspace(0,200,1000)
#popt = [1, 1, 0.01, 1]
y = func(x_data, *popt)
plot(x_data,y, color=tableau10[i], lw=lw)
print popt
#plt.show()
