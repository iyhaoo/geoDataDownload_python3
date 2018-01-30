import urllib.request

import gzip, os, time, re, threading

from ftplib import FTP

destdir="D:/scRNAseqData/000datasetIndex"


#allDatasets = ["GSE42268","GSE45719","GSE76483","GSE47835","GSE52583","GSE55291","GSE57249","GSE60297","GSE60361","GSE60768",
#           "GSE61470","GSE63576","GSE64960","GSE65525","GSE66202","GSE70844","GSE75107","GSE75108","GSE75109","GSE75110",
#           "GSE75111","GSE74923","GSE67120","GSE79510","GSE70605","GSE81682","GSE66578","GSE74596","GSE77029","GSE65924",
#           "GSE70657"]
#allDatasets = ["GSE81682","GSE66578","GSE74596","GSE77029","GSE65924","GSE70657"]

def read_gz_file(path):
    if os.path.exists(path):
        with gzip.open(path, 'r') as pf:
            for line in pf:
                yield line

def page_request(srxUrl, gse2srrUrlDirCache, srxNo, dataset):
    with urllib.request.urlopen(srxUrl) as urlOpen:
        file = open(gse2srrUrlDirCache + "/" + srxNo, "wb")
        # print(str(urlOpen.read()))
        file.write(urlOpen.read())

        file.close()
        print("finish: %s \t %s" % (dataset, srxNo))

"""
for dataset in allDatasets:
    '''
    url = "ftp://ftp.ncbi.nlm.nih.gov/geo/series/" + dataset[0:len(dataset)-3] + "nnn/" + dataset + "/soft/" + dataset + "_family.soft.gz"
    print(url)
    with urllib.request.urlopen(url) as urlOpen:
        file = open(destdir + "/" + dataset + "_family.soft.gz", "wb")

        file.write(urlOpen.read())
        file.close()
        urlOpen.close()
        print("finish: %s" % dataset)
    '''

    gse2srxUrlDir = destdir + "/gse2srxUrlDir"
    '''
    if os.path.exists(gse2srxUrlDir):
        print("gse2srxUrlDir exist\n")
    else:
        os.mkdir(gse2srxUrlDir)

    con = read_gz_file(destdir + "/" + dataset + "_family.soft.gz")
    with open(gse2srxUrlDir + "/" + dataset + "_gse2srxUrlDir", "w") as file:

        for line in con:
            strLine = str(line)
            if strLine.startswith("b'!Sample_relation = SRA:"):
                file.write(strLine[26:-3] + "\n")
    '''

    gse2srrUrlDir = destdir + "/gse2srrUrlDir"
    if os.path.exists(gse2srrUrlDir):
        print("gse2srxUrlDir exist\n")
    else:
        os.mkdir(gse2srrUrlDir)

    gse2srrUrlDirCache = gse2srrUrlDir + "/pageCache"
    if os.path.exists(gse2srrUrlDirCache):
        print("gse2srxUrlDir exist\n")
    else:
        os.mkdir(gse2srrUrlDirCache)

    with open(gse2srxUrlDir + "/" + dataset + "_gse2srxUrlDir", "r") as file:

        for srxUrl in file:
            srxNo = srxUrl[38:-1]
            try:
                page_request(srxUrl, gse2srrUrlDirCache, srxNo, dataset)
            except:
                time.sleep(5)
                print("error occur\n")
                page_request(srxUrl, gse2srrUrlDirCache, srxNo, dataset)
"""
'''
gse2srxUrlDir = destdir + "/gse2srxUrlDir"
gseVec = os.listdir(gse2srxUrlDir)


class gse2srx:
    gse = []
    srx = []

    def __init__(self, gse, srx):
        self.gse = gse
        self.srx = srx

for ii in gseVec:
    with open(gse2srxUrlDir + "/" + ii, "r") as gse2srxFile:
        for jj in gse2srxFile:
            gse2srx.gse.append(ii.split("_")[0])
            gse2srx.srx.append(jj.replace("\n","").split("=")[1])

gse2srrUrlDir = destdir + "/gse2srrUrlDir"
gse2srrUrlDirCache = gse2srrUrlDir + "/pageCache"


pageCacheList = os.listdir(gse2srrUrlDirCache)

regex=re.compile('run=SRR[0-9]+?">SRR[0-9]+?</a>')
SRRNOList = []

for pageCacheDir in pageCacheList:
    with open(gse2srrUrlDirCache + "/" + pageCacheDir, "r", encoding='utf-8') as file:
        fileText = file.read()
        gseIndex = gse2srx.srx.index(pageCacheDir)
        for rawSRRNo in regex.findall(fileText):
            SRRNO = rawSRRNo.split('">')[1][:-4]
            ftpDir = "ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/" + SRRNO[:6] + "/" + SRRNO + "/" + SRRNO + ".sra"
            gse2ftpDir = gse2srx.gse[gseIndex] + "\t" + "ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/" + SRRNO[:6] + "/" + SRRNO + "/" + SRRNO + ".sra"
            with open(gse2srrUrlDir + "/srrUrl", "w") as srrUrl:
                srrUrl.write(ftpDir + "\n")
            with open(gse2srrUrlDir + "/gse2SrrUrl", "w") as gse2SrrUrl:
                gse2SrrUrl.write(gse2ftpDir + "\n")
            print(ftpDir + "\t" + pageCacheDir)


    #break

'''





