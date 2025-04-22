import struct
from src.ui.colors import Colors as cl

def send(sock, data):
    """Bulk Send Commands And Data"""
    try:
        if isinstance(data, str):
            data = data.encode()
        data_size = len(data)
        sock.sendall(struct.pack('>I', data_size))  
        sock.sendall(data) 
    except (ConnectionError, struct.error, OSError) as e:
        print(f"{cl.red}[!] Send failed: {e}{cl.reset}")
        raise

def recv(sock):
    """ Receive First Letter, Then Return the rest """
    try:
        data_size = recvall(sock, 4)
        if not data_size:
            return None
        data_len = struct.unpack('>I', data_size)[0]
        return recvall(sock, data_len)
    except (ConnectionError, struct.error, OSError) as e:
        print(f"{cl.red}[!] Receive failed: {e}{cl.reset}")
        raise

def recvall(sock, d_len):
    """ Bulk Receive Data, Including Files """
    try:
        packet = b''
        while len(packet) < d_len:
          chunk = sock.recv(d_len - len(packet))
          if not chunk:
            return None
          packet += chunk
        return packet
    except (ConnectionError, struct.error, OSError) as e:
        print(f"{cl.red}[!] Receive all failed: {e}{cl.reset}")
        raise