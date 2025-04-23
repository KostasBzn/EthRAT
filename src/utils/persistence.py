from src.ui.colors import Colors as cl
from src.utils.net_io import recv, send

def persistence(cl_info, cmd):
    try:
        if cl_info['status'] == "online":
            send(cl_info['socket'], cmd)
            res = recv(cl_info['socket'])
            if res:
                print(f"{cl.light_green}[#] Result: {res.decode()}{cl.reset}")
    except Exception as e:
        print(f"{cl.red}[!] Persistence error: {e}{cl.reset}")
