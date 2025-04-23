# Eth Rat 🐀

**Eth Rat** is an **ethical remote shell tool (RAT)** for cybersecurity education and testing purposes. It is written in Python, and it allows you to remotely manage and interact with systems in a controlled, ethical environment.

## Features
- **Remote Command Execution** – Send and execute commands to connected clients.
- **Directory Navigation** – Use `cd` to navigate directories on the client.
- **Download Files/Folders from Client** – Download single files or whole directories. 
- **Push files to Client** – Send files to the clients current directory.
- **Persistence** – Implements startup persistence for Windows and Linux clients.
- **Multi-Client Management** – Manage multiple clients at once.  
- **Cross-Platform Compatibility** – Works on **Windows and Linux**.  
- **Educational Focus** – Built for **learning and testing** in a responsible manner.  
- **User-Friendly Interface** – Simple setup with an interactive command menu.  


## Project Preview
![Tool Screenshot](https://raw.githubusercontent.com/KostasBzn/EthRAT/refs/heads/main/png/Screenshot12.png)


## Purpose
Eth Rat is written to help practice remote shell techniques in a safe and ethical manner. It is **not intended for malicious use**.

## Testing Environment
- Tested on:
  - Windows 11
  - Kali Linux  
- Always test in a **controlled lab environment**.

## Usage
1. **Start the server**  
   ```bash
   python server.py -lhost 0.0.0.0 -lport 4444
   ```
2. **Connect clients** to the server.  
3. **Manage sessions** Once clients are connected, you can interact with them through an interactive session system.
4. **Use** `help` to see all the available commands 


## Ethical Disclaimer
This tool is **strictly for educational and ethical testing purposes only**. **Misuse is prohibited** and may violate laws.