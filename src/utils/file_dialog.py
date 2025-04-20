import os
from tkinter.filedialog import askdirectory, askopenfilename
from src.ui.colors import Colors as cl

def save_file():    
    save_path = askdirectory(
        title="Select download directory",
        initialdir= os.getcwd()
    )
    if not save_path:
        print(f"{cl.red}[!] No save location selected.{cl.reset}")
        return
    return save_path

def open_file():
    file_path = askopenfilename(
        title="Select your file",
        filetypes=[("All files", "*.*")]
    )
    if not file_path:
        print(f"{cl.red}[!] No file selected.{cl.reset}")
        return
    file_name = os.path.basename(file_path)
    return file_path, file_name