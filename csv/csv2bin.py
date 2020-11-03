import csv

def readcsv(filename):
    with open(filename,'r') as csvFile:
        reader = csv.reader(csvFile)
        chart = []
        for line in reader:
            chart.append(line)
    
    return chart

def writebin(bin):

if __name__ == '__main__':
    chart = readcsv("chart.csv")
    print(chart)