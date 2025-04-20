import platform
import socket


IP = "127.0.0.1"
PORT = 4444
ARC = platform.system()

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        print("Connected to server...")
        
    
    except Exception as e:
        print(f"Connection error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
