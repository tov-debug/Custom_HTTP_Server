import socket
import time
from network_acl import load_blacklist, is_blocked

# 1. בדיקת יחידה לרשימה השחורה (ACL)
load_blacklist('blacklist.txt')
print("--- ACL Blacklist Tests ---")
print("[V] Blacklisted IP Blocked" if is_blocked("192.168.1.50") else "[X] Failed: IP should be blocked")
print("[V] Clean IP Allowed" if not is_blocked("8.8.8.8") else "[X] Failed: IP should be allowed")

# 2. בדיקת בקשות HTTP מול השרת
def check_server(test_name, payload, expected_status):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8085))
    s.send(payload.encode('utf-8'))
    
    response = s.recv(1024).decode('utf-8')
    s.close()
    
    if expected_status in response:
        print(f"[V] {test_name} - Passed")
    else:
        print(f"[X] {test_name} - Failed")
    time.sleep(0.1)

print("\n--- Server & WAF Integration Tests ---")

# בקשה תקינה
check_server("Valid Request", "GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: Test\r\n\r\n", "200 OK")

# בקשה לא חוקית / שבורה (מופעל מנגנון ה-Fallback בשרת)
check_server("Invalid/Malformed Request", "NOT_HTTP_DATA_STREAM\r\n\r\n", "200 OK")

# מתקפת SQL Injection (נחסם ע"י WAF)
check_server("WAF: SQL Injection", "GET /?q=UNION SELECT HTTP/1.1\r\nHost: localhost\r\nUser-Agent: Test\r\n\r\n", "403 Forbidden")

# מתקפת Path Traversal (נחסם ע"י WAF)
check_server("WAF: Path Traversal", "GET /../../etc/passwd HTTP/1.1\r\nHost: localhost\r\nUser-Agent: Test\r\n\r\n", "403 Forbidden")