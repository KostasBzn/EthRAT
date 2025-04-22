from prompt_toolkit import PromptSession
from src.utils.net_io import recv, send
from src.ui.colors import Colors as cl

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