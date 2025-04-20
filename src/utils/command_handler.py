from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from src.ui.colors import Colors as cl
from src.utils.client_handler import get_client_by_id, list_clients, clients
from src.ui.help import show_main_help

session = PromptSession(history=InMemoryHistory())

commands = ["sessions", "broadcast", "exit", "help"]  
completer = WordCompleter(commands)  
session = PromptSession(completer=completer, history=InMemoryHistory())  

def main_loop():
    while True:  
        try:  
            cmd = session.prompt("cmd> ")  
            if cmd == "exit":  
                if cmd == "exit":
                    confirm = input("Exit server? (y/n): ").lower()
                    if confirm == 'y':
                        exit()

            elif cmd == "help":
                show_main_help()

            elif cmd.startswith("sessions"):
                choice = cmd[8:].strip()
                cl_info = get_client_by_id(clients, choice)
                print(f"{cl.cyan}[+] Switching to client {cmd}{cl.reset}")
                
                print(f"Interract with client {cl_info['ip']}:{cl_info['port']} logic to implimented later")


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