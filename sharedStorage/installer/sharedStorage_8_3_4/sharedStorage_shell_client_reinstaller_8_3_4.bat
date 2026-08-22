@echo off

wmic datafile where Name="C:\\Windows\\sharedStorage\\fcconsole.exe" get Name,Version /format:table
echo Ist die oben angegebene sharedStorage Version veraltet? Wenn nein schliesse das Fenster, wenn du weiter installieren willst druecke j &pause>nul

echo Unmounte alle Drives...
plchld unmount -a

echo.
echo Deinstalliere alte sharedStorage Version...
C:\Windows\sharedStorage\fcuninstall.exe
echo Druecke irgendeine Taste um die Shell zu deinstallieren. &pause>nul

echo.
echo Deinstalliere sharedStorage Shell...
C:\Windows\sharedStorage\huishell2\x64\huiuninstall.exe
echo Druecke irgendeine Taste um den sharedStorage Ordner zu loeschen. &pause>nul

echo.
echo Loesche den sharedStorage Ordner...
rd "C:\Windows\sharedStorage\" /s /q
start "" "C:\Windows\"
echo Wurde der Ordner C:\Windows\sharedStorage\ entfernt? Wenn ja druecke j, sonst loesche bitte von Hand &pause>nul

echo.
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