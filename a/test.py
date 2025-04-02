import socket
from tkinter.filedialog import askdirectory
import os

aa = socket.gethostbyname(socket.gethostname())
print(aa)

def save_file():    
    save_path = askdirectory(
        title="Select download directory",
        initialdir= os.getcwd()
    )
    if not save_path:
        print(f"No save location selected.")
        return
    print(f"File will be saved at: {save_path}")
    return save_path

save_path = save_file()

print(save_path)
for a,b,c in os.walk(os.getcwd()):
    print("a",a)
    print("b",b)
    print("c",c)