class ftpSettings:
    saveDir = ""
    logDir = ""
    downloadLog = ""
    cacheLen = 512000
    isFinish = 0
    downloadList = {
        "fileName": [],
        "dataLen": [],
        "finLen": [],
        "time": []
    }
    downloadCache = {
        "fileName": [],
        "cache": []
    }
    class threadAndFile:
        thread = []
        file = []
        def __init__(self, thread, file):
            self.thread = thread
            self.file = file
    def __init__(self, threadAndFile, downloadCache, isFinish, saveDir="", logDir="", downloadList="", downloadLog = "", cacheLen = 2048000):
        self.threadAndFile = threadAndFile
        self.downloadCache = downloadCache
        self.saveDir = saveDir
        self.logDir = logDir
        self.downloadList = downloadList
        self.downloadLog = downloadLog
        self.cacheLen = cacheLen
        self.isFinish = isFinish
    def retrbinaryCallback(self):
        threadIndex = ftpSettings.threadAndFile.thread.index(threading.get_ident())
        fileName = ftpSettings.threadAndFile.file[threadIndex]
        fileNameIndex = ftpSettings.downloadList["fileName"].index(fileName)
        ftpSettings.downloadList["finLen"][fileNameIndex] = ftpSettings.downloadList["finLen"][fileNameIndex] + len(self)
        if ftpSettings.downloadCache["fileName"].count(fileName) == 0:
            ftpSettings.downloadCache["fileName"].append(fileName)
            ftpSettings.downloadCache["cache"].append("")
        catchIndex = ftpSettings.downloadCache["fileName"].index(fileName)
        if len(ftpSettings.downloadCache["cache"][catchIndex]) == 0:
            ftpSettings.downloadCache["cache"][catchIndex] = self
        else:
            ftpSettings.downloadCache["cache"][catchIndex] += self
        if len(ftpSettings.downloadCache["cache"][catchIndex]) > ftpSettings.cacheLen or ftpSettings.downloadList["finLen"][fileNameIndex] == ftpSettings.downloadList["dataLen"][fileNameIndex]:
            saveFileDir = ftpSettings.saveDir + "/" + ftpSettings.downloadList["fileName"][fileNameIndex]
            with open(saveFileDir, "ab") as saveFile:
                saveFile.write(ftpSettings.downloadCache["cache"][catchIndex])
            logFileDir = ftpSettings.logDir + "/" + ftpSettings.downloadList["fileName"][fileNameIndex] + ".log"
            if os.path.getsize(saveFileDir) == ftpSettings.downloadList["finLen"][fileNameIndex]:
                with open(logFileDir, "w")as downloadLogFile:
                    downloadLogFile.write(ftpSettings.downloadList["fileName"][fileNameIndex] + "\t" + str(ftpSettings.downloadList["dataLen"][fileNameIndex]) + "\t" + str(ftpSettings.downloadList["finLen"][fileNameIndex]))
            else:
                ftpSettings.downloadList["finLen"][fileNameIndex] = 0
                os.remove(saveFileDir)
                raise NameError(fileName, "e8: file and log are inconsistent")
            ftpSettings.downloadCache["cache"][catchIndex] = ""
            lastTime = ftpSettings.downloadList["time"][fileNameIndex]
            ftpSettings.downloadList["time"][fileNameIndex] = time.time()
            if ftpSettings.downloadList["time"][fileNameIndex] == lastTime:
                print("lastTime: " + str(lastTime))
                print("thisTime: " + str(ftpSettings.downloadList["time"][fileNameIndex]))
                lastTime = lastTime - 1
            print("wrinting " + ftpSettings.downloadList["fileName"][fileNameIndex] + "\tSpeed: " + str(round(ftpSettings.cacheLen/((ftpSettings.downloadList["time"][fileNameIndex]-lastTime)*1000), 2)) +"k/s")
            print("Fin: " + str(ftpSettings.downloadList["finLen"][fileNameIndex]) + "\tAll: " + str(ftpSettings.downloadList["dataLen"][fileNameIndex]) + "\t" + str(round(100 * ftpSettings.downloadList["finLen"][fileNameIndex] / ftpSettings.downloadList["dataLen"][fileNameIndex], 2)))
        #print(ftpSettings.downloadList["fileName"][fileNameIndex], ftpSettings.downloadList["finLen"][fileNameIndex], ftpSettings.downloadList["dataLen"][fileNameIndex], len(ftpSettings.downloadList["cache"][fileNameIndex]), 100 * ftpSettings.downloadList["finLen"][fileNameIndex] / ftpSettings.downloadList["dataLen"][fileNameIndex])

    def retrlinesCallback(self):
        regex = re.compile('[a-zA-Z]+?[ ]+?[0-9]+?(?=[ ]+?[a-zA-Z]+?)')
        threadIndex = ftpSettings.threadAndFile.thread.index(threading.get_ident())
        fileName = ftpSettings.threadAndFile.file[threadIndex]
        ftpSettings.downloadList["fileName"].append(fileName)
        ftpSettings.downloadList["dataLen"].append(0)
        ftpSettings.downloadList["finLen"].append(0)
        ftpSettings.downloadList["time"].append(time.time())
        ftpSettings.downloadList["dataLen"][ftpSettings.downloadList["fileName"].index(fileName)] = int(str(regex.findall(str(self))[0]).split(" ")[-1])
        ftpSettings.downloadList["time"][ftpSettings.downloadList["fileName"].index(fileName)] = time.time()

