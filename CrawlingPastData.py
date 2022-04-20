import sys
import win32com.client
import pandas as pd
import os
import ctypes
import time
import datetime
import argparse

def InitPlusCheck(g_objCpStatus):
    """
    Cybos API 실행을 위한 환경 메소드
    관리자 권한과 Cybos Plus 연결 확인
    """
    if ctypes.windll.shell32.IsUserAnAdmin():
        print('정상: 관리자권한으로 실행된 프로세스입니다.')
    else:
        print('오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')
        return False

    # 연결 여부 체크
    if (g_objCpStatus.IsConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        return False
    return True

# Cybos 차트 요청 - 기간 기준으로
def CrawlingPastData(g_objCpStatus,objStockChart,code,fromDate,toDate, stockData):
    """
    Cybos API 를 이용한 차트 요청
    기간 기준으로 데이터 받아오기
    """
    print("종목코드 : " + code + " 요청날짜 : " + fromDate + "~" + toDate)
   
    # 연결 여부 체크
    if InitPlusCheck(g_objCpStatus) == False:
        return False

    while int(toDate) >= 20190501:
        objStockChart.SetInputValue(0, code)                    # 종목코드
        objStockChart.SetInputValue(1, ord('1'))                # 기간으로 받기
        objStockChart.SetInputValue(3, fromDate)                # From 날짜
        objStockChart.SetInputValue(2, toDate)                  # To 날짜
        objStockChart.SetInputValue(5, [0, 1, 2, 8])            # 날짜,시간,시가,거래량
        objStockChart.SetInputValue(6, ord('m'))                # '차트 주기 - 분/틱
        objStockChart.SetInputValue(7, 1)                       # 분틱차트 주기
        objStockChart.SetInputValue(9, ord('1'))                # 수정주가 사용
        objStockChart.BlockRequest()
        toDate = objStockChart.GetDataValue(0, 4998) - 1
        
        # 요청하고 요청 상태 받기
        rqStatus = objStockChart.GetDibStatus()
        rqRet = objStockChart.GetDibMsg1()
        if rqStatus != 0:
            print("통신상태 문제 발생 : " + rqStatus + " " + rqRet)
            exit()

        for i in range(objStockChart.GetHeaderValue(3)):
            stockData['STOCK_DATE'].append(objStockChart.GetDataValue(0, i))
            stockData['STOCK_TIME'].append(objStockChart.GetDataValue(1, i))
            stockData['STOCK_PRICE'].append(objStockChart.GetDataValue(2, i))
            stockData['STOCK_VOLUME'].append(objStockChart.GetDataValue(3, i))
    return 

def setStock(stock,datapath):
    """
    종목코드 설정하고 (stock)
    해당 경로 설정(datapath)
    이후 csv 가져와서 찾기
    """
    # data 디렉토리 내부의 파일 목록 읽어오기
    filepath = os.listdir(datapath)
    # 주가 코드를 가지고 있는 securities.csv 파일 읽기
    csv_file = [idx for idx in filepath if 'securities' in idx]

    securities_csv = pd.read_csv("%s%s" % (datapath,"".join(csv_file)), encoding='CP949', index_col=0 , header=0)
    securities_csv = securities_csv.drop_duplicates(["종목명"])

    securities_codes = {}
    print(securities_csv)
    for i in stock:
        securities_codes[i] ="".join(list(securities_csv[securities_csv["종목명"] == i]["종목코드"]))

    # Key : 이름 - Value : 코드
    return securities_codes

if __name__=="__main__":
    # python 버전 출력
    print(sys.version)
    
    # 주가 관련 데이터 경로
    datapath = "//117.17.142.79/hadoop/tmp/stock_in/"
    
    # Cybos Plus API 사용을 위한 필요변수 
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
    g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
    
    (datetime.date.today()-datetime.timedelta(1)).strftime("%m%d")
    
    # 현재 날짜 가져오기
    nowDate = datetime.date.today().strftime("%m%d")
    # 현재 연도
    nowYear = int(datetime.date.today().strftime("%Y") + "0000")
   
    timeToSave = ["0101"]
    timeToSave.append(nowDate)
    
    # exe file 로 배포파일을 만들 경우 인자를 통해 코드 불러옴.
    # -h 옵션으로 도움말 제공
    parser = argparse.ArgumentParser(description="Enter any stock name")
    # list를 받을 이름 설정.
    parser.add_argument('stockName', type=str, nargs='+')
    
     # 주가 리스트
    stockList = setStock(parser.parse_args().stockName,datapath)
    print(stockList)
    for name,code in stockList.items():
        stockData = {
            'STOCK_DATE' : [], 
            'STOCK_TIME' : [],
            'STOCK_PRICE' : [],
            'STOCK_VOLUME' : []
        }
        filename="PastData_"+nowDate+"_"+code+".csv"
       
        if os.path.isfile(datapath+filename)==True:
            print("해당 파일은 이미 존재합니다")
            break
        
        for i in range(len(timeToSave)-1):
            CrawlingPastData(g_objCpStatus,objStockChart,code,str(nowYear+int(timeToSave[i])),str(nowYear+int(timeToSave[i+1])-1),stockData)

        # 역순으로 저장되기 때문에 조정해야 함.
        stockData['STOCK_DATE'].reverse()
        stockData['STOCK_TIME'].reverse()
        stockData['STOCK_PRICE'].reverse()
        stockData['STOCK_VOLUME'].reverse()
        df = pd.DataFrame(stockData, columns=['STOCK_DATE','STOCK_TIME','STOCK_PRICE','STOCK_VOLUME'])
        df.to_csv("%s%s%s%s%s.csv" % (datapath,"PastData_",nowDate,"_",code),header = True, encoding="CP949")
        f=open(datapath+"inlist.txt",'a')
        f.write(filename+"\n")
        f.close()
        

