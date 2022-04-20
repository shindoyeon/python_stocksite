from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import csv,json
import os,sys
import pandas as pd
import datetime,time
import subprocess
import shlex

filepath = "C:/Users/Administrator/Desktop/stockproject/CybosAPI/Upjonglist/"
filelist = os.listdir(filepath)
dictlist = [i[4:] for i in filelist]
dictlist = [i[:-4] for i in dictlist]
result = {}
search=""
for i in range(len(filelist)):
	df = pd.read_csv(filepath+filelist[i],header=None)
	df = df[1].dropna()
	result[dictlist[i]] = list(df)



def crawling(request):
	if request.method=='POST':
		search=request.POST['search']
		print(search)

	temp = {}
    
	# subprocess.Popen(['C:\\Users\\administrator\\Desktop\\stockproject\\CybosAPI\\CrawlingPastData.exe+" "+str'])
	return render(request , 'index.html' , temp)

def setStock(stock):

	datapath="//117.17.142.79/hadoop/tmp/stock_in/"
	filepath = os.listdir(datapath)
	# 주가 코드를 가지고 있는 securities.csv 파일 읽기
	csv_file = [idx for idx in filepath if 'securities' in idx]

	securities_csv = pd.read_csv("%s%s" % (datapath,"".join(csv_file)), encoding='CP949', index_col=0 , header=0)
	securities_csv = securities_csv.drop_duplicates(["종목명"])

	code = "".join(list(securities_csv[securities_csv["종목명"] == stock]["종목코드"]))
	return code

def index(request):
   
	print("index")
	return render(request , 'index.html' , context = {"result" : result})

def tables(request):
   
	print("talbes")
	return render(request , 'tables.html')

def chartsModify(request):
    
    temp = {}
    return render(request , 'chartsModify.html' , temp)

@csrf_exempt
def test(request):
	
	nowDate = datetime.date.today().strftime("%m%d")	
	print("test")
	search=request.GET['search']
	print(search)
	
	dataDirectory = "//117.17.142.79/hadoop/tmp/stock_out/"
	filepath=dataDirectory+"PastData_"+nowDate+"_"+setStock(search)+".csv"
	print(filepath)

	if(os.path.isfile(filepath)==False):
		print("크롤링..")
		os.system("python C:\\Users\\Administrator\\Desktop\\stockproject\\CybosAPI\\CrawlingPastData.py "+search)
		time.sleep(8)
	
	df = pd.read_csv(filepath)
	date = df["STOCK_DATE"].unique().tolist()
	date.sort()
	result_dict = []
	volume_dict=[]
	
	for j in date:
	    target = df[df['STOCK_DATE']==j]
	    volume = target["STOCK_VOLUME"]
	    target = target["STOCK_PRICE"]
	    target = target.reset_index(drop=True)
	    volume = volume.reset_index(drop=True)
	    date_string = datetime.datetime.strptime(str(j)+"1530", '%Y%m%d%H%M')
	    timestamp = int(time.mktime(date_string.timetuple()))*1000
	    volume=volume.sum()
	    max = int(target.max())
	    min = int(target.min())
	    start = int(target[0])
	    end = int(list(target)[-1])
	    result_dict.append([timestamp,start,max,min,end])
	    volume_dict.append([timestamp,int(volume)])

	result_dict=json.dumps(result_dict,indent="\t")
	volume_dict=json.dumps(volume_dict,indent="\t")
	print(volume_dict)
	
	category=[]
	for i in result.keys():
		for name in result[i]:
			if name==search:
				category.append(i)
	print(category)

	return render(request , 'chartsModify.html' , context={'data':result_dict, 'volume':volume_dict, 'search':search, 'category':category})


	

    
    
    