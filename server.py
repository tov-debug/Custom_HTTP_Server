import socket

def parse_request(data):
    str_data = data.decode('utf-8', errors= 'ignore')
    print(str_data)
    request_line , separator, rest = str_data.partition('\r\n') 
    request_type,path, client_proto = request_line.split(' ')
    #print("method:", request_type)
    #print("path:", path)
    #print("version:", client_proto)
    headers_lines = rest.split('\r\n')

    print(headers_lines)

    headers = {}
    for line in headers_lines:
        if not line:
            break

        name, value = line.split(':',1)
        value = value.strip()
        headers[name] = value
    #print(headers)
    #print(headers["User-Agent"])
    return request_type,path, client_proto, headers

def build_response(status, body):
    
    server_proto = "HTTP/1.1"
    length = len(body)
    response = server_proto + " " + status + "\r\nContent-Length: " + str(length) + "\r\n\r\n" + body
    res = response.encode('utf-8')

    return res

def handle_client(client_sock):
    pass

def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 8080 ))
    server_sock.listen(1)
    client_sock, client_add = server_sock.accept()

    data = client_sock.recv(1024)
    #print("200 ok")
    #print(data)

    request_type,path, client_proto, headers = parse_request(data)


    res = build_response("200 OK", "hi, nice to meet you")
    client_sock.send(res)
    client_sock.close()
    server_sock.close()
