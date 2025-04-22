# Eth Rat 🐀

**Eth Rat** is an **ethical remote shell tool (RAT)** for cybersecurity education and testing purposes. It is written in Python, and it allows you to remotely manage and interact with systems in a controlled, ethical environment.

## Features
- **Remote Command Execution** – Send and execute commands to connected clients.
- **Download Files/Folders from Client** – Download single files or whole directories. 
- **Push files to Client** – Send files to the clients current directory.
- **Multi-Client Management** – Manage multiple clients at once.  
- **Cross-Platform Compatibility** – Works on **Windows and Linux**.  
- **Educational Focus** – Built for **learning and testing** in a responsible manner.  
- **User-Friendly Interface** – Simple setup with an interactive command menu.  
- **Directory Navigation** – Use `cd` to navigate directories on the client.   

## Project Preview
![Tool Screenshot](https://raw.githubusercontent.com/KostasBzn/EthRAT/refs/heads/main/png/Screenshot1.png)



## Purpose
Eth Rat is written to help practice remote shell techniques in a safe and ethical manner. It is **not intended for malicious use**.

## Usage
1. **Start the server**  
   ```bash
   python server.py -lhost 0.0.0.0 -lport 4444
   ```
2. **Connect clients** to the server.  
3. **Manage sessions** Once clients are connected, you can interact with them through an interactive session system.
4. Supported commands:
   - `help` – Help menu with available commands 
   - `sesssions` – List the connected clients.
   - `sessions <ID>` – Interact with a specific client session
   - `sessions kill <ID` – Kill a session
   - `getip` – Retrieve the client's public IP.  
   - `cd <navigation commands>` – Change the working directory on the client.  
   - `download <file/folder>` – Downloads the file or folder.
   - `upload` – Opens file dialog to choose a file to push to the client.
   - `kill` – Kill the current client connection
   - `back` – Return to the main menu.  
   - `exit` – Shut down the server.  
   - And more. Use the `help` function for all the available commands

## Ethical Disclaimer
This tool is **strictly for educational and ethical testing purposes only**. **Misuse is prohibited** and may violate laws.