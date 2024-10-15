import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import config

class Application:
    def __init__(self, name, description, image, open_console, commands):
        self.name = name
        self.description = description
        self.image = image
        self.open_console = open_console
        self.commands = commands

    def __repr__(self):
        return f"Application(name={self.name}, description={self.description}, image={self.image})"


def run_commands(open_console, commands):
    try:
        # Détecter si nous sommes dans un conteneur Docker
        in_docker = os.path.exists('/.dockerenv')

        if not open_console or in_docker:
            for command in commands:
                print(f"Exécution : {command}")
                subprocess.run(command, shell=True, check=True)
        else:
            # Joindre les commandes avec "&&" pour les exécuter séquentiellement
            command_str = " && ".join(commands)
            print(f"Exécution : {command_str}")

            # Exécuter les commandes dans un terminal Gnome (hors Docker)
            subprocess.run(f"gnome-terminal -- bash -c '{command_str}; exec bash'", shell=True, check=True)
        
        messagebox.showinfo("Succès", "Toutes les commandes ont été exécutées avec succès.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution de la commande : {e}")
        print(e.stderr.decode())


# Création de l'interface Tkinter avec Scrollbar
def create_gui():
    root = tk.Tk()
    root.title("Gestionnaire d'applications")

    window_width = config.window_width
    window_height = config.window_height
    root.geometry(f"{window_width}x{window_height}")

    # Définir le fond de la fenêtre
    root.configure(bg="#2D2D2D")  # RGB(45, 45, 45)

    # Créer un conteneur Canvas pour ajouter le support de scroll
    canvas = tk.Canvas(root, bg="#2D2D2D")  # Fond du Canvas
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#2D2D2D")  # Fond du cadre défilant

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Organiser le Canvas et la Scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Activation du scroll au centre avec la molette
    def on_mouse_wheel(event):
        # Gestion du défilement sur Windows et macOS
        if event.delta:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # Gestion du défilement sur Linux (Button-4 pour scroll up et Button-5 pour scroll down)
        elif event.num == 4:  # Scroll up
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            canvas.yview_scroll(1, "units")

    # Lier la molette au canvas (pour Windows et macOS)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Pour Windows/macOS
    canvas.bind_all("<Button-4>", on_mouse_wheel)    # Pour Linux (scroll up)
    canvas.bind_all("<Button-5>", on_mouse_wheel)    # Pour Linux (scroll down)

    row = 0  # Compte les lignes
    col = 0  # Compte les colonnes

    num_columns = config.num_columns  # Récupère le nombre de colonnes depuis le fichier de configuration

    card_width = 200  # Largeur fixe des cartes

    # Liste pour stocker toutes les cartes (frames)
    frames = []

    # Pour chaque section dans le dictionnaire
    for section, apps in config.applications_by_section.items():
        # Créer une étiquette pour la section (sur une ligne séparée)
        section_label = tk.Label(scrollable_frame, text=section, font=("Arial", 16, "bold"), fg="#E95420", bg="#2D2D2D")
        section_label.grid(row=row, column=0, columnspan=num_columns, pady=10)  # Occupe toutes les colonnes
        row += 1  # Passer à la ligne suivante après l'étiquette de la section

        for app in apps:
            # Créer un cadre pour chaque application
            frame = tk.Frame(scrollable_frame, relief="raised", borderwidth=1, bg="#2D2D2D", width=card_width)
            frame.grid_propagate(True)  # Permet au cadre de se redimensionner en fonction du contenu
            frame.grid(row=row, column=col, padx=10, pady=10)  # Placer le cadre dans la grille

            # Stocker chaque frame dans la liste des frames
            frames.append(frame)

            # Nom de l'application (wrap sur plusieurs lignes si nécessaire)
            label = tk.Label(frame, text=app.name, font=("Arial", 12, "bold"), fg="#E95420", bg="#2D2D2D", wraplength=card_width - 10)
            label.pack(pady=5)

            # Description de l'application (wrap sur plusieurs lignes si nécessaire)
            description_label = tk.Label(frame, text=app.description, fg="white", bg="#2D2D2D", wraplength=card_width - 10)
            description_label.pack(pady=5)

            # Bouton pour exécuter les commandes
            button = tk.Button(frame, text="Installer", command=lambda a=app: run_commands(a.open_console, a.commands), bg="#E95420", fg="white")
            button.pack(side="bottom", pady=5)

            # Gestion des colonnes et lignes pour créer l'effet wrap selon le nombre de colonnes défini
            col += 1
            if col == num_columns:  # Si on a rempli toutes les colonnes
                col = 0  # Réinitialiser la colonne à 0
                row += 1  # Passer à la ligne suivante

        row += 1  # Ajouter une ligne vide entre les sections

    # Calculer la hauteur maximale parmi toutes les cartes
    root.update_idletasks()  # Assure que tout soit dessiné avant de calculer les hauteurs
    max_height = max(frame.winfo_height() for frame in frames)

    # Appliquer cette hauteur maximale à toutes les cartes
    for frame in frames:
        frame.config(height=max_height)
        frame.grid_propagate(False)  # Désactiver la propagation du redimensionnement après avoir fixé la hauteur

    root.mainloop()

# Exécuter l'interface
if __name__ == "__main__":
    create_gui()
    input("Appuyez sur Entrée pour fermer...")