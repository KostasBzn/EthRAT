from src.ui.colors import Colors as cl
from rich.console import Console
from rich.table import Table

def show_main_help():
    """Displays the main command help menu"""
    console = Console()
    
    table = Table(title=f"{cl.cyan}Main Command Menu{cl.reset}", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="dim", width=12)
    table.add_column("Description", min_width=20)
    
    # Add commands
    table.add_row("sessions", "List all connected clients")
    table.add_row("sessions [ID]", "Interact with specific client")
    table.add_row("broadcast", "Send command to all clients")
    table.add_row("exit", "Shutdown the server")
    table.add_row("help", "Show this menu")
    
    console.print(table)

show_main_help()