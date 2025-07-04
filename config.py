from models.application import Application

num_columns = 4
window_width = 875
window_height = 700

# Tableau d'objets Application, organisé par sections
applications_by_section = {
    "System": [
        Application("Linux mint version", "Get linux mint version", "mint.png", True, ["cat /etc/issue"]),
        Application("Update & Upgrade", "Update and Upgrade packages", "download.png", True, ["sudo apt update && apt upgrade"]),
        Application("Linux mint upgrade 21.3 to 22", "An update from Linux mint 21.3 to 22", "mint.png", True, [
            "sudo apt update",
            "sudo apt install mintupgrade",
            "sudo mintupgrade",
            "sudo apt remove mintupgrade",
            "sudo reboot"
        ])
    ],
    "Input": [
        Application("Update & Upgrade", "Supprimer", "download.png", True, ["sudo apt update && apt upgrade"]),
        Application("Raccourci Navigateur", "Ctrl+Alt+A", "Firefox.png", False, [
            "gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \"['/org/gnome/settings-daemon/plugins/media-keys/custom-keybinding/custom-open-browser/\']\"; "
            "gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybinding/custom-open-browser/ name 'Ouvrir le navigateur'; "
            "gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybinding/custom-open-browser/ command 'xdg-open http://www.google.com'; "
            "gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybinding/custom-open-browser/ binding '<Super>a'; "
        ]),#gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings
        Application("Supprimer Raccourci Navigateur", "Supprimer", "Firefox.png", True, ["gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings '[]'"])
    ],
    "Gaming": [
        Application("Discord", "Application de chat vocal et textuel. (Require Snap)", "discord.png", True, ["sudo snap install discord"]), #https://discord.com/api/download?platform=linux&format=deb
        Application("Steam", "Plateforme de distribution de jeux.", "steam.png", True, ["sudo apt install steam", "sudo add-apt-repository multiverse", "sudo apt update", "sudo apt install steam"]),
        Application("Lutris", "Gestionnaire de jeux vidéo open-source.", "lutris.png", True, ["sudo apt install lutris"]),
        Application("OpenRazer", "Razer device manager", "razer.png", True, [
            "sudo add-apt-repository ppa:openrazer/stable",
            "sudo add-apt-repository ppa:polychromatic/stable",
            "sudo apt update",
            "sudo apt install openrazer-meta polychromatic",
            "sudo gpasswd -a $USER plugdev",
            "echo restart your computer to apply changes"
        ])
    ],
    "Development": [
        Application("CodeBlock", "IDE pour la programmation en C/C++.", "codeblock.png", True, ["codeblocks", "sudo apt install codeblocks"]),
        Application("Visual Studio", "IDE de développement.", "vscode.png", True, [
            "sudo apt-get install wget gpg",
            "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg",
            "sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg",
            "echo \"deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main\" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null",
            "rm -f packages.microsoft.gpg",
            "sudo apt install apt-transport-https",
            "sudo apt update",
            "sudo apt install code"
        ]),
        Application("Python", "Python.", "python.png", True, ["sudo apt-get install python3", "sudo apt-get install python3-pip"]),
        Application("PyInstaller", "Python compiler (Requires Python)", "python.png", True, ["sudo pip install pyinstaller"]),
        Application("Build-Essential", "Compiler for Linux (C, C++)", "build-essential.png", True, ["sudo apt install build-essential"]),
        Application("Qt Creator", "IDE + Framework de développement multi-plateforme Linux", "qt.png", True, [
            "xdg-open https://d13lb3tujbc8s0.cloudfront.net/onlineinstallers/qt-online-installer-linux-x64-4.8.1.run",
            "sudo apt-get install -y libxcb-cursor-dev"
        ]),
        Application("Docker", "Container manager tool", "docker.png", True, [
            "sudo apt-get update",
            "sudo apt-get install ca-certificates curl",
            "sudo install -m 0755 -d /etc/apt/keyrings",
            "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
            "sudo chmod a+r /etc/apt/keyrings/docker.asc",
            "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$UBUNTU_CODENAME\") stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
            "sudo apt-get update",
            "sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
            "sudo docker run hello-world",
            "sudo apt install docker-compose"
        ]),
        Application("Git", "Version manager tools", "git.png", True, ["sudo apt install git-all"]),
        Application("Unity Hub", "Unity Game Engine", "unity.png", True, [
            "wget -qO - https://hub.unity3d.com/linux/keys/public | gpg --dearmor | sudo tee /usr/share/keyrings/Unity_Technologies_ApS.gpg > /dev/null",
            "sudo sh -c 'echo \"deb [signed-by=/usr/share/keyrings/Unity_Technologies_ApS.gpg] https://hub.unity3d.com/linux/repos/deb stable main\" > /etc/apt/sources.list.d/unityhub.list\'",
            "sudo apt update",
            "sudo apt-get install unityhub"
        ])
    ],
    "Utilities": [
        Application("Snap", "Linux package manager", "snap.png", True, ["sudo rm /etc/apt/preferences.d/nosnap.pref", "sudo snap install vlc"]),
        Application("VLC Media Player", "Video media player (Require Snap)", "vlc.png", True, ["sudo rm /etc/apt/preferences.d/nosnap.pref", "sudo apt install snapd"]),
        Application("Wine", "Emulator for Windows apps", "wine.png", True, ["sudo apt install wine64 wine32"]),
        Application("Thème Windows", "Installer un thème windows", "windows.png", True, [
            "wget https://github.com/B00merang-Project/Windows-10-Dark/archive/refs/tags/3.2.1-dark.zip",
            "mkdir -p ~/\".themes\"",
            "mv 3.2.1-dark.zip ~/.themes/",
            "cd ~/.themes/",
            "unzip 3.2.1-dark.zip",
            "rm 3.2.1-dark.zip",
            "wget https://github.com/B00merang-Artwork/Windows-10/archive/master.zip",
            "mkdir -p ~/\".icons\"",
            "mv master.zip ~/.icons/",
            "cd ~/.icons/",
            "unzip master.zip",
            "rm master.zip"
        ]),
        Application("Solaar", "Logitech device manager", "logitech.png", True, ["sudo apt install solaar"])
    ]
}
