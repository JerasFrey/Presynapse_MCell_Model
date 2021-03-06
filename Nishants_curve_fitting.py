#!/usr/bin/python

from scipy import *
from numpy import *
from pylab import *
import os, sys
from scipy.optimize import curve_fit

# Fitting Curve | 
def func(x, a, b, c, d):
	return a*exp(-(((x-b)**2)/((2*c)**2))) + d
#	return a + b*x**d*exp(-c*x)

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



resultsdir = "results/RyR/"
modelfolders = os.listdir(resultsdir)
modelfolders =[e for e in modelfolders if os.path.isdir(resultsdir+e)]

outputdir = "output/RyR/"
outmodels = os.listdir(outputdir)

outfilename = "P2_plot.dat"

all_rels = []
x_data = []
y_data = []
p2_data = []

for k in range(len(modelfolders)):
	all_rels.append(np.genfromtxt(resultsdir+modelfolders[k]+"/all_rels/rel_all_assorted.dat", skip_header=1, unpack=1))
print np.genfromtxt(resultsdir+modelfolders[k]+"/all_rels/rel_all_assorted.dat", skip_header=1, unpack=1)
for l in range(len(all_rels)):
	p2_data.append([all_rels[l][0], all_rels[l][12]])

print p2_data
np.savetxt(resultsdir+outfilename, p2_data)

popt, pcov = curve_fit(func, p2_data[:,0], p2_data[:,1], (0.08, 250, 100, 0.15))
x = linspace(0,200,1000)
#popt = [1, 1, 0.01, 1]
y = func(p2_data[:,0], *popt)
plot(p2_data[:,0],y, color=tableau10[i], lw=lw)
print popt


'''
			popt, pcov = curve_fit(func, np.array(ts), np.array(ptpData), (0.08, 250, 100, 0.15))
			if i==2:
				popt, pcov = curve_fit(func2, np.array(ts), np.array(ptpData), (2.04, 0.004, 0.0015))
		if row ==1:
			popt, pcov = curve_fit(func, np.array(ts), np.array(ptpData), (2.0, 0.001, 0.003, 1))
			if i==2:
				popt, pcov = curve_fit(func2, np.array(ts), np.array(ptpData), (1.56, 0.09, 0.008))
		x = linspace(0,3500,1000)
		#popt = [2.0, 0.15, 0.003]
		if i==2: y = func2(x, *popt)
		else: y = func(x, *popt)
		ax[row].plot(x,y, color=tableau10[i], lw=lw)
		print popt
		ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)
'''

