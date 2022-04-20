import os
import subprocess
import shlex

inpath="/home/hadoop/tmp/stock_in/"
outpath="/home/hadoop/tmp/stock_out/"

f=open(inpath+"inlist.txt",'r')
filename=f.readlines()[-1]
f.close()
hdpath="/stock/"+filename
filepath=inpath+filename

if(os.path.isfile(outpath+filename)==False):
	print(filename)
	incommand="hadoop fs -put "+filepath+" "+hdpath
	put=subprocess.Popen(shlex.split(incommand),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	put.communicate()

	filepath=outpath+filename
	outcommand="hadoop fs -get "+hdpath+" "+filepath
	get=subprocess.Popen(shlex.split(outcommand), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	get.communicate()	
