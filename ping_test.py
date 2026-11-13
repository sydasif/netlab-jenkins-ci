import socket

routers = ["192.168.121.101", "192.168.121.102", "192.168.121.103", "192.168.121.104"]
for ip in routers:
    try:
        s = socket.create_connection((ip, 22), timeout=2)
        print(f"Router {ip} SSH port 22 is REACHABLE")
        s.close()
    except Exception as e:
        print(f"Router {ip} NOT reachable: {e}")

