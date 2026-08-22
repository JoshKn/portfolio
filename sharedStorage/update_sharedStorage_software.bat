:: Full update script for sharedStorage and Software for Program.
:: Unmounts all sharedStorage drives, uninstalls the old client and shell, deletes the sharedStorage folder,
:: then copies and runs fresh installers for the sharedStorage shell, client, Software, and server config.

@echo off

echo Unmounte alle Drives...
plchld unmount -a

echo.
echo Deinstalliere alte sharedStorage Version...
C:\Windows\sharedStorage\plchduninstall.exe
echo Druecke irgendeine Taste um die Shell zu deinstallieren. &pause>nul

echo.
echo Deinstalliere sharedStorage Shell...
C:\Windows\sharedStorage\huishell\huiuninstall.exe
C:\Windows\sharedStorage\huishell2\x64\huiuninstall.exe
echo Druecke irgendeine Taste um den sharedStorage Ordner zu loeschen. &pause>nul

echo.
echo Loesche den sharedStorage Ordner...
rd "C:\Windows\sharedStorage\" /s /q
start "" "C:\Windows\"
echo Wurde der Ordner C:\Windows\sharedStorage\ entfernt? Wenn ja druecke j, sonst loesche bitte von Hand &pause>nul

echo.
echo Installiere sharedStorage Shell...
xcopy /s \\nas-server\nas-share\Installer\sharedStorage_HTML_UI_Shell-1.1.1-cef115-win.exe /d .\
.\sharedStorage_HTML_UI_Shell-1.1.1-cef115-win.exe
del sharedStorage_HTML_UI_Shell-1.1.1-cef115-win.exe

echo.
echo Installiere sharedStorage Client 8.3.0...
xcopy /s \\nas-server\nas-share\Installer\sharedStorage_Hub_Windows_Client_8.3.0.exe /d .\
.\sharedStorage_Hub_Windows_Client_8.3.0.exe
del sharedStorage_Hub_Windows_Client_8.3.0.exe

echo.
echo Installiere Software 6.0...
del Software_for_Program-6.0.21475.msi
xcopy /s \\nas-server\nas-share\Installer\Software_for_Program-6.0.21475.msi /d .\
.\Software_for_Program-6.0.21475.msi
del Software_for_Program-6.0.21475.msi

echo.
xcopy /s \\nas-server\nas-share\Installer\sharedStorage_CMD_Server_Config_8_3_0.bat /d .\
echo Fuehre Server Config aus...
echo.
.\sharedStorage_CMD_Server_Config_8_3_0.bat