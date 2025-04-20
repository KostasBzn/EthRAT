from src.ui.colors import Colors as cl
import threading
from threading import Lock
import socket
from datetime import datetime

clients = {}
client_lock = Lock()

def list_clients(clients):
    """ Returns the list of the connected clients """
    if clients:
        print(f"{cl.purple}ID |\tIP                 |\tPORT   |\tHOSTNAME                   |\tSTATUS   |\tLAST SEEN    |{cl.reset}")
        print(f"{cl.purple}___|\t___________________|\t_______|\t___________________________|\t_________|\t_____________|{cl.reset}")
        for id, info in clients.items():
             print(f"{cl.light_green}{id:<3}|\t{info['ip']:<19}|\t{info['port']:<7}|\t{info['hostname']:<25}|\t{info['status']:<9}|\t{info['last'].strftime('%Y-%m-%d %H:%M:%S'):<15}{cl.reset}")
    else:
        print(f"{cl.red}[!] No clients connected.{cl.reset}")

def get_client_by_id(clients, choice):
    """ Get the client socket based on user choise """
    for id, info in clients.items():
        if int(choice) == id:
            if info['status'] == 'online':
                return info
            else:
                raise Exception("The current client is offline")
    raise Exception("This session ID is not valid")
        
def client_disconnection(ip, port):
    """Changes the status when a client is disconnected """
    with client_lock:
        for cl_id, cl_info in clients.items():
            if cl_info['ip'] == ip and cl_info['port'] == port:
                cl_info['status'] = "offline"
                cl_info['last'] = datetime.now()
    print(f"{cl.yellow}[!] Client {cl_info['ip'] }:{port} disconnected{cl.reset} ")

def client_connection(client_socket, addr):
    """Check if the client was previously connected before we add him"""
    for cl_id, cl_info in clients.items():
        if cl_info['ip'] == addr[0]:
            cl_info['status'] = "online"
            cl_info['last'] = datetime.now()
            print(f"{cl.green}[+] Client {addr[0]:}:{addr[1]} is online{cl.reset}")
            return   
    with client_lock:
        cl_id = max(clients.keys(), default=-1) + 1
        clients[cl_id] = {
            "ip": addr[0],
            "local_ip": "unknown",
            "port": addr[1],
            "socket": client_socket,
            "status": "online",
            "hostname": "unknown",
            "last" : datetime.now()
        }
    print(f"{cl.green}[+] New client {addr[0]:}:{addr[1]} connected{cl.reset} ")

def handle_client(sock):
    """Accepts a single client connection """
    try:
        while True:
            try:
                client_socket, addr = sock.accept()
                client_connection(client_socket, addr)
                threading.Thread(target=monitor_client, args=(client_socket, addr), daemon=True).start()
            except (OSError, socket.error) as e:
                print(f"{cl.red}[!] Error accepting client: {e}{cl.reset}")
    except Exception as e:
        print(f"{cl.red}[!] Unexpected error in handle_client: {e}{cl.reset}")

def monitor_client(client_socket, addr):
    """Handles disconnections"""
    try:
        while True:
            try:
                data = client_socket.recv(1, socket.MSG_PEEK)
                if not data: 
                    client_disconnection(addr[0], addr[1])
                    break
            except (OSError, socket.error ) as e:
                print(f"{cl.red}[!] Socket error with client {addr[0]}:{addr[1]}: {e}{cl.reset}")
                client_disconnection(addr[0], addr[1])
                break
    except Exception as e:
        print(f"{cl.red}[!] Error in monitor_client ({addr[0]}:{addr[1]}): {e}{cl.reset}")
        client_disconnection(addr[0], addr[1])
        client_socket.close()