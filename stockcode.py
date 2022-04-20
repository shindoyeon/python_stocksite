import win32com.client
import pandas as pd
import os

stockData = {
            '종목코드' : [],
            '종목명' : [],
            '종류' : []
}
datapath="C:/Users/Administrator/Desktop/stockproject/CybosAPI/Upjonglist/"
# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 
# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1) #거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2) #코스닥
 
for i, code in enumerate(codeList):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    stockData['종목코드'].append(code)
    stockData['종목명'].append(name)
    stockData['종류'].append("KOSPI")

for i, code in enumerate(codeList2):
    secondCode = objCpCodeMgr.GetStockSectionKind(code)
    name = objCpCodeMgr.CodeToName(code)
    stdPrice = objCpCodeMgr.GetStockStdPrice(code)
    stockData['종목코드'].append(code)
    stockData['종목명'].append(name)
    stockData['종류'].append("KOSDAQ")
 
df = pd.DataFrame(stockData, columns=['종목코드','종목명','종류'])
df.to_csv("%s%s.csv" % (datapath,"securities.csv"),header = True, encoding="CP949")
print(df)
