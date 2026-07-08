"""Report whether common app ports are free or in use."""
import socket
PORTS = [80, 443, 8501, 8000, 9090, 3000, 9000, 9001]

def is_open(port):
    s = socket.socket()
    s.settimeout(0.3)
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()

for port in PORTS:
    print(f"{port}: {'in use' if is_open(port) else 'free'}")
