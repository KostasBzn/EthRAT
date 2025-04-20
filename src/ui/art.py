from src.ui.colors import Colors as cl
import os

def banner():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    logo = cl.purple + r"""
##################################
 _____ _   _    ______  ___ _____ 
|  ___| | | |   | ___ \/ _ \_   _|
| |__ | |_| |__ | |_/ / /_\ \| |  
|  __|| __| '_ \|    /|  _  || |  
| |___| |_| | | | |\ \| | | || |  
\____/ \__|_| |_\_| \_\_| |_/\_/  

##################################
""" + cl.reset
    print(logo)
    VERSION = "v0.3"
    print(f"{cl.purple}EthRAT {VERSION}{cl.reset}\n\n")
