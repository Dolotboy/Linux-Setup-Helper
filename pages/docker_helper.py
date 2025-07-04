import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil

class DockerHelperFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1E1E1E")

        # === Zone scrollable ===
        canvas = tk.Canvas(self, bg="#1E1E1E", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#1E1E1E")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.build_ui()

    def build_ui(self):
        # === Conteneurs ===
        tk.Label(self.scrollable_frame, text="Conteneurs actifs :", fg="white", bg="#1E1E1E", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(10, 0))

        self.container_listbox = tk.Listbox(self.scrollable_frame, height=6, bg="#2D2D2D", fg="white", selectbackground="#444444")
        self.container_listbox.pack(fill="x", padx=20, pady=(0, 5))

        tk.Button(self.scrollable_frame, text="Rafraîchir", command=self.update_container_list, bg="#E95420", fg="white").pack(pady=(0, 15))

        # === Entrée de commande ===
        tk.Label(self.scrollable_frame, text="Commande dans le conteneur sélectionné :", fg="white", bg="#1E1E1E", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))

        self.command_entry = tk.Entry(self.scrollable_frame, width=60, bg="#2D2D2D", fg="white", insertbackground="white")
        self.command_entry.pack(padx=20, pady=5)

        tk.Button(self.scrollable_frame, text="Exécuter la commande", command=self.run_command_in_container, bg="#E95420", fg="white").pack(padx=20, pady=5)

        # === Console output ===
        tk.Label(self.scrollable_frame, text="Sortie de la commande :", fg="white", bg="#1E1E1E", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(20, 0))

        output_frame = tk.Frame(self.scrollable_frame, bg="#1E1E1E")
        output_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.output_text = tk.Text(output_frame, height=10, bg="#2D2D2D", fg="white", insertbackground="white", wrap="word")
        self.output_text.pack(side="left", fill="both", expand=True)

        output_scrollbar = tk.Scrollbar(output_frame, command=self.output_text.yview)
        output_scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=output_scrollbar.set)

        # === Sélection dossier ===
        folder_frame = tk.Frame(self.scrollable_frame, bg="#1E1E1E")
        folder_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.folder_label = tk.Label(folder_frame, text="Aucun dossier sélectionné", fg="white", bg="#1E1E1E", width=40, anchor="w")
        self.folder_label.pack(side="left", padx=5)

        tk.Button(folder_frame, text="Choisir dossier", command=self.select_folder, bg="#E95420", fg="white").pack(side="right", padx=5)

        # === Boutons fichiers ===
        button_frame = tk.Frame(self.scrollable_frame, bg="#1E1E1E")
        button_frame.pack(padx=20, pady=10)

        self.create_dockerfile_btn = tk.Button(button_frame, text="Créer Dockerfile", command=self.create_dockerfile, bg="#E95420", fg="white", state=tk.DISABLED)
        self.create_dockerfile_btn.grid(row=0, column=0, padx=5, pady=5)

        self.create_compose_btn = tk.Button(button_frame, text="Créer docker-compose.yml", command=self.create_docker_compose, bg="#E95420", fg="white", state=tk.DISABLED)
        self.create_compose_btn.grid(row=0, column=1, padx=5, pady=5)

        self.compose_up_btn = tk.Button(button_frame, text="Compose Up", command=self.compose_up, bg="#E95420", fg="white", state=tk.DISABLED)
        self.compose_up_btn.grid(row=1, column=0, padx=5, pady=5)

        self.compose_down_btn = tk.Button(button_frame, text="Compose Down", command=self.compose_down, bg="#E95420", fg="white", state=tk.DISABLED)
        self.compose_down_btn.grid(row=1, column=1, padx=5, pady=5)

        self.update_container_list()

    def update_container_list(self):
        self.container_listbox.delete(0, tk.END)
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True
            )
            containers = result.stdout.strip().splitlines()
            if not containers:
                self.container_listbox.insert(tk.END, "(Aucun conteneur actif)")
            else:
                for container in containers:
                    self.container_listbox.insert(tk.END, container)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les conteneurs :\n{e}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=folder)
            self.check_docker_files()

    def check_docker_files(self):
        dockerfile = os.path.join(self.folder_path, "Dockerfile")
        composefile = os.path.join(self.folder_path, "docker-compose.yml")

        self.create_dockerfile_btn.config(state=tk.NORMAL if not os.path.exists(dockerfile) else tk.DISABLED)
        self.create_compose_btn.config(state=tk.NORMAL if not os.path.exists(composefile) else tk.DISABLED)
        self.compose_up_btn.config(state=tk.NORMAL if os.path.exists(composefile) else tk.DISABLED)
        self.compose_down_btn.config(state=tk.NORMAL if os.path.exists(composefile) else tk.DISABLED)

    def create_dockerfile(self):
        if self.folder_path:
            path = os.path.join(self.folder_path, "Dockerfile")
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write("FROM python:3.8-slim\n")
                messagebox.showinfo("Succès", "Dockerfile créé.")
                self.check_docker_files()

    def create_docker_compose(self):
        if self.folder_path:
            path = os.path.join(self.folder_path, "docker-compose.yml")
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write("version: '3'\nservices:\n  app:\n    image: python:3.8-slim\n")
                messagebox.showinfo("Succès", "docker-compose.yml créé.")
                self.check_docker_files()

    def compose_up(self):
        try:
            subprocess.run(["docker-compose", "up", "-d"], cwd=self.folder_path, check=True)
            messagebox.showinfo("Succès", "Compose Up exécuté.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du lancement :\n{e}")

    def compose_down(self):
        try:
            subprocess.run(["docker-compose", "down"], cwd=self.folder_path, check=True)
            messagebox.showinfo("Succès", "Compose Down exécuté.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'arrêt :\n{e}")

    def run_command_in_container(self):
        container = self.get_selected_container()
        if not container:
            messagebox.showwarning("Aucun conteneur", "Veuillez sélectionner un conteneur dans la liste.")
            return

        command = self.command_entry.get().strip()
        if not command:
            messagebox.showwarning("Commande vide", "Veuillez entrer une commande à exécuter.")
            return

        full_command = ["docker", "exec", container] + command.split()

        self.output_text.delete(1.0, tk.END)  # Vide l'ancienne sortie
        self.output_text.insert(tk.END, f"$ docker exec {container} {command}\n\n")

        try:
            result = subprocess.run(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            self.output_text.insert(tk.END, result.stdout)
            if result.stderr:
                self.output_text.insert(tk.END, "\n[stderr]\n" + result.stderr)
        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"[ERREUR] :\n{e.stderr or str(e)}")

    def get_selected_container(self):
        selection = self.container_listbox.curselection()
        if not selection:
            return None
        return self.container_listbox.get(selection[0])

def is_docker_available():
    return shutil.which("docker") is not None or os.path.exists("/var/run/docker.sock")
