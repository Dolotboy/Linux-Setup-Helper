import os
import socket
import psutil

def get_system_info():
    return {
        "Nom d'hôte": socket.gethostname(),
        "CPU utilisé": f"{psutil.cpu_percent()}%",
        "RAM utilisée": f"{psutil.virtual_memory().percent}%",
    }
