import csv
from multiprocessing import Process
import os

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

if __name__ == '__main__':
    binpath = 'bchart'
    csvpath = 'chart.csv'
    subpath = './subfile/'
    num_sub = mksubfiles(csvpath)
    Process_list = []
    for i in range(num_sub):
        p = Process(target=subpro, args=(i,subpath))
        Process_list.append(p)
        p.start()
    for i in range(num_sub):
        p.join()
    catsubfiles(num_sub,binpath,subpath)

    
    #writebin(chart,binpath)
    #readbin(binpath)