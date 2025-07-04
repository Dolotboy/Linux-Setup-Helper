# Linux Setup Helper Readme

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A tool that helps new Linux user to setup and install what they need 

## Dependencies

- [python](https://www.python.org/downloads/)
- [python tk / pip install tk](https://docs.python.org/3/library/tkinter.html)
- [python pyinstaller / pip install pysintaller](https://pyinstaller.org/en/stable/)

## Run the container
- sudo docker-compose up
If you have an error like this one:
```bash
Starting python_linuxSetupHelper ... done
Attaching to python_linuxSetupHelper
python_linuxSetupHelper | Authorization required, but no authorization protocol specified
python_linuxSetupHelper | Authorization required, but no authorization protocol specified
python_linuxSetupHelper | Traceback (most recent call last):
python_linuxSetupHelper |   File "/usr/src/app/main.py", line 147, in <module>
python_linuxSetupHelper |     create_gui()
python_linuxSetupHelper |   File "/usr/src/app/main.py", line 45, in create_gui
python_linuxSetupHelper |     root = tk.Tk()
python_linuxSetupHelper |            ^^^^^^^
python_linuxSetupHelper |   File "/usr/local/lib/python3.12/tkinter/__init__.py", line 2346, in __init__
python_linuxSetupHelper |     self.tk = _tkinter.create(screenName, baseName, className, interactive, wantobjects, useTk, sync, use)
python_linuxSetupHelper |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
python_linuxSetupHelper | _tkinter.TclError: couldn't connect to display ":0"
python_linuxSetupHelper exited with code 1
```
Then execute this command before the step 1 : xhost +si:localuser:root

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