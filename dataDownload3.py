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
    downloadList = ""
    saveDir = ""
    logDir = ""
    downloadLog = ""
    cacheLen = 512000
    class threadAndFile:
        thread = []
        file = []
        def __init__(self, thread, file):
            self.thread = thread
            self.file = file
    class downloadCache:
        fileName = []
        cache = []
        def __init__(self, fileName, cache):
            self.fileName = fileName
            self.cache = cache
    def __init__(self, threadAndFile, downloadCache, saveDir="", logDir="", downloadList="", downloadLog = "", cacheLen = 2048000):
        self.threadAndFile = threadAndFile
        self.downloadCache = downloadCache
        self.saveDir = saveDir
        self.logDir = logDir
        self.downloadList = downloadList
        self.downloadLog = downloadLog
        self.cacheLen = cacheLen
    def retrbinaryCallback(self):
        threadIndex = ftpSettings.threadAndFile.thread.index(threading.get_ident())
        fileName = ftpSettings.threadAndFile.file[threadIndex]
        fileNameIndex = ftpSettings.downloadList.fileName.index(fileName)
        ftpSettings.downloadList.finLen[fileNameIndex] = ftpSettings.downloadList.finLen[fileNameIndex] + len(self)
        downloadList = ftpSettings.downloadList
        if ftpSettings.downloadCache.fileName.count(fileName) == 0:
            ftpSettings.downloadCache.fileName.append(fileName)
            ftpSettings.downloadCache.cache.append("")

        catchIndex = ftpSettings.downloadCache.fileName.index(fileName)
        if len(ftpSettings.downloadCache.cache[catchIndex]) == 0:
            ftpSettings.downloadCache.cache[catchIndex] = self
        else:
            ftpSettings.downloadCache.cache[catchIndex] += self
        if len(ftpSettings.downloadCache.cache[catchIndex]) > ftpSettings.cacheLen or ftpSettings.downloadList.finLen[fileNameIndex] == ftpSettings.downloadList.dataLen[fileNameIndex]:
            with open(ftpSettings.logDir + "/" + ftpSettings.downloadList.fileName[fileNameIndex] + ".log", "w")as downloadLogFile:
                downloadLogFile.write(ftpSettings.downloadList.fileName[fileNameIndex] + "\t" + str(ftpSettings.downloadList.dataLen[fileNameIndex]) + "\t" + str(
                    ftpSettings.downloadList.finLen[fileNameIndex]))
            with open(ftpSettings.saveDir + "/" + ftpSettings.downloadList.fileName[fileNameIndex], "ab") as saveFile:
                saveFile.write(ftpSettings.downloadCache.cache[catchIndex])
            ftpSettings.downloadCache.cache[catchIndex] = ""
            lastTime = downloadList.time[fileNameIndex]
            downloadList.time[fileNameIndex] = time.time()
            if downloadList.time[fileNameIndex] == lastTime:
                print("lastTime: " + str(lastTime))
                print("thisTime: " + str(downloadList.time[fileNameIndex]))
                lastTime = lastTime - 1
            print("wrinting " + ftpSettings.downloadList.fileName[fileNameIndex] + "\tSpeed: " + str(ftpSettings.cacheLen/((downloadList.time[fileNameIndex]-lastTime)*1000)) +"k/s")
            print("Fin: " + str(downloadList.finLen[fileNameIndex]) + "\tAll: " + str(downloadList.dataLen[fileNameIndex]) + "\t" + str(100 * downloadList.finLen[fileNameIndex] / downloadList.dataLen[fileNameIndex]))
        #print(downloadList.fileName[fileNameIndex] + "\t" + str(downloadList.finLen[fileNameIndex]) + "\t" + str(downloadList.dataLen[fileNameIndex]) + "\t" + str(len(ftpSettings.downloadCache.cache[catchIndex])) + "\t" + str(100 * downloadList.finLen[fileNameIndex] / downloadList.dataLen[fileNameIndex]))

    def retrlinesCallback(self):
        regex = re.compile('[a-zA-Z]+?[ ]+?[0-9]+?(?=[ ]+?[a-zA-Z]+?)')
        threadIndex = ftpSettings.threadAndFile.thread.index(threading.get_ident())
        fileName = ftpSettings.threadAndFile.file[threadIndex]
        ftpSettings.downloadList.fileName.append(fileName)
        ftpSettings.downloadList.dataLen.append(0)
        ftpSettings.downloadList.finLen.append(0)
        ftpSettings.downloadList.time.append(time.time())
        ftpSettings.downloadList.dataLen[ftpSettings.downloadList.fileName.index(fileName)] = int(str(regex.findall(str(self))[0]).split(" ")[-1])
        ftpSettings.downloadList.time[ftpSettings.downloadList.fileName.index(fileName)] = time.time()

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
    def __init__(self, singleUrl, downloadList):
        threading.Thread.__init__(self)
        self.singleUrl = singleUrl
        self.downloadList = downloadList
    def run(self):
        try:
            ftpFileDownloadThread.mainFun(self.singleUrl, self.downloadList)
        except Exception as e:
            print(e)
            print("e2: " + self.singleUrl.split("/")[-1])
            time.sleep(5)
            return ftpFileDownloadThread.run(self)
    def mainFun(singleUrl, downloadList):
        fileName = singleUrl.split("/")[-1]
        ftpServer = singleUrl.split("/")[2]
        remotePath = singleUrl.split(ftpServer)[1].split("\n")[0]
        ftpSettings.downloadList = downloadList
        if fileName in ftpSettings.threadAndFile.file:
            fileThreadIndex = ftpSettings.threadAndFile.file.index(fileName)
            ftpSettings.threadAndFile.thread[fileThreadIndex] = threading.get_ident()
        else:
            ftpSettings.threadAndFile.thread.append("")
            ftpSettings.threadAndFile.file.append(fileName)
            fileThreadIndex = ftpSettings.threadAndFile.file.index(fileName)
            ftpSettings.threadAndFile.thread[fileThreadIndex] = threading.get_ident()
        if fileName in downloadList.fileName:
            fileNameIndex = downloadList.fileName.index(fileName)
            if downloadList.finLen[fileNameIndex] == downloadList.dataLen[fileNameIndex]:
                print(str(downloadList.fileName[fileNameIndex]) + " has finished")
                return 0
            else:
                print("Continue downloading " + str(fileName) + " from " + str(downloadList.finLen[fileNameIndex]/downloadList.dataLen[fileNameIndex]*100) + "\t in " + str(downloadList.finLen[fileNameIndex]) + "/" + str(downloadList.dataLen[fileNameIndex]))
        else:
            downloadListAdd(ftpServer, remotePath, ftpSettings, 10)
            fileNameIndex = downloadList.fileName.index(fileName)
        ftp = FTP(host=ftpServer, timeout=60)
        ftp.login()
        ftp.retrbinary(cmd='RETR ' + remotePath, callback=ftpSettings.retrbinaryCallback, rest=downloadList.finLen[fileNameIndex])
        #ftp.retrbinary(cmd='RETR ' + remotePath, callback=ftpSettings.retrbinaryCallback, rest=downloadList.dataLen[fileNameIndex] - 5120000)
        ftp.quit()
        print(str(downloadList.fileName[fileNameIndex]) + " finished")
        threadIndex = ftpSettings.threadAndFile.thread.index(threading.get_ident())
        del ftpSettings.threadAndFile.thread[threadIndex]
        del ftpSettings.threadAndFile.file[threadIndex]

