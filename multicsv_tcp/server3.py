import csv
import socket
import os

if __name__ == '__main__':
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server.bind(("172.16.0.22", 23335))
    
    tcp_server.listen(128)

    tcp_client, tcp_client_address= tcp_server.accept()
    recv_data = tcp_client.recv(1024)
    recv_content = recv_data.decode(encoding = "utf-8")

    send_data = recv_content.encode(encoding = "utf-8")
    tcp_client.send(send_data)
    tcp_client.close()