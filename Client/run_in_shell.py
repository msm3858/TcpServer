import logging
import socket

ip = '127.0.0.1'
port = 5000

file_name = '4chanWebScrapper.zip'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))


message = file_name.encode()

len_sent  =server.send(message)

response = server.recv(len_sent)
