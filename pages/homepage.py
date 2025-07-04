import tkinter as tk
from tkinter import messagebox
from system_info import get_system_info
import subprocess
import os

class HomePageFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")
        self.labels = {}

        # ====== INFOS SYSTÈME ======
        for key in ["Nom d'hôte", "CPU utilisé", "RAM utilisée"]:
            label = tk.Label(self, text="", fg="white", bg="#1E1E1E", font=("Arial", 14))
            label.pack(anchor="w", padx=20, pady=5)
            self.labels[key] = label

        self.update_info()

        # ====== BOUTONS D'ACTIONS ======
        button_frame = tk.Frame(self, bg="#1E1E1E")
        button_frame.pack(pady=30)

        actions = [
            ("Redémarrer", "reboot"),
            ("Éteindre", "poweroff"),
            ("Se déconnecter", "gnome-session-quit --logout --no-prompt"),
        ]

        for label, cmd in actions:
            btn = tk.Button(
                button_frame,
                text=label,
                command=lambda c=cmd: self.execute_command(c),
                bg="#E95420",
                fg="white",
                font=("Arial", 12),
                width=20,
                pady=5
            )
            btn.pack(pady=5)

    def update_info(self):
        info = get_system_info()
        for key, label in self.labels.items():
            label.config(text=f"{key} : {info.get(key, 'N/A')}")
        self.after(1000, self.update_info)

    from tkinter import messagebox

    def execute_command(self, command):
        try:
            if os.path.exists("/.dockerenv"):
                messagebox.showwarning("Environnement restreint", f"Commande bloquée en conteneur Docker : {command}")
                return

            # Demander confirmation à l’utilisateur
            confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment exécuter :\n{command} ?")
            if not confirmation:
                return

            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("Succès", f"Commande exécutée :\n{command}")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erreur", f"Échec de la commande :\n{command}\n\n{e}")

