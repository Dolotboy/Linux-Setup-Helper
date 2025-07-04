import tkinter as tk
from system_info import get_system_info
from pages.homepage import HomePageFrame
from pages.task_manager import TaskManagerFrame
from pages.setup_helper import SetupHelperFrame
from pages.docker_helper import DockerHelperFrame, is_docker_available

class LinuxControlCenter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Linux Control Center")
        self.geometry("1000x700")
        self.configure(bg="#1E1E1E")

        # Menu latéral
        self.sidebar = tk.Frame(self, bg="#2D2D2D", width=200)
        self.sidebar.pack(side="left", fill="y")

        # Zone de contenu principal
        self.main_content = tk.Frame(self, bg="#1E1E1E")
        self.main_content.pack(side="right", fill="both", expand=True)

        # Onglets disponibles
        self.pages = {
            "Accueil": HomePageFrame,
            "Task Manager": TaskManagerFrame,
            "Setup Helper": SetupHelperFrame,
        }

        # Ajouter dynamiquement Docker si installé
        if is_docker_available():
            self.pages["Docker"] = DockerHelperFrame

        # Création des boutons du menu
        for name in self.pages:
            button = tk.Button(
                self.sidebar, text=name, fg="white", bg="#3C3C3C",
                command=lambda n=name: self.show_frame(n)
            )
            button.pack(fill="x", padx=5, pady=5)

        # Initialiser avec la page d’accueil
        self.show_frame("Accueil")

    def show_frame(self, name):
        # Clear ancien contenu
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Afficher nouvelle page
        if callable(self.pages[name]):
            page = self.pages[name](self.main_content)
        else:
            page = self.pages[name]

        page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = LinuxControlCenter()
    app.mainloop()
