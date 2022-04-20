import win32com.client

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
#industryCodeList = instCpCodeMgr.GetIndustryList()


Upjong=["005 음식료품",
        "006 섬유,의복",
        "007 종이,목재",
        "008 화학",
        "009 의약품",
        "010 비금속광물",
        "011 철강,금속",
        "012 기계",
        "013 전기,전자",
        "014 의료정밀",
        "015 운송장비",
        "016 유통업",
        "017 전기가스업",
        "018 건설업",
        "019 운수창고",
        "020 통신업",
        "021 금융업",
        "022 은행",
        "024 증권",
        "025 보험",
        "026 서비스업",
        "027 제조업"]


for i in range(5,28):
    if i==23:
        continue
    tarketCodeList = instCpCodeMgr.GetGroupCodeList(i)
    if(i>23):
        print(Upjong[i-6])
    else:
        print(Upjong[i-5])
    for code in tarketCodeList:
        print(code, instCpCodeMgr.CodeToName(code))
    print("\n")
