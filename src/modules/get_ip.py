import json
from src.ui.colors import Colors as cl
from rich.console import Console
from rich.table import Table


def print_ip(data):
    ip_info = json.loads(data.decode())
    console = Console()    
    ip_table = Table(show_header=False)
    ip_table.add_row("Local IP", ip_info.get('lip', 'unknown'))
    ip_table.add_row("Public IP", ip_info.get('pip', 'unknown'))
    console.print(ip_table)

