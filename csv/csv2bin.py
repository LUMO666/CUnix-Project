import csv

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
        str =''
        p = None
        while True:
            p = binFile.read(1).decode(encoding='utf-8')
            str += p
            if p == '':
                break
        print(str)

if __name__ == '__main__':
    binpath = 'bchart'
    csvpath = 'chart.csv'
    chart = readcsv(csvpath)
    print(chart)
    writebin(chart,binpath)
    readbin(binpath)