class downLoadState(threading.Thread):
    def __init__(self, downloadDir):
        threading.Thread.__init__(self)
        self.downloadDir = downloadDir
    def run(self):
        while threading.activeCount() > 1:
            if ftpSettings.downloadList != "":
                allLog = ""
                for ii in range(len(ftpSettings.downloadList.fileName)):
                    allLog += ftpSettings.downloadList.fileName[ii] + "\t" + str(ftpSettings.downloadList.dataLen[ii]) + "\t" + str(ftpSettings.downloadList.finLen[ii]) + "\t" +str(100*ftpSettings.downloadList.finLen[ii]/ftpSettings.downloadList.dataLen[ii]) + "\n"
                with open(self.downloadDir + "/allLog.log", "w")as allLogFile:
                    allLogFile.write(allLog)
            time.sleep(10)
            if threading.activeCount() <= 2:
                print("finished?")
                time.sleep(5)
                if threading.activeCount() <= 2:
                    print("finished!")
                    return 0

def ftpFileDownload(srrUrlContent, downloadDir, maxThreadNum):
    class downloadList:
        fileName = []
        dataLen = []
        finLen = []
        time = []
        def __init__(self, fileName, dataLen, finLen):
            self.fileName = fileName
            self.dataLen = dataLen
            self.finLen = finLen
            self.time = time
    logDir = downloadDir + "/downloadLog"
    if os.path.isdir(logDir):
        downloadLog = os.listdir(logDir)
        for LogFile in downloadLog:
            with open(logDir + "/" + LogFile, "r") as logContent:
                downloadState = logContent.read().replace("\n", "").split("\t")
                downloadList.fileName.append(downloadState[0])
                downloadList.dataLen.append(int(downloadState[1]))
                downloadList.finLen.append(int(downloadState[2]))
                downloadList.time.append(time.time())
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
        thisThread = ftpFileDownloadThread(srrUrlContentVec[ii], downloadList)
        while threading.activeCount() > maxThreadNum:
            time.sleep(1)
        thisThread.start()







downloadDir = "D:/scRNAseqData/pyDl1"

if os.path.exists(downloadDir):
    print("downloadDir exist")
else:
    os.mkdir(downloadDir)


with open(gse2srrUrlDir + "/srrUrl", "r") as srrUrl:
    srrUrlContent = srrUrl.read()

ftpFileDownload(srrUrlContent, downloadDir, 10)




