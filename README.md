# Linux Setup Helper Readme

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A tool that helps new Linux user to setup and install what they need 

## Dependencies

- [python](https://www.python.org/downloads/)
- [python tk / pip install tk](https://docs.python.org/3/library/tkinter.html)
- [python pyinstaller / pip install pysintaller](https://pyinstaller.org/en/stable/)

## Compile

If you are running the tool under Docker (With the included files in the repository), you will need to execute the pyinstaller command inside the Docker container:
```sh
$ sudo docker exec -it python_linuxSetupHelper pyinstaller --onefile main.py
# Execute a command inside the Docker container named python_linuxSetupHelper, this will output a binary executable file named main inside the dist folder
```

If you run this app with a python installed on the host, you can simply run this command in the folder:
```sh
$ pyinstaller --onefile main.py
# This will output a binary executable file named main inside the dist folder
```

## Errors

If you get this error while using docker-compose up (On Linux): 
```sh
$ getting display:0
```
Use this command:
```sh
$ xhost +local:root
```

## Maintainers

[@Dolotboy](https://github.com/Dolotboy).

### Contributors

This project exists thanks to all the people who contribute. 
<a href="https://github.com/Dolotboy/Linux-Setup-Helper/graphs/contributors">Dolotboy</a>

## License

[MIT](LICENSE) © Dolotboy