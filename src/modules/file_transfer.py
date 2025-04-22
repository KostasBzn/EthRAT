from src.ui.colors import Colors as cl
from src.utils.net_io import send, recv, recvall
from src.utils.file_dialog import open_file, save_file
import os

def download(cl_socket, cmd):
    """Download a file/folder from the client"""
    try:
        save_dir = save_file()
        print(f"{cl.cyan}[*] File will be saved at: {save_dir}{cl.reset}")
        send(cl_socket, cmd)
        file_name_data = recv(cl_socket)
        if file_name_data and file_name_data.decode().startswith("FILE_NAME:"):
           file_name = file_name_data.decode()[len("FILE_NAME:"):].strip()
           print(f"{cl.cyan}[*] Downloading...{cl.reset}")
        data = recv(cl_socket)
        if data.startswith(b"ERROR"):
            print(data.decode())
        else:
            full_save_path = os.path.normpath(os.path.join(save_dir, file_name))
            with open(full_save_path, "wb") as f:
                f.write(data)
            print(f"{cl.green}[+] File downloaded{cl.reset}")

    except Exception as e:
        print(f"{cl.red}Download error: {e}{cl.reset}")


def upload(cl_socket, cmd):
    """Upload a file to the client"""
    file_path, file_name = open_file()
    cmd = f"{cmd} {file_name}"
    if not file_path or not file_name:
        return
    try:
        send(cl_socket, cmd)
        print(f"{cl.cyan}[*] Uploading '{file_name}'...{cl.reset}")
        with open(file_path,"rb") as f_up:
            data = f_up.read()
        send(cl_socket, data)
        res = recv(cl_socket)
        if res.startswith(b"ERROR"):
            print(res.decode())
        else:
            print(f"{cl.yellow}[*] Client response: {res.decode()}{cl.reset}")
            print(f"{cl.green}[+] Upload successful{cl.reset}")
    except Exception as e:
        print(f"{cl.red}Upload error: {e}{cl.reset}")

