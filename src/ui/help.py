from src.ui.colors import Colors as cl
from rich.console import Console
from rich.table import Table

def show_main_help():
    """Displays the main command help menu"""
    console = Console()
    
    table = Table(title=f"{cl.cyan}Main Command Menu{cl.reset}", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="dim", width=16)
    table.add_column("Description", min_width=25)
    
    table.add_row("listen", "Wait for clients")
    table.add_row("sessions", "List all sessions")
    table.add_row("sessions <ID>", "Interact with specific session")
    table.add_row("sessions kill <ID>", "Kill a session")
    table.add_row("broadcast", "Send command to all clients")
    table.add_row("exit", "Shutdown the server")
    table.add_row("help", "Show this menu")
    
    console.print(table)

def show_client_help():
    """Help menu when interacting with a client"""
    console = Console()
    
    table = Table(title=f"{cl.cyan}Client Session Commands{cl.reset}", show_header=True, header_style="bold yellow")
    table.add_column("Command", style="dim", width=16)
    table.add_column("Description", min_width=25)
    
    table.add_row("shell", "Start interactive shell")
    table.add_row("download", "Download file/folder from client")
    table.add_row("upload", "Upload file to client")
    table.add_row("getip", "Get public and local ip from the client")
    table.add_row("back", "Return to main session")
    table.add_row("help", "Show this menu")
    
    console.print(table)
