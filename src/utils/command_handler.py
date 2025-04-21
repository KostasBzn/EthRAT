from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from src.ui.colors import Colors as cl
from src.utils.client_handler import get_client_by_id, list_clients, clients, handle_client
from src.ui.help import show_main_help, show_client_help



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

            elif cmd.startswith("sessions "):
                choice = cmd[8:].strip()
                cl_info = get_client_by_id(clients, choice)
                print(f"{cl.cyan}[+] Switching to client {cmd}{cl.reset}")
                client_loop(cl_info)

            elif cmd.strip() == "sessions":
                list_clients(clients) 

            elif cmd.strip() == "broadcast": 
                print("Broadcasting function logic to implimented later")
            else:
                print(f"{cl.red}[!] Unknown command. Type 'help' for options.{cl.reset}")
        except KeyboardInterrupt:  
            continue 
        except Exception as e:
            print(f"{cl.red}[!] Cmd error: {e}{cl.reset}")

def client_loop(client_info):
    """Handles the client-specific command loop"""
    cl_prompt = f"client_{client_info['ip']}> "
    cl_commands = ["shell", "download", "upload", "help", "back"]  
    completer = WordCompleter(cl_commands)  
    cl_session = PromptSession(completer=completer, history=InMemoryHistory())
    
    while True:
        try:
            cmd = cl_session.prompt(cl_prompt).strip()
            
            if cmd == "shell":
                print(f"{cl.green}[+] Starting shell session on client {client_info['id']}...{cl.reset}")
                
            elif cmd.strip() == "download":
                print(f"{cl.green}[+] Downloading..{cl.reset}")
                    
            elif cmd.strip() == "upload":
                print(f"{cl.green}[+] Uploading..{cl.reset}")
                
            elif cmd == "getip":
                print(f"{cl.cyan}[*] Client {client_info['id']} IP Report:")
                print(f"    Local IP: {client_info.get('local_ip', 'unknown')}")
                print(f"    Public IP: {client_info.get('public_ip', 'unknown')}{cl.reset}")
            
            elif cmd == "kill":
                print(f"{cl.blue}[-] Killing the session with the client{cl.reset}")
                break

            elif cmd == "back":
                print(f"{cl.blue}[+] Returning to main session{cl.reset}")
                break
                
            elif cmd == "help":
                show_client_help()
                
            elif cmd:
                print(f"{cl.red}[!] Unknown command. Type 'help' for options.{cl.reset}")
                
        except KeyboardInterrupt:
            print(f"\n{cl.yellow}[!] Type 'back' to return to main session{cl.reset}")
            continue