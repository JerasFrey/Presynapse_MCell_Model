import os
from time import time

tstart = time()
#Give the paths to the input directories
#give original path (data path) seperate from avgdir
modeldir = "output/IP3_100/"





modelfolds = os.listdir(modeldir)
modelfolds =[e for e in modelfolds if os.path.isdir(modeldir+e)]

for j in range(len(modelfolds)):
	print(modelfolds[j])
	tend1 = time()
	print "Time Taken: ", tend1-tstart, " sec"
	seedfolders = os.listdir(modeldir+modelfolds[j]+"/")
	seedfolders =[d for d in seedfolders if os.path.isdir(modeldir+modelfolds[j]+"/"+d)]
	
	resultsdir = "results/IP3_100/"+modelfolds[j]+"_avg/"+"all_rels/"
	if not os.path.exists(resultsdir):
		os.makedirs(resultsdir)
	dataPath = modeldir+modelfolds[j]+"/"
	
	os.system("cat " + dataPath + "/*/dat/vdcc.spont.dat > " + resultsdir + "/rel_spont.dat")
	os.system("cat " + dataPath + "/*/dat/vdcc.async_*.dat > " + resultsdir + "/rel_async.dat")
	os.system("cat " + dataPath + "/*/dat/vdcc.sync_*.dat > " + resultsdir + "/rel_sync.dat")
	
	dataPath = modeldir+modelfolds[j]+"/"
	for i in range(len(seedfolders)):
		os.system("cat " + dataPath + seedfolders[i] + "/dat/vdcc.*.dat > " + dataPath + seedfolders[i] + "/dat/rel_all.dat")
#		
#		os.system("cat " + dataPath + "/*/dat/vdcc.*.dat > " + avgdir + "/rel_all.dat")
tend = time()
print("Time Taken Final: " + str(tend-tstart) + " sec")
