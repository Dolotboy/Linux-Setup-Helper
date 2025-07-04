import tkinter as tk
from tkinter import ttk
import psutil

class TaskManagerFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")

        # Titre
        title = tk.Label(self, text="Gestionnaire des tâches", font=("Arial", 16, "bold"), fg="#E95420", bg="#1E1E1E")
        title.pack(pady=10)

        # Cadre pour le tableau
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar verticale
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        # Table des processus
        self.tree = ttk.Treeview(table_frame, columns=("PID", "Nom", "CPU", "Mémoire"), show="headings", yscrollcommand=scrollbar.set)
        self.tree.column("PID", width=70, anchor="center")
        self.tree.column("Nom", width=300, anchor="w")
        self.tree.column("CPU", width=100, anchor="center")
        self.tree.column("Mémoire", width=100, anchor="center")

        for col in ("PID", "Nom", "CPU", "Mémoire"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Style sombre
        style = ttk.Style()
        style.configure("Treeview", background="#2D2D2D", foreground="white", fieldbackground="#2D2D2D", rowheight=25)
        style.map("Treeview", background=[("selected", "#444444")])

        # Lancer la boucle de mise à jour
        self.update_process_list()

    def update_process_list(self):
        self.tree.delete(*self.tree.get_children())

        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                pid = proc.info["pid"]
                name = proc.info["name"] or "Inconnu"
                cpu = f"{proc.info['cpu_percent']:.1f}%"
                mem = f"{proc.info['memory_percent']:.1f}%"

                self.tree.insert("", "end", values=(pid, name, cpu, mem))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.after(1000, self.update_process_list)
