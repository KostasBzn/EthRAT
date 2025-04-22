from src.ui.colors import Colors as cl
from src.utils.net_io import recv
import threading
from threading import Lock
import socket
from datetime import datetime
from rich.console import Console
from rich.table import Table
import json

clients = {}
client_lock = Lock()

def list_clients(clients):
    """ Returns the list of the connected clients """
    if clients:
        console = Console()
        table = Table(title=f"{cl.cyan}Sessions{cl.reset}", show_header=True, header_style="bold purple")
        table.add_column("ID", min_width=5)
        table.add_column("IP", min_width=13)
        table.add_column("PORT", min_width=8)
        table.add_column("MAC", min_width=20)
        table.add_column("HOSTNAME", min_width=12)
        table.add_column("LOCAL_IP", min_width=12)
        table.add_column("STATUS", min_width=10)
        table.add_column("LAST SEEN", min_width=15)
        for id, info in clients.items():
            table.add_row(str(id), info['ip'], str(info['port']), info['mac'], info['hostname'], info['local_ip'], info['status'], info['last'].strftime('%Y-%m-%d %H:%M:%S'))
        console.print(table)
    else:
        print(f"{cl.red}[!] No clients connected.{cl.reset}")

def get_client_by_id(clients, choice):
    """ Get the client socket based on user choise """
    for id, info in clients.items():
        if int(choice) == id:
                return info
    raise Exception("This session ID is not valid")

def remove_client(cl_id):
    """Remove client from the list after killing the session """
    for id, info in clients.items():
        if int(cl_id) == id:
            del clients[id]
            break
        else:
            print(f"{cl.yellow}[!] Session {cl_id} not found{cl.reset}")
    print(f"{cl.light_green}[+] Session {cl_id} removed{cl.reset}")
    
def client_disconnection(ip, port, clinfo):
    """Changes the status when a client is disconnected """
    with client_lock:
        for cl_id, cl_info in clients.items():
            if cl_info['port'] == port or cl_info['mac'] == clinfo['mac']:
                cl_info['status'] = "offline"
                cl_info['last'] = datetime.now()
    #print(f"{cl.yellow}[!] Client {cl_info['ip'] }:{port} disconnected{cl.reset} ")

def client_connection(client_socket, addr, clinfo):
    """Check if the client was previously connected before we add him"""
    for cl_id, cl_info in clients.items():
        if cl_info['mac'] == clinfo['mac']:
            cl_info['status'] = "online"
            cl_info['port'] = addr[1]
            cl_info['ip'] = addr[0]
            cl_info['socket'] = client_socket
            cl_info['local_ip'] = clinfo['lip']
            cl_info['last'] = datetime.now()
            print(f"{cl.green}[+] Client {addr[0]:}:{addr[1]} is online{cl.reset}")
            return   
    with client_lock:
        cl_id = max(clients.keys(), default=-1) + 1
        clients[cl_id] = {
            "ip": addr[0],
            "port": addr[1],
            "socket": client_socket,
            "local_ip": clinfo['lip'],
            "hostname": clinfo['hname'],
            "mac": clinfo['mac'],
            "status": "online",
            "last" : datetime.now()
        }
    print(f"{cl.green}[+] New client {addr[0]:}:{addr[1]} connected{cl.reset} ")

def handle_client(sock):
    """Accepts a single client connection """
    try:
        client_socket, addr = sock.accept()
        data = recv(client_socket)
        if data:
            clinfo = json.loads(data.decode())
            client_connection(client_socket, addr, clinfo)
        threading.Thread(target=monitor_client, args=(client_socket, addr, clinfo), daemon=True).start()
    except (Exception, OSError, socket.error) as e:
        print(f"{cl.red}[!] Error accepting client: {e}{cl.reset}")


def monitor_client(client_socket, addr, clinfo):
    """Handles disconnections"""
    try:
        while True:
            try:
                data = client_socket.recv(1, socket.MSG_PEEK)
                if not data: 
                    client_disconnection(addr[0], addr[1], clinfo)
                    break
            except (OSError, socket.error ) as e:
                print(f"{cl.red}[!] Socket error with client {addr[0]}:{addr[1]}: {e}{cl.reset}")
                client_disconnection(addr[0], addr[1], clinfo)
                break
    except Exception as e:
        print(f"{cl.red}[!] Error in monitor_client ({addr[0]}:{addr[1]}): {e}{cl.reset}")
        client_disconnection(addr[0], addr[1], clinfo)
        client_socket.close()