rm -rf .vscode
rm -rf .idea
rm -rf build
rm -rf dist
rm -rf Release/client/*
rm -rf Release/server/*

pyinstaller -F src/client/main.py
cp dist/main Release/client/main
pyinstaller -F src/client/listener.py
cp dist/listener Release/client/listener

# python server不进行编译
# pyinstaller -F src/server/main.py
# cp dist/main Release/server/server