import socket
import platform
import uuid

def show_main_help():
    ARC = platform.node()
    local_ip = str(socket.gethostbyname(socket.gethostname()))
    mac = uuid.getnode()
    mac_str = ':'.join(['{:02x}'.format((mac >> ele) & 0xff) for ele in range(40, -1, -8)])
    print(ARC)
    print(local_ip)
    print(mac_str)

show_main_help()


def get_mac_address():
    mac = uuid.getnode()
    mac_str = ':'.join(['{:02x}'.format((mac >> ele) & 0xff) for ele in range(40, -1, -8)])
    return mac_str
