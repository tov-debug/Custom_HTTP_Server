import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('127.0.0.1', 8080 ))
server_sock.listen(1)
client_sock, client_add = server_sock.accept()

data = client_sock.recv(1024)
#print("200 ok")
print(data)
str_data = data.decode('utf-8', errors= 'ignore')
print(str_data)
request_line , separator, rest = str_data.partition('\r\n') 
request_type,path, client_proto = request_line.split(' ')
print("method:", request_type)
print("path:", path)
print("version:", client_proto)




server_proto = "HTTP/1.1"
state = "200 OK"
length = 5
response = server_proto + " " + state + "\r\nContent-Length: " + str(length) + "\r\n\r\nHello"
res = response.encode('utf-8')
client_sock.send(res)
client_sock.close()
server_sock.close()
