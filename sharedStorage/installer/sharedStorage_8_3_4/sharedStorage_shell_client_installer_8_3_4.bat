@echo off

echo Installiere sharedStorage Shell...
xcopy /s \\nas-server\nas-share\Installer\sharedStorage_HTML_UI_Shell-1.1.3-cef115-win.exe /d .\
.\sharedStorage_HTML_UI_Shell-1.1.3-cef115-win.exe
del sharedStorage_HTML_UI_Shell-1.1.3-cef115-win.exe

echo.
echo Installiere sharedStorage Client 8.3.4...
xcopy /s \\nas-server\nas-share\Installer\sharedStorage_Hub_Windows_Client_8.3.4.exe /d .\
.\sharedStorage_Hub_Windows_Client_8.3.4.exe
del sharedStorage_Hub_Windows_Client_8.3.4.exe

echo.
xcopy /s \\nas-server\nas-share\Installer\sharedStorage_CMD_Server_Config.bat /d .\
echo Fuehre Server Config aus...
echo.
.\sharedStorage_CMD_Server_Config.bat