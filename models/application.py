class Application:
    def __init__(self, name, description, image, open_console, commands):
        self.name = name
        self.description = description
        self.image = image
        self.open_console = open_console
        self.commands = commands

    def __repr__(self):
        return f"Application(name={self.name}, description={self.description}, image={self.image})"