'''
# Bound Ca 
rcParams['figure.figsize'] = 5,3
ax = gca()
#f.patch.set_facecolor(colorScheme)

setp(ax.spines.values(), color=axiscolor)
setp([ax.get_xticklines(), ax.get_yticklines()], color=axiscolor)
ax.yaxis.label.set_color(txtcolor)
ax.xaxis.label.set_color(txtcolor)
ax.tick_params(axis='x', colors=axiscolor)
ax.tick_params(axis='y', colors=axiscolor)
	
ax.set_xlabel('Time (msec)')

label = ['SERCA | RS', 'SERCA | IS', 'SERCA | S', 'RyR | RS']
files = ["c250/RSI20V80/sercaMol.dat", "c250/IP3SI20V80/sercaMol.dat", "c250/SI20V80/sercaMol.dat","c250/RSI20V80/ryrMol.dat"]
datarf = genfromtxt("c250/RSI20V80/ryrCaFlux.dat")
for i, file in enumerate(files):
	data = genfromtxt(file)
	if i == 3:
		plot(data[:,0]*1000, datarf[:,1]-datarf[:,2]-(data[:,3]+data[:,4]+data[:,5]+data[:,6]+data[:,7]+data[:,8]+2*(data[:,11]+data[:,13])+2*(data[:,12]+data[:,14]))+8, lw=0.4, color=tableau10[i], label=label[i])
	else:
		plot(data[:,0]*1000, data[:,2]+data[:,5]+2*(data[:,3]+data[:,4]), lw=0.4, color=tableau10[i], label=label[i])
	ax.set_ylabel('Ca bound to SERCA and Cumulative Ca flux from RyR (num)')
	l = ax.legend()
	l.get_frame().set_facecolor(colorScheme)
	for j, text in enumerate(l.get_texts()):
		text.set_color(tableau10[j])

savefig('SercaboundCa.eps', format='eps', dpi=300)
#show()
'''
'''
# Facilitation
def stimProtocol(d):
	s = d.split("_")
	n = int(s[1])
	isi = 1000/float(s[2].split("hz")[0])
	if "ms" in s[3]:
		ptd = float(s[3].split("ms")[0])
	else:
		ptd = float(s[3].split("s")[0])*1000
	
	ts = [i*isi for i in range(n)]
	ts.append((n-1)*isi+ptd)
	ts = [(i+2.5) for i in ts]
	
	return ts
	
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)
	
subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.4, hspace=None)
ax[-1].set_xlabel('Time (msec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS","c1000/train/RS", "c250/train/NS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		ts = stimProtocol(dir)
		ptpData = genfromtxt(dir + '/result')
		ptpData /= float(ptpData[0])
		ax[row].plot(ts,ptpData, '.', color=tableau10[i], label=label[i])
		ax[row].set_ylabel('Facilitation ($n^{th}/1^{st})$')
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
		if row == 0:
			popt, pcov = curve_fit(func, np.array(ts), np.array(ptpData), (0.08, 250, 100, 0.15))
			if i==2:
				popt, pcov = curve_fit(func2, np.array(ts), np.array(ptpData), (2.04, 0.004, 0.0015))
		if row ==1:
			popt, pcov = curve_fit(func, np.array(ts), np.array(ptpData), (2.0, 0.001, 0.003, 1))
			if i==2:
				popt, pcov = curve_fit(func2, np.array(ts), np.array(ptpData), (1.56, 0.09, 0.008))
		x = linspace(0,3500,1000)
		#popt = [2.0, 0.15, 0.003]
		if i==2: y = func2(x, *popt)
		else: y = func(x, *popt)
		ax[row].plot(x,y, color=tableau10[i], lw=lw)
		print popt
		ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)

ax[-1].set_xlim(0,ts[-1])
savefig('fittedFacilitation.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()
'''
'''
# RRP
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)

subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.1, hspace=None)
ax[-1].set_xlabel('Time (sec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS", "c1000/train/RS", "c250/train/NS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		rrpData = genfromtxt(dir + '/rrp.dat')
		ax[row].plot(rrpData[:,0], rrpData[:,1], lw=lw, color=tableau10[i], label=label[i])
		ax[row].set_ylabel('RRP (num)') 
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
			
	ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)
	ax[row].set_xlim(0,rrpData[-1,0])
	
savefig('rrp.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()

# Cytosol [Ca]
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)
	
subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.4, hspace=None)
ax[-1].set_xlabel('Time (sec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS", "c1000/train/RS", "c250/train/NS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		lCaData = genfromtxt(dir + '/CaConc')
		ax[row].set_xlim(0,0.7/(1+row))
		ax[row].set_ylim(0,0.7+0.4*row)
		ax[row].plot(lCaData[:,0], smooth(lCaData[:,1], 50), lw=0.2, color=tableau10[i], label=label[i])
		ax[row].set_ylabel('[Ca$^{2+}$]$_{cyt}$ ($\mu$M)')
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
	ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)

#ax[-1].set_xlim(0,lCaData[-1,0])
savefig('CaCytosolBase1.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()


# Ca Flux through RyR
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)
	
subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.4, hspace=None)
ax[-1].set_xlabel('Time (sec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS", "c1000/train/RS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		ryrCaFluxData = genfromtxt(dir + '/ryrCaFlux.dat')
		ax[row].plot(ryrCaFluxData[:,0], ryrCaFluxData[:,1], lw=lw, color=tableau10[i], label=label[i])
		ax[row].set_ylabel('RyR Ca Cumulative. Flux (num)')
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
	ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)
	ax[row].set_xlim(0,3.0/(row+1))

savefig('CaRyRFlux.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()

# Open RyR
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)
	
subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.4, hspace=None)
ax[-1].set_xlabel('Time (sec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS", "c1000/train/RS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		openRyrData = genfromtxt(dir + '/ryrMol.dat')
		ax[row].plot(openRyrData[:,0], [j[6]+j[7]+j[8]+j[13]+j[14] for j in openRyrData], lw=lw, color=tableau10[i], label=label[i])
		ax[row].set_ylabel('Open RyR Channels')
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
	ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)
	ax[row].set_xlim(0,3.0/(row+1))
	
savefig('openRyR.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()


# ER [Ca]
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)
	
subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.4, hspace=None)
ax[-1].set_xlabel('Time (sec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS", "c1000/train/RS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		ERCaData = genfromtxt(dir + '/ca.dat')
		ax[row].plot(ERCaData[:,0], [j/23.47 for j in ERCaData[:,3]], lw=lw, color=tableau10[i], label=label[i])
		ax[row].set_ylabel('[Ca$^{2+}$]$_{ER}$ ($\mu$M)')
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
	ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)
	ax[row].set_xlim(0,3.0/(row+1))
	
savefig('CaER.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()

# Cumulative Vesicle Release (histogram)
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)
	
subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.4, hspace=None)
ax[-1].set_xlabel('Time (sec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS", "c1000/train/RS", "c250/train/NS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		vesRelData = genfromtxt(dir + '/vesRel')
		lCaData = genfromtxt(dir + '/CaConc',usecols = (0))
		nBin = int(lCaData[-1]/0.005)
		n, bins, patches = ax[row].hist(vesRelData[:,0], nBin, lw=lw, histtype='step', cumulative=True, color=tableau10[i], label=label[i])
		ax[row].set_ylabel('Cumulative Vesicles Release (Total)')
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
	ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)
	ax[row].set_xlim(0,3.0/(row+1))
	legend(loc='upper left', frameon=False)
		
savefig('vesicleRelCumul.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()

# Vesicle Release (histogram)
rcParams['figure.figsize'] = 5,3
f, ax = subplots(nSubPlots)
f.patch.set_facecolor(colorScheme)
for i in range(nSubPlots):
	setp(ax[i].spines.values(), color=axiscolor)
	setp([ax[i].get_xticklines(), ax[i].get_yticklines()], color=axiscolor)
	ax[i].yaxis.label.set_color(txtcolor)
	ax[i].xaxis.label.set_color(txtcolor)
	ax[i].tick_params(axis='x', colors=axiscolor)
	ax[i].tick_params(axis='y', colors=axiscolor)
	
subplots_adjust(left=None, bottom=0.08, right=0.95, top=0.97, wspace=0.4, hspace=None)
ax[-1].set_xlabel('Time (sec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS']
dirs = ["c250/train/RS", "c500/train/RS", "c1000/train/RS", "c250/train/NS"]
for row, freq in enumerate(["10hz", "20hz"]):
	for i, d in enumerate(dirs):
		dir = d + "_30_" + freq + "_100ms"
		if i == 2: dir = d + "_30_" + freq + "_500ms"
		vesRelData = genfromtxt(dir + '/vesRel')
		lCaData = genfromtxt(dir + '/CaConc',usecols = (0))
		nBin = int(lCaData[-1]/0.02)
		n, bins, patches = ax[row].hist(vesRelData[:,0], nBin, lw=lw, histtype='step', color=tableau10[i], label=label[i])
		ax[row].set_ylabel('Vesicles Release (Total)')
		l = ax[row].legend()
		l.get_frame().set_facecolor(colorScheme)
		for j, text in enumerate(l.get_texts()):
			text.set_color(tableau10[j])
	ax[row].text(ax[row].get_xlim()[1]/2.0, ax[row].get_ylim()[1], freq, color=txtcolor)
	ax[row].set_xlim(0,lCaData[-1])
	
savefig('vesicleRel.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
#show()
'''
'''
# ISI Vs PPF
rcParams['figure.figsize'] = 5,4.3
ax = gca()
#f.patch.set_facecolor(colorScheme)

setp(ax.spines.values(), color=axiscolor)
setp([ax.get_xticklines(), ax.get_yticklines()], color=axiscolor)
ax.yaxis.label.set_color(txtcolor)
ax.xaxis.label.set_color(txtcolor)
ax.tick_params(axis='x', colors=axiscolor)
ax.tick_params(axis='y', colors=axiscolor)
	
ax.set_xlabel('ISI (msec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS', '2*RyR1000']
files = ["c250/RSdata.dat", "c500/RSdata.dat", "c1000/RSdata.dat", "c250/NSdata.dat", "c1000/c1000/f2/RSdata.dat"]
for i, file in enumerate(files):
	data = genfromtxt(file,usecols = (13,14,15))
	data = sorted(data, key=lambda x: x[1])
	isi = []
	ppf = []
	for d in data:
		if d[2] == 80:
			isi.append(d[1])
			ppf.append(d[0])
	
	plot(isi, ppf, '.', color=tableau10[i], label=label[i])
	ax.set_ylabel('PPF')
	l = ax.legend()
	l.get_frame().set_facecolor(colorScheme)
	for j, text in enumerate(l.get_texts()):
		text.set_color(tableau10[j])
		
	popt, pcov = curve_fit(func1, np.array(isi), np.array(ppf), (1.4, 1, 0.01, 1))
	x = linspace(0,200,1000)
	#popt = [1, 1, 0.01, 1]
	y = func1(x, *popt)
	ax.plot(x,y, color=tableau10[i], lw=lw)
	print popt
	
savefig('ISIvsPPF.eps', format='eps', dpi=300)
#show()
'''
'''
# Ca Profile Overload
rcParams['figure.figsize'] = 5,4.3
ax = gca()
#f.patch.set_facecolor(colorScheme)

setp(ax.spines.values(), color=axiscolor)
setp([ax.get_xticklines(), ax.get_yticklines()], color=axiscolor)
ax.yaxis.label.set_color(txtcolor)
ax.xaxis.label.set_color(txtcolor)
ax.tick_params(axis='x', colors=axiscolor)
ax.tick_params(axis='y', colors=axiscolor)
	
ax.set_xlabel('Time (msec)')

label = ['RyR250', 'RyR500', 'RyR1000', 'NS', '2*RyR1000']
files = ["c250/RSI20V80/CaConc", "c500/RSI20V80/CaConc", "c1000/RSI20V80/CaConc", "c250/NSI20V80/CaConc", "c1000/c1000/f2/RSI20V80/CaConc"]
for i, file in enumerate(files):
	data = genfromtxt(file)

	plot(data[:,0]*1000, smooth(data[:,1],10), lw=0.6, color=tableau10[i], label=label[i])
	ax.set_ylabel('[Ca] ($\mu M$)')
	l = ax.legend()
	l.get_frame().set_facecolor(colorScheme)
	for j, text in enumerate(l.get_texts()):
		text.set_color(tableau10[j])

savefig('CaProfileOverload.eps', format='eps', dpi=300)
#show()
'''
'''
# Ca Profile
rcParams['figure.figsize'] = 5,3
ax = gca()
#f.patch.set_facecolor(colorScheme)

setp(ax.spines.values(), color=axiscolor)
setp([ax.get_xticklines(), ax.get_yticklines()], color=axiscolor)
ax.yaxis.label.set_color(txtcolor)
ax.xaxis.label.set_color(txtcolor)
ax.tick_params(axis='x', colors=axiscolor)
ax.tick_params(axis='y', colors=axiscolor)
	
ax.set_xlabel('Time (msec)')

label = ['RS', 'IS', 'S', 'NS']
files = ["c250/RSI20V80/CaConc", "c250/IP3SI20V80/CaConc", "c250/SI20V80/CaConc", "c250/NSI20V80/CaConc"]
for i, file in enumerate(files):
	data = genfromtxt(file)

	plot(data[:,0]*1000, smooth(data[:,1],10), lw=0.4, color=tableau10[i], label=label[i])
	ax.set_ylabel('[Ca] ($\mu M$)')
	l = ax.legend()
	l.get_frame().set_facecolor(colorScheme)
	for j, text in enumerate(l.get_texts()):
		text.set_color(tableau10[j])

savefig('CaProfile.eps', format='eps', dpi=300)
#show()
'''
