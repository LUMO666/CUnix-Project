import csv
from multiprocessing import Process, Queue
import os
import mmap

def readcsv(filename):
    with open(filename,'r') as csvFile:
        reader = csv.reader(csvFile)
        chart = []
        for line in reader:
            chart.append(line)
    
    return chart

def writebin(data,bin):
    with open(bin,'wb') as binFile:
        n = '\n'
        for line in data:
            for item in line:
                for char in (item+'\t'):
                    binFile.write((char).encode(encoding='utf-8'))
            binFile.write(n.encode(encoding='utf-8'))

def readbin(bin):
    with open(bin,'rb') as binFile:
        strr =''
        p = None
        while True:
            p = binFile.read(1).decode(encoding='utf-8')
            strr += p
            if p == '':
                break
        return strr

def subpro(fileidx,path):
    writebin(readcsv(path + str(fileidx) + '.csv'), path + str(fileidx) + '_bchart')

def mksubfiles(filename):
    idx = 0
    with open(filename,'r') as csvFile:
        for line in csvFile.readlines():
            with open('./subfile/'+str(idx)+'.csv','w+') as subf:
                subf.write(line)
            idx += 1
    return idx

def catsubfiles(num_sub,filename,subpath):
    n = '\n'
    with open(filename,'wb') as binFile:
        for i in range(num_sub):
            line = readbin(subpath+str(i)+'_bchart')
            for char in line:
                binFile.write((char).encode(encoding='utf-8'))

def subtrans(lineq, binq):
    line = lineq.get(True)
    binline = b''
    for char in line:
        binline += (char).encode(encoding='utf-8')
    binq.put(binline)

def bincat(file):
    with open(file,'rb') as binFile:
        mm = mmap.mmap(binFile.fileno(),0,prot = mmap.PROT_READ)
        flag = mm.readline()
        while flag:
            print(flag.decode(encoding='utf-8'))
            flag = mm.readline()


if __name__ == '__main__':
    binpath = 'bchart'
    csvpath = 'chart.csv'
    subpath = './subfile/'
    idx = 0
    lineq = Queue()
    binq = Queue()
    Process_list = []
    with open(csvpath,'r') as csvFile:
        for line in csvFile.readlines():
            lineq.put(line)
            p = Process(target=subtrans, args=(lineq,binq))
            Process_list.append(p)
            p.start()
            idx += 1

    for i in range(idx):
        Process_list[i].join()
    with open(binpath,'wb') as binFile:
        for i in range(idx):
            writeline = binq.get(True)
            binFile.write(writeline)
    bincat(binpath)    

    #writebin(chart,binpath)
    #readbin(binpath)