def downloadListAdd(ftpServer, remotePath, ftpSettings, timeoutLen):
    try:
        ftp = FTP(host=ftpServer, timeout=timeoutLen)
        ftp.login()
        ftp.retrlines('LIST ' + remotePath, callback=ftpSettings.retrlinesCallback)
        ftp.quit()
    except Exception as e:
        print(e)
        print("e1")
        time.sleep(5)
        return downloadListAdd(ftpServer, remotePath, ftpSettings, timeoutLen)

class ftpFileDownloadThread(threading.Thread):
    def __init__(self, singleUrl):
        threading.Thread.__init__(self)
        self.singleUrl = singleUrl
    def run(self):
        try:
            ftpFileDownloadThread.mainFun(self.singleUrl)
            threadIndex = ftpSettings.threadAndFile.thread.index(threading.get_ident())
            del ftpSettings.threadAndFile.thread[threadIndex]
            del ftpSettings.threadAndFile.file[threadIndex]
        except Exception as e:
            print(e)
            print("e2: " + self.singleUrl.split("/")[-1])
            time.sleep(5)
            threadIndex = ftpSettings.threadAndFile.thread.index(threading.get_ident())
            del ftpSettings.threadAndFile.thread[threadIndex]
            del ftpSettings.threadAndFile.file[threadIndex]
            return ftpFileDownloadThread.run(self)
    def mainFun(singleUrl):
        fileName = singleUrl.split("/")[-1]
        ftpServer = singleUrl.split("/")[2]
        remotePath = singleUrl.split(ftpServer)[1].split("\n")[0]
        if fileName in ftpSettings.threadAndFile.file:
            fileThreadIndex = ftpSettings.threadAndFile.file.index(fileName)
            ftpSettings.threadAndFile.thread[fileThreadIndex] = threading.get_ident()
        else:
            ftpSettings.threadAndFile.thread.append("")
            ftpSettings.threadAndFile.file.append(fileName)
            fileThreadIndex = ftpSettings.threadAndFile.file.index(fileName)
            ftpSettings.threadAndFile.thread[fileThreadIndex] = threading.get_ident()
        if fileName in ftpSettings.downloadList["fileName"]:
            fileNameIndex = ftpSettings.downloadList["fileName"].index(fileName)
            if fileName in ftpSettings.downloadCache["fileName"]:
                catchIndex = ftpSettings.downloadCache["fileName"].index(fileName)
                ftpSettings.downloadList["finLen"][fileNameIndex] = ftpSettings.downloadList["finLen"][fileNameIndex] - len(ftpSettings.downloadCache["cache"][catchIndex])
                ftpSettings.downloadCache["cache"][catchIndex] = ""
            if ftpSettings.downloadList["finLen"][fileNameIndex] == ftpSettings.downloadList["dataLen"][fileNameIndex]:
                saveFileDir = ftpSettings.saveDir + "/" + ftpSettings.downloadList["fileName"][fileNameIndex]
                if os.path.exists(saveFileDir):
                    if os.path.getsize(ftpSettings.saveDir + "/" + ftpSettings.downloadList["fileName"][fileNameIndex]) != ftpSettings.downloadList["dataLen"][fileNameIndex]:
                        print(os.path.getsize(
                            ftpSettings.saveDir + "/" + ftpSettings.downloadList["fileName"][fileNameIndex]),
                              ftpSettings.downloadList["dataLen"][fileNameIndex])
                print(str(ftpSettings.downloadList["fileName"][fileNameIndex]) + " has finished")
                return 0
            else:
                if os.path.exists(ftpSettings.saveDir + "/" + fileName):
                    if os.path.getsize(ftpSettings.saveDir + "/" + fileName) != ftpSettings.downloadList["finLen"][fileNameIndex]:
                        print("e5: inconsistence", fileName, "finLen:", ftpSettings.downloadList["finLen"][fileNameIndex], "fileLen:", os.path.getsize(ftpSettings.saveDir + "/" + fileName))
                        os.remove(ftpSettings.saveDir + "/" + fileName)
                        ftpSettings.downloadList["finLen"][fileNameIndex] = 0
                else:
                    ftpSettings.downloadList["finLen"][fileNameIndex] = 0
                    print("e6: file lost ", fileName)
                if ftpSettings.downloadList["finLen"][fileNameIndex] >= ftpSettings.downloadList["dataLen"][fileNameIndex]:
                    print("e7: wrong download", fileName, "finLen:", ftpSettings.downloadList["finLen"][fileNameIndex], "dataLen:", ftpSettings.downloadList["dataLen"][fileNameIndex])
                    os.remove(ftpSettings.saveDir + "/" + fileName)
                    ftpSettings.downloadList["finLen"][fileNameIndex] = 0
                print("Continue downloading " + fileName + " from " + str(round(ftpSettings.downloadList["finLen"][fileNameIndex]/ftpSettings.downloadList["dataLen"][fileNameIndex]*100, 2)) + "\t in " + str(ftpSettings.downloadList["finLen"][fileNameIndex]) + "/" + str(ftpSettings.downloadList["dataLen"][fileNameIndex]))
        else:
            downloadListAdd(ftpServer, remotePath, ftpSettings, 10)
            if fileName not in ftpSettings.downloadList["fileName"]:
                print("e3", fileName in ftpSettings.downloadList["fileName"])
            fileNameIndex = ftpSettings.downloadList["fileName"].index(fileName)#####
            if os.path.exists(ftpSettings.saveDir + "/" + fileName):
                if os.path.getsize(ftpSettings.saveDir + "/" + fileName) != ftpSettings.downloadList["dataLen"][fileNameIndex]:
                    print("remove wrong downloaded file\t" + fileName)
                    os.remove(ftpSettings.saveDir + "/" + fileName)
        ftp = FTP(host=ftpServer, timeout=30)
        ftp.login()
        ftp.retrbinary(cmd='RETR ' + remotePath, callback=ftpSettings.retrbinaryCallback, rest=ftpSettings.downloadList["finLen"][fileNameIndex])
        ftp.quit()
        if os.path.getsize(ftpSettings.saveDir + "/" + fileName) == ftpSettings.downloadList["dataLen"][fileNameIndex]:
            print(str(ftpSettings.downloadList["fileName"][fileNameIndex]) + " finished")
        else:
            os.remove(ftpSettings.saveDir + "/" + fileName)
            raise NameError("downloade finished but wrong\t" + fileName)



