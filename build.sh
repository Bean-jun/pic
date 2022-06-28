rm -rf .vscode
rm -rf .idea
rm -rf build
rm -rf dist
# rm -rf Release/client/*
# rm -rf Release/server/*

pyinstaller -F src/client/command.py
cp dist/command Release/client/command_darwin_amd64
pyinstaller -F src/client/listener.py
cp dist/listener Release/client/listener_darwin_amd64
pyinstaller -w -F src/client/listener_gui.py
cp dist/listener_gui Release/client/listener_gui_darwin_amd64

# python server不进行编译
# pyinstaller -F src/server/main.py
# cp dist/main Release/server/server


rm -rf .vscode
rm -rf .idea
rm -rf build
rm -rf dist
rm -rf *.spec