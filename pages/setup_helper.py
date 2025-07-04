import os
import tkinter as tk
from tkinter import messagebox
import subprocess
import config
from models.application import Application

class SetupHelperFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2D2D2D")

        num_columns = config.num_columns
        card_width = 200
        frames = []

        canvas = tk.Canvas(self, bg="#2D2D2D")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2D2D2D")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mouse_wheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", on_mouse_wheel)
        canvas.bind_all("<Button-5>", on_mouse_wheel)

        row = 0
        col = 0

        for section, apps in config.applications_by_section.items():
            section_label = tk.Label(scrollable_frame, text=section, font=("Arial", 16, "bold"), fg="#E95420", bg="#2D2D2D")
            section_label.grid(row=row, column=0, columnspan=num_columns, pady=10)
            row += 1

            for app in apps:
                frame = tk.Frame(scrollable_frame, relief="raised", borderwidth=1, bg="#2D2D2D", width=card_width)
                frame.grid_propagate(True)
                frame.grid(row=row, column=col, padx=10, pady=10)

                frames.append(frame)

                label = tk.Label(frame, text=app.name, font=("Arial", 12, "bold"), fg="#E95420", bg="#2D2D2D", wraplength=card_width - 10)
                label.pack(pady=5)

                description_label = tk.Label(frame, text=app.description, fg="white", bg="#2D2D2D", wraplength=card_width - 10)
                description_label.pack(pady=5)

                button = tk.Button(frame, text="Installer", command=lambda a=app: run_commands(a.open_console, a.commands), bg="#E95420", fg="white")
                button.pack(side="bottom", pady=5)

                col += 1
                if col == num_columns:
                    col = 0
                    row += 1

            row += 1

        self.update_idletasks()
        max_height = max(frame.winfo_height() for frame in frames)
        for frame in frames:
            frame.config(height=max_height)
            frame.grid_propagate(False)

def run_commands(open_console, commands):
    try:
        in_docker = os.path.exists('/.dockerenv')
        if not open_console or in_docker:
            for command in commands:
                print(f"Exécution : {command}")
                subprocess.run(command, shell=True, check=True)
        else:
            command_str = " && ".join(commands)
            print(f"Exécution : {command_str}")
            subprocess.run(f"gnome-terminal -- bash -c '{command_str}; exec bash'", shell=True, check=True)
        messagebox.showinfo("Succès", "Toutes les commandes ont été exécutées avec succès.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution de la commande : {e}")
        if e.stderr:
            print(e.stderr.decode())
