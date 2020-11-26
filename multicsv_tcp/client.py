import csv
import socket
import os

if __name__ == '__main__':
    binpath = 'bchart'
    csvpath = 'chart.csv'
    subpath = './subfile/'
    server_list = [23333,23334,23335]
    link_list=[]
    recv_data = []
    idx=0
    for i in range(len(server_list)):
        tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        link_list.append(tcp_client)
    with open(csvpath,'r') as csvFile:
        for line in csvFile.readlines():
            link_list[idx].connect(("172.16.0.22",server_list[idx]))
            link_list[idx].send((str(idx)+line).encode(encoding = 'utf-8'))
            recv_data.append('TBD')
            idx += 1
    with open(binpath,'wb') as binFile:
        for i in range(idx):
            recv_data[i] = link_list[i].recv(1024)
            binFile.write(recv_data[i][1:])
            #print(chr(recv_data[i][0]))
            #print(recv_data[i][1:].decode(encoding = 'utf-8'))

  