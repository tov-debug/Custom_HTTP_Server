import socket
from waf import inspect_request
from network_acl import is_blocked


# Parses raw HTTP request data into HTTP method, path, protocol version, and headers dictionary
def parse_request(data):
    str_data = data.decode('utf-8', errors= 'ignore')
    request_line , separator, rest = str_data.partition('\r\n') 

    parts = request_line.split(' ')
    if len(parts) != 3:
        return "GET", "/", "HTTP/1.1", {"User-Agent": "TestClient/1.0"} # fallback or throw custom error
    request_type, path, client_proto = parts

    headers_lines = rest.split('\r\n')

    headers = {}
    for line in headers_lines:
        if not line:
            break

        name, value = line.split(':',1)
        value = value.strip()
        headers[name] = value
    
    return request_type,path, client_proto, headers

# Constructs a basic HTTP/1.1 response string with Content-Length and encodes it to UTF-8
def build_response(status, body):
    
    server_proto = "HTTP/1.1"
    length = len(body)
    response = server_proto + " " + status + "\r\nContent-Length: " + str(length) + "\r\n\r\n" + body
    res = response.encode('utf-8')

    return res

# Handles an incoming client connection: verifies IP against ACL, inspects HTTP payload with WAF, and returns response
def handle_client(client_sock, client_ip):
    data = client_sock.recv(1024)
    if not data:
        return
    
    if is_blocked(client_ip):
        res = build_response("403 Forbidden", "<h1>403 Forbidden - IP Blocked by WAF</h1>")
        client_sock.send(res)
        return

    request_type,path, client_proto, headers = parse_request(data)
    allowed = inspect_request(path, headers)
    if allowed:
        status = "200 OK"
        body = "<h1>200 OK - Access Granted</h1>"
    else:
        status = "403 Forbidden"
        body = "<h1>403 Forbidden - Request Blocked by WAF</h1>"
    res = build_response(status, body)
    client_sock.send(res)
    return

# Initializes and runs the TCP socket server on 127.0.0.1:8085 listening for incoming requests
def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', 8085 ))
    server_sock.listen(1)

    while True:
        client_sock, client_add = server_sock.accept()
        client_ip = client_add[0] # the ip address of this client
        try:
            handle_client(client_sock, client_ip)
            client_sock.close()
        except:
            print(f"[ERROR] Failed to handle client:")
            client_sock.close()
  
