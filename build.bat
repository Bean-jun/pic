pyinstaller -F src\client\command.py -i images\pic.ico
copy /Y dist\command.exe Release\client\command_windows_amd64.exe
pyinstaller -F src\client\listener.py -i images\pic.ico
copy /Y dist\listener.exe Release\client\listener_windows_amd64.exe
pyinstaller -w -F src\client\listener_gui.py -i images\pic.ico
copy /Y dist\listener_gui.exe Release\client\listener_gui_windows_amd64.exe