class downLoadState(threading.Thread):
    def __init__(self, downloadDir):
        threading.Thread.__init__(self)
        self.downloadDir = downloadDir
    def run(self):
        while threading.activeCount() > 1:
            if ftpSettings.downloadList != "":
                allLog = ""
                for ii in range(len(ftpSettings.downloadList["fileName"])):
                    if ftpSettings.downloadList["dataLen"][ii] == 0:
                        print("e4")
                    allLog += ftpSettings.downloadList["fileName"][ii] + "\t" + \
                              str(ftpSettings.downloadList["dataLen"][ii]) + "\t" + \
                              str(ftpSettings.downloadList["finLen"][ii]) + "\t" + \
                              str(round(100*ftpSettings.downloadList["finLen"][ii]/ftpSettings.downloadList["dataLen"][ii], 2)) + "\n"
                with open(self.downloadDir + "/allLog.log", "w")as allLogFile:
                    allLogFile.write(allLog)
            time.sleep(5)#reflesh time
            if threading.activeCount() <= 2:
                print("finished?")
                time.sleep(10)
                if ftpSettings.isFinish == 1:
                    if threading.activeCount() <= 2:
                        print("finished!")
                        return 0

def ftpFileDownload(srrUrlContent, downloadDir, maxThreadNum):
    logDir = downloadDir + "/downloadLog"
    if os.path.isdir(logDir):
        downloadLog = os.listdir(logDir)
        for LogFile in downloadLog:
            with open(logDir + "/" + LogFile, "r") as logContent:
                downloadState = logContent.read().replace("\n", "").split("\t")
                ftpSettings.downloadList["fileName"].append(downloadState[0])
                ftpSettings.downloadList["dataLen"].append(int(downloadState[1]))
                ftpSettings.downloadList["finLen"].append(int(downloadState[2]))
                ftpSettings.downloadList["time"].append(time.time())
    else:
        os.mkdir(logDir)
    srrUrlContentVec = srrUrlContent.split("\n")
    if "" in srrUrlContentVec:
        srrUrlContentVec.remove("")
    ftpSettings.saveDir = downloadDir
    ftpSettings.logDir = logDir
    downLoadState(downloadDir).start()
    maxThreadNum = maxThreadNum + 1

    for ii in range(0, len(srrUrlContentVec)):
        thisThread = ftpFileDownloadThread(srrUrlContentVec[ii])
        while threading.activeCount() > maxThreadNum:
            time.sleep(1)
        thisThread.start()
    ftpSettings.isFinish = 1




gse2srrUrlDir = destdir + "/gse2srrUrlDir"
srrUrlDir = gse2srrUrlDir + "/srrUrl"
downloadDir = "D:/scRNAseqData/pyDl1"

if os.path.exists(downloadDir):
    print("downloadDir exist")
else:
    os.mkdir(downloadDir)


with open(srrUrlDir, "r") as srrUrl:
    srrUrlContent = srrUrl.read()

ftpFileDownload(srrUrlContent, downloadDir